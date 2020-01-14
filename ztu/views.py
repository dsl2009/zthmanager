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
        if user_auth == 'true':
            user_auth = 1
        else:
            user_auth = 0
        dt = data_manager.add_manager(tel_num=user_tel,user_name=username, pre=user_auth)
        return HttpResponse(json.dumps(dt,cls=CJsonEncoder))
    else:
        return HttpResponse(json.dumps({'status': 400, 'message': 'fail'}))

def update_user(request):
    username = request.GET.get("user_name", None)
    user_auth = request.GET.get("user_auth", None)
    user_tel = request.GET.get("user_tel", None)
    user_id = request.GET.get("user_id", None)
    if username and user_auth and user_tel:
        if user_auth=='true':
            user_auth=1
        else:
            user_auth=0

        dt = data_manager.update_manager(tel_num=user_tel,user_name=username, pre=user_auth,manager_id=user_id)
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
    user_tel = request.GET.get("user_tel", None)
    if user_tel:
        dt = data_manager.delete_mananger(user_tel)
        return HttpResponse(json.dumps(dt, cls=CJsonEncoder))
    else:
        return HttpResponse(json.dumps({'status': 400, 'message': 'fail'}))

def get_devices_web_company(request):
    code = request.GET.get("company_id", None)
    if code:
        data = data_manager.get_device_by_company_web(code)
        return HttpResponse(json.dumps(data))
    else:
        data = dict()
        data['status'] = 404
        return HttpResponse(json.dumps(data))

def get_device_history(request):
    dev_mac = request.GET.get("dev_mac", None)
    if dev_mac:
        dt = data_manager.get_devices_history(dev_mac)
        return HttpResponse(json.dumps(dt, cls=CJsonEncoder))
    else:
        return HttpResponse(json.dumps({'status': 400, 'message': 'fail'}))