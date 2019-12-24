from django.shortcuts import render
from django.http import HttpResponse
import json

def login(request):
    username = request.GET.get("username", None)
    password = request.GET.get("password", None)
    if username and password:
        if username=='admin' and password=='900504':
            return HttpResponse(json.dumps({'status':200,'message':'ok'}))
        else:
            return HttpResponse(json.dumps({'status': 400, 'message': 'fail'}))
    else:
        return HttpResponse(json.dumps({'status': 400, 'message': 'fail'}))
