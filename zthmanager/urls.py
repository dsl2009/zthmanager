"""zthmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from ztu import views
from django.conf.urls import url
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^api/login', views.login, name='login'),
    url(r'^api/get_kehu', views.get_kehu, name='get_kehu'),
    url(r'^api/add_kehu', views.add_kehu, name='add_kehu'),
    url(r'^api/login_super', views.super_login, name='super_login'),
    url(r'^api/add_super', views.add_super_user, name='add_super_user'),
    url(r'^api/delete_super', views.delete_super_user, name='delete_super_user'),
    url(r'^api/bind_super', views.bind_super_user, name='bind_super_user'),
    url(r'^api/get_super', views.get_super_user, name='get_super_user'),
    url(r'^api/update_kehu', views.update_kehu, name='update_kehu'),
    url(r'^api/get_devices', views.get_devices_web_company, name='get_devices_web_company'),
    url(r'^api/get_static_time', views.get_static_time, name='get_static_time'),
    url(r'^api/get_device_history', views.get_device_history, name='get_device_history'),
    url(r'^api/get_history', views.get_history, name='get_history'),
    url(r'^api/add_user', views.add_user, name='add_user'),
    url(r'^api/delete_user', views.delete_user, name='delete_user'),
    url(r'^api/update_user', views.update_user, name='update_user'),
    url(r'^api/get_all_user', views.get_all_manager, name='get_all_manager'),
    url(r'^$',TemplateView.as_view(template_name='index.html')),

]
