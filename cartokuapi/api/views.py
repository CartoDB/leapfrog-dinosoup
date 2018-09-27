from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from api.models import Deploy, App
from django.core.serializers import serialize
from api.tasks import deploy

#@csrf_exempt
def push_deploy(request, username, app_name):
    status = request.POST['status']
    applications = App.objects.filter(name=app_name)
    if len(applications) == 0:
        application = App(name=app_name, username = username)
        application.save()
    else:
        application = applications[0]
    deploy = Deploy(status = status, app = application)
    deploy.save()
    deploy_id = deploy.id

    deploy.delay(deploy_id)
    return JsonResponse({'deploy_id': deploy_id})

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
#
#@csrf_exempt
#def show_deploy(username):
#    pass
