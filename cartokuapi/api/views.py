from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from api.models import Deploy, App
from django.core.serializers import serialize
from api.tasks import deploy

import os
import subprocess

BASE_REPO_PATH = '/srv/git'
DOMAIN = 'carto.ku'
PORT = 8000

def push_deploy(request, username, app_name):
    commit_hash = request.POST['commit_hash']
    application = App.objects.get(username=username, name=app_name)
    dep = Deploy(status="pending", app=application)
    dep.commit_hash_abbreviated = commit_hash
    dep.save()

    deploy.delay(dep.id)
    return JsonResponse({'deploy_id': dep.id, 'deploy_status_url': deploy_poll_url(username, app_name, dep.id)})

def get_deploys_list (username, app_name):
    try:
        application = App.objects.get(name=app_name)
        deploys = Deploy.objects.filter(app = application.id)
        serialized_deploys = []
        for deploy in deploys:
            serialized_deploys.append({'created_at': deploy.created_at, 'status': deploy.status, 'commit_hash_abbreviated': deploy.commit_hash_abbreviated})
        return serialized_deploys
    except App.DoesNotExist:
        return []

def list_deploys(request, username, app_name):
    return JsonResponse({'deploys' : get_deploys_list})

def apps(request, username):
    if request.method == 'POST':
        appname = request.POST['name']
        appdesc = request.POST['description']
        return JsonResponse(create_app(username, appname, appdesc))
    else:
        return JsonResponse({'apps' : get_apps_list(username)})

def get_apps_list(username):
    try:
        apps = App.objects.filter(username = username)
        serialized_apps = []
        for app in apps:
            serialized_apps.append({'name': app.name, 'repo_path': app.repo_path, 'status': app.status, 'stack': app.stack, 'description' : app.description, 'url': app_url(username, app.name)})
        return serialized_apps
    except App.DoesNotExist:
        return []

def get_deploy(request, username, app_name, deploy_id):
    try:
        application = App.objects.get(name=app_name)
        deploys = Deploy.objects.filter(app=application.id, id=deploy_id)
        serialized_deploys = []
        for deploy in deploys:
            serialized_deploys.append({'created_at': deploy.created_at, 'status': deploy.status, 'log': deploy.log, 'commit_hash_abbreviated': deploy.commit_hash_abbreviated})
        return JsonResponse({'deploys' : serialized_deploys})
    except App.DoesNotExist:
        return JsonResponse({'deploys': []})


def create_app(username, appname, appdesc):
    if len(App.objects.filter(name=appname)) > 0:
        return({'message': "App %s already exists" % appname})
    repo_path = BASE_REPO_PATH + "/" + username + "_" + appname + '.git'
    app = App(username=username, name=appname, repo_path=repo_path)
    app.stack = "python"
    app.description = appdesc
    app.save()

    os.mkdir(repo_path)
    subprocess.run(['git', 'init', '--bare', repo_path])
    hook_content = """
#!/bin/sh
red='\033[0;31m'
green='\033[0;32m'
yellow='\033[0;33m'
blue='\033[0;34m'
no_color='\033[0m'

commit_hash=`git log master --format="%%h" -n 1`
response=`curl -X POST localhost:8000/%s/apps/%s/deploy -d commit_hash=${commit_hash}`
status_url=`echo ${response} | jq '.deploy_status_url'`

date >> /tmp/git_hook.log
echo "\n${blue}Deployed! Check your app at: ${green}${status_url}${no_color}\n"
""" % (app.username, app.name)
    with open(repo_path + '/hooks/post-receive', 'w') as hook:
        hook.write(hook_content)
        os.fchmod(hook.fileno(), 0o755)
    
    return({'username': app.username, 'name': app.name, 'repo_path': app.repo_path, 'deploy_instructions' : deploy_instructions(app.repo_path)})

def show_app(request, username, app_name):
    print(app_name)
    try:
        application = App.objects.get(name=app_name)
        app_data = {
                "name": application.name,
                "deploy_instructions" : deploy_instructions(application.repo_path),
                "username": application.username,
                "status": application.status,
                "stack": application.stack,
                "description": application.description,
                "url": app_url(username, app_name),
                "deploys_list": get_deploys_list(username, app_name)
                }
        return JsonResponse(app_data)
    except App.DoesNotExist:
        return JsonResponse({})

def app_url(username, app_name):
    return "http://%s.%s/" % (app_name, DOMAIN)

def deploy_poll_url(username, app_name, deploy_id):
    return "http://%s/%s/apps/%s/deploys/%d" % (DOMAIN, username, app_name, deploy_id)

def push_url(repo_path):
    return "ssh://git@cartoku%s" % repo_path

def deploy_instructions(repo_path):
    return [
            "git remote add cartoku %s" % push_url(repo_path),
            "git push cartoku master"
            ]
