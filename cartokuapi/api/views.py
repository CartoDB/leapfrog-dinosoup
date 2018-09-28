from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from api.models import Deploy, App
from django.core.serializers import serialize
from api.tasks import deploy

import os
import subprocess

BASE_REPO_PATH = '/srv/git'

def push_deploy(request, username, app_name):
    application = App.objects.get(username=username, name=app_name)
    dep = Deploy(status="pending", app=application)
    dep.save()

    deploy.delay(dep.id)
    return JsonResponse({'deploy_id': dep.id})

def get_deploys_list (username, app_name):
    try:
        application = App.objects.get(name=app_name)
        deploys = Deploy.objects.filter(app = application.id)
        serialized_deploys = []
        for deploy in deploys:
            serialized_deploys.append({'created_at': deploy.created_at, 'status': deploy.status})
        return serialized_deploys
    except App.DoesNotExist:
        return []

def list_deploys(request, username, app_name):
    return JsonResponse({'deploys' : get_deploys_list})

def apps(request, username):
    if request.method == 'POST':
        appname = request.POST['name']
        create_app(username, name)        
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
            serialized_deploys.append({'created_at': deploy.created_at, 'status': deploy.status, 'log': deploy.log})
        return JsonResponse({'deploys' : serialized_deploys})
    except App.DoesNotExist:
        return JsonResponse({'deploys': []})


def create_app(request, username):
    appname = request.POST['name']
    appdesc = request.POST['description']
    if len(App.objects.filter(name=appname)) > 0:
        return JsonResponse({'message': "App %s already exists" % appname}, status=400)
    repo_path = BASE_REPO_PATH + "/" + username + "_" + appname + '.git'
    app = App(username=username, name=appname, repo_path=repo_path)
    app.stack = "python"
    app.description = appdesc
    app.save()

    os.mkdir(repo_path)
    subprocess.run(['git', 'init', '--bare', repo_path])
    with open(repo_path + '/hooks/post-receive', 'w') as hook:
        hook.write("#!/bin/sh\ncurl -X POST localhost:8000/{}/apps/{}/deploy".format(app.username, app.name))
        os.fchmod(hook.fileno(), 0o755)

    return JsonResponse({'username': app.username, 'name': app.name, 'repo_path': app.repo_path})

def show_app(request, username, app_name):
    print(app_name)
    try:
        application = App.objects.get(name=app_name)
        push_url = "ssh://git@cartoku%s" % application.repo_path
        app_data = {
                "name": application.name,
                "deploy_instructions" : ["git remote add cartoku %s" % push_url, "git push cartoku master"],
                "username": application.username,
                "url": app_url(username, app_name),
                "deploys_list": get_deploys_list(username, app_name)
                }
        return JsonResponse(app_data)
    except App.DoesNotExist:
        return JsonResponse({})

def app_url(username, app_name):
    return "http://%s.carto.ku/%s" % (username, app_name)
