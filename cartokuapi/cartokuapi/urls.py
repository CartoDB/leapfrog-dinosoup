"""cartokuapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'<username>/apps/<app_name>/deploy', views.push_deploy),
    path(r'<username>/apps/<app_name>/deploys', views.list_deploys),
    path(r'<username>/apps/<app_name>/deploys/<deploy_id>', views.get_deploy),
]
    #path(r'<str:username>/deploys/<int:deploy_id>', views.show_deploy),
