from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from .forms import NotificationForm  
from .models import *
from Activity.models import *
from Activity.serializers import *

from django.contrib import messages

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import *
from rest_framework.parsers import JSONParser

from pytz import timezone
from datetime import datetime as dt
date = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d')
time = dt.now(timezone("Asia/Kolkata")).strftime('%H:%M %p')
print(date)
print(time)
# Create your views here.  

# @api_view(["GET"])
# def all(request):

    # top2bp = Activity.objects.raw('SELECT * FROM `activity_activity` WHERE `To` >= "2022-01-27"')

    # top5=[]

    # for od in top2bp:
        # print(od.Subject)
        # print(od.Name)
        # top5.append({"Subject":od.Subject, "Name":od.Name})
        
    # return Response({"message": "Success","status": 200,"data":top5})


#Notification All API
@api_view(["POST"])
def all(request):
    Emp=request.data['Emp']
    noti_all = []
    
    act_obj = Notification.objects.filter(Emp=Emp, CreatedDate=date).order_by("-id")
    #act_json = NotificationSerializer(act_obj, many=True)
    if len(act_obj) > 0:
        for obj in act_obj:
            noti_json = {}
            obj_json = NotificationSerializer(obj, many=False)
            #print(obj_json.data)
            
            noti_json["notification"] = obj_json.data
            #print(obj.SourceID)
            
            act_src = Activity.objects.get(id=obj.SourceID)
            src_json = ActivitySerializer(act_src)   
            noti_json["source"] = src_json.data
            
            noti_all.append(noti_json)
            print(noti_all)
    
        return Response({"message": "Success","status": 200,"data":noti_all})
    else:
        return Response({"message": "Success","status": 200,"data":[]})

#Notification One API
@api_view(["POST"])
def one(request):
    id=request.data['id']    
    act_obj = Notification.objects.get(id=id)
    act_json = NotificationSerializer(act_obj)
    
    act_src = Activity.objects.get(id=act_obj.SourceID)
    src_json = ActivitySerializer(act_src)
    return Response({"message": "Success","status": 200,"data":[act_json.data], "source":[src_json.data]})


#Notification Read API
@api_view(['POST'])
def read(request):
    fetchid = request.data['id']
    try:
        Notification.objects.filter(id = fetchid).update(Read = 1)
        return Response({"message":"successful","status":200,"data":[]})
    except:
        return Response({"message":"ID Wrong","status":201,"data":[]})


#Notification Delete API
@api_view(['POST'])
def delete(request):
    fetchid=request.data['id']
    try:
        Notification.objects.get(pk=fetchid).delete()
        return Response({"message":"successful","status":200,"data":[]})
    except Exception as e:
         return Response({"message":"Id wrong","status":201,"data":[str(e)]})


