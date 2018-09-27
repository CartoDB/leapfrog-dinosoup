from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from api.models import Deploy, App
from django.core.serializers import serialize


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
	response = {'deploy_id': deploy_id}
	return JsonResponse(response)

#@csrf_exempt 
def list_deploys(request, username, app_name):
	import pdb; pdb.set_trace()
	try:
		application = App.objects.get(name=app_name)
		#deploys = Deploy.objects.filter(app = application.id)
		serialized_deploys = serialize('json', Deploy.objects.filter(app = application.id), cls=LazyEncoder)
		return JsonResponse({'deploys' : serialized_deploys})	
	except App.DoesNotExist:
		return JsonResponse({'deploys': []})
#
#@csrf_exempt 
#def show_deploy(username):
#    pass

from django.core.serializers.json import DjangoJSONEncoder

class LazyEncoder(DjangoJSONEncoder):
	def default(self, obj):
		#if isinstance(obj, YourCustomType):
		#	return str(obj)
		return super().default(obj)
