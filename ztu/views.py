from django.shortcuts import render
from django.http import HttpResponse
import json
from ztu.CJsonEncoder import CJsonEncoder
from ztu import data_manager

def login(request):
    username = request.GET.get("user_name", None)
    password = request.GET.get("password", None)
    if username and password:
        return HttpResponse(json.dumps(data_manager.login(username,password),cls=CJsonEncoder))
    else:
        return HttpResponse(json.dumps({'status': 400, 'message': 'fail'}))


def add_user(request):
    username = request.GET.get("user_name", None)
    user_auth = request.GET.get("user_auth", None)
    user_tel = request.GET.get("user_tel", None)
    if username and user_auth and user_tel:
        dt = data_manager.add_manager(tel_num=user_tel,user_name=username, pre=int(user_auth))
        return HttpResponse(json.dumps(dt,cls=CJsonEncoder))
    else:
        return HttpResponse(json.dumps({'status': 400, 'message': 'fail'}))

def update_user(request):
    username = request.GET.get("user_name", None)
    user_auth = request.GET.get("user_auth", None)
    user_tel = request.GET.get("user_tel", None)
    user_id = request.GET.get("user_id", None)
    if username and user_auth and user_tel:
        dt = data_manager.update_manager(tel_num=user_tel,user_name=username, pre=int(user_auth),manager_id=user_id)
        return HttpResponse(json.dumps(dt,cls=CJsonEncoder))
    else:
        return HttpResponse(json.dumps({'status': 400, 'message': 'fail'}))

def get_all_manager(request):
    company_id = request.GET.get("company_id", None)
    if company_id:
        dt = data_manager.get_manager_by_company(company_id)
        return HttpResponse(json.dumps(dt, cls=CJsonEncoder))
    else:
        return HttpResponse(json.dumps({'status': 400, 'message': 'fail'}))
def delete_user(request):
    user_id = request.GET.get("user_id", None)
    if user_id:
        dt = data_manager.delete_mananger(user_id)
        return HttpResponse(json.dumps(dt, cls=CJsonEncoder))
    else:
        return HttpResponse(json.dumps({'status': 400, 'message': 'fail'}))
