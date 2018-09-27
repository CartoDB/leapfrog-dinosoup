from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from api.models import Deploy, App
from django.core.serializers import serialize
from api.tasks import deploy

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
#
#@csrf_exempt
#def show_deploy(username):
#    pass
