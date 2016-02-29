from django.shortcuts import render
import requests
from .models import *
import json

def index(request):
    url = "https://gale43.atlassian.net/rest/auth/1/session"
    headers = {"Content-Type":"application/json","Accept":"application/json"}
    data = json.dumps({"username":"dipika.singhania","password":"gale@123!"})
    resp = requests.request("POST", url, headers=headers, data=data)
    sessionid = resp.json()['session']['value']
    projectName = 'Hello'
    try:
        pro = Project.objects.get(name=projectName)
        pro.sessionid = sessionid
    except:
        pro = Project(name=projectName, sessionid=sessionid)
    pro.save()
    return render(request, 'board/d1.html', {})
