from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from api.models import Deploy, App
from django.core.serializers import serialize
from api.tasks import deploy

import os
import subprocess

BASE_REPO_PATH = '/srv/git'

#@csrf_exempt
def push_deploy(request, username, app_name):
    application = App.objects.get(username=username, name=app_name)
    dep = Deploy(status="pending", app=application)
    dep.save()

    deploy.delay(dep.id)
    return JsonResponse({'deploy_id': dep.id})

#@csrf_exempt
def list_deploys(request, username, app_name):
    try:
        application = App.objects.get(name=app_name)
        deploys = Deploy.objects.filter(app = application.id)
        serialized_deploys = []
        for deploy in deploys:
            serialized_deploys.append({'created_at': deploy.created_at, 'status': deploy.status})
        return JsonResponse({'deploys' : serialized_deploys})
    except App.DoesNotExist:
        return JsonResponse({'deploys': []})


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
    repo_path = BASE_REPO_PATH + "/" + username + "_" + appname + '.git'
    app = App(username=username, name=appname, repo_path=repo_path)
    app.save()

    os.mkdir(repo_path)
    subprocess.run(['git', 'init', '--bare', repo_path])
    with open(repo_path + '/hooks/post-receive', 'w') as hook:
        hook.write("#!/bin/sh\ncurl -X POST localhost:8000/{}/apps/{}/deploy".format(app.username, app.name))
        os.fchmod(hook.fileno(), 0o755)

    return JsonResponse({'username': app.username, 'name': app.name, 'repo_path': app.repo_path})
#
#@csrf_exempt
#def show_deploy(username):
#    pass
