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
def super_login(request):
    username = request.GET.get("user_name", None)
    password = request.GET.get("password", None)
    if username and password:
        return HttpResponse(json.dumps(data_manager.login_super(username,password),cls=CJsonEncoder))
    else:
        return HttpResponse(json.dumps({'status': 400, 'message': 'fail'}))

def add_super_user(request):
    username = request.GET.get("user_name", None)
    user_auth = request.GET.get("user_auth", None)
    user_tel = request.GET.get("user_tel", None)
    if username and user_auth and user_tel:
        dt = data_manager.add_super_manager(tel_num=user_tel,user_name=username, auth=user_auth)
        return HttpResponse(json.dumps(dt,cls=CJsonEncoder))
    else:
        return HttpResponse(json.dumps({'status': 400, 'message': 'fail'}))

def delete_super_user(request):
    change_id = request.GET.get("change_id", None)
    delete_id = request.GET.get("delete_id", None)
    if delete_id :
        dt = data_manager.delete_super_mananger(change_id, delete_id)
        return HttpResponse(json.dumps(dt,cls=CJsonEncoder))
    else:
        return HttpResponse(json.dumps({'status': 400, 'message': 'fail'}))


def get_super_user(request):
    username = request.GET.get("user_id", None)
    if username==2:
        dt = data_manager.get_all_super_manager()
        return HttpResponse(json.dumps(dt,cls=CJsonEncoder))
    else:
        return HttpResponse(json.dumps( {'data':[],'status':200}))


def bind_super_user(request):
    super_id = request.GET.get("super_id", None)
    kehu_id = request.GET.get("kehu_id", None)
    if super_id and kehu_id:
        dt = data_manager.bind_super_manager(super_id, kehu_id)
        return HttpResponse(json.dumps(dt,cls=CJsonEncoder))
    else:
        return HttpResponse(json.dumps( {'msg':'fail','status':400}))



def add_user(request):
    username = request.GET.get("user_name", None)
    user_auth = request.GET.get("user_auth", None)
    user_tel = request.GET.get("user_tel", None)
    if username and user_auth and user_tel:
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
    delete_id = request.GET.get("delete_id", None)
    change_id = request.GET.get("change_id", None)
    if delete_id and change_id:
        dt = data_manager.delete_mananger(change_id=change_id, delete_id=delete_id)
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

def get_history(request):
    dev_mac = request.GET.get("dev_mac", None)
    if dev_mac:
        dt = data_manager.get_history(dev_mac)
        return HttpResponse(json.dumps(dt, cls=CJsonEncoder))
    else:
        return HttpResponse(json.dumps({'status': 400, 'message': 'fail'}))

def get_static_time(request):
    dev_mac = request.GET.get("dev_mac", None)
    if dev_mac:
        dt = data_manager.get_history_times(dev_mac)
        return HttpResponse(json.dumps(dt, cls=CJsonEncoder))
    else:
        return HttpResponse(json.dumps({'status': 400, 'message': 'fail'}))


def get_kehu(request):
    dt = data_manager.get_kehu()
    return HttpResponse(json.dumps(dt, cls=CJsonEncoder))
def add_kehu(request):
    user_name = request.GET.get("user_name", None)
    user_tel = request.GET.get("user_tel", None)
    user_login_name = request.GET.get("user_login_name", None)
    user_login_password = request.GET.get("user_login_password", None)
    if user_name and user_tel and user_login_name and user_login_password:
        dt = data_manager.add_kehu(user_name,  user_tel, user_login_name, user_login_password)
        return HttpResponse(json.dumps(dt, cls=CJsonEncoder))
    else:
        return HttpResponse(json.dumps({'status': 400, 'message': 'fail'}))
def update_kehu(request):
    user_name = request.GET.get("user_name", None)
    user_tel = request.GET.get("user_tel", None)
    user_login_name = request.GET.get("user_login_name", None)
    user_login_password = request.GET.get("user_login_password", None)
    user_id = request.GET.get("user_id", None)
    if user_name and user_tel and user_login_name and user_login_password:
        dt = data_manager.update_kehu(user_name,  user_tel, user_login_name, user_login_password,user_id)
        return HttpResponse(json.dumps(dt, cls=CJsonEncoder))
    else:
        return HttpResponse(json.dumps({'status': 400, 'message': 'fail'}))