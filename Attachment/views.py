from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from .models import Attachment  

from django.contrib import messages

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import AttachmentSerializer
from rest_framework.parsers import JSONParser

import os
from django.core.files.storage import FileSystemStorage
import json

# Create your views here.  

#Attachment Create API
@api_view(['POST'])
def create(request):
    try:
        LinkType = request.data['LinkType']
        LinkID = request.data['LinkID']
        Caption = request.data['Caption']
        CreateDate = request.data['CreateDate']
        CreateTime = request.data['CreateTime']
        UpdateDate = CreateDate
        UpdateTime = CreateTime
        
        File = request.data['File']
        attachmentsImage_url = ""
        if File !="" :
            target ='./bridge/static/image/Attachment'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+File.name, File)
            productImage_url = fss.url(file)
            attachmentsImage_url = productImage_url.replace('/bridge/', '/')
            

        model=Attachment(File=attachmentsImage_url, LinkType=LinkType, Caption=Caption, LinkID=LinkID, CreateDate=CreateDate, CreateTime=CreateTime, UpdateDate=UpdateDate, UpdateTime=UpdateTime)
        
        model.save()
        return Response({"message":"successful","status":"200","data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})

#Attachment Create API
@api_view(['POST'])
def createmany(request):
    try:
        LinkType = request.data['LinkType']
        LinkID = request.data['LinkID']
        Caption = request.data['Caption']
        CreateDate = request.data['CreateDate']
        CreateTime = request.data['CreateTime']
        UpdateDate = CreateDate
        UpdateTime = CreateTime
        for File in request.FILES.getlist('File'):
            attachmentsImage_url = ""
            if File !="" :
                target ='./bridge/static/image/Attachment'
                os.makedirs(target, exist_ok=True)
                fss = FileSystemStorage()
                file = fss.save(target+"/"+File.name, File)
                productImage_url = fss.url(file)
                attachmentsImage_url = productImage_url.replace('/bridge/', '/')
                print(attachmentsImage_url)
                

            model=Attachment(File=attachmentsImage_url, LinkType=LinkType, Caption=Caption, LinkID=LinkID, CreateDate=CreateDate, CreateTime=CreateTime, UpdateDate=UpdateDate, UpdateTime=UpdateTime)
            
            model.save()
        return Response({"message":"successful","status":"200","data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})


#Attachment All API
@api_view(["POST"])
def all(request):
    try:
        LinkID=request.data['LinkID']
        LinkType=request.data['LinkType']
        Attachment_obj = Attachment.objects.filter(LinkID=LinkID, LinkType=LinkType) 
        Attachment_json = AttachmentSerializer(Attachment_obj, many=True)
        return Response({"message": "Success","status": 200,"data":Attachment_json.data})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})


#Attachment One API
@api_view(["POST"])
def one(request):
    try:
        id=request.data['id']
        Attachment_obj = Attachment.objects.get(id=id)
        Attachment_json = AttachmentSerializer(Attachment_obj)
        return Response({"message": "Success","status": 200,"data":[Attachment_json.data]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})


#Attachment Update API
@api_view(['POST'])
def update(request):
    try:
        fetchid = request.data['id']
        model = Attachment.objects.get(pk = fetchid)
        model.LinkID = request.data['LinkID']
        model.Caption = request.data['Caption']
        model.LinkType = request.data['LinkType']
        model.UpdateDate = request.data['UpdateDate']
        model.UpdateTime = request.data['UpdateTime']
        
        File = request.data['File']
        attachmentsImage_url = ""
        if File !="" :
            target ='./bridge/static/image/Attachment'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+File.name, File)
            productImage_url = fss.url(file)
            attachmentsImage_url = productImage_url.replace('/bridge/', '/')
            model.File = attachmentsImage_url
        print(attachmentsImage_url)
        model.save()
        return Response({"message":"successful","status":"200","data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})

#Attachment delete
@api_view(['POST'])
def delete(request):
    try:
        fetchid=request.data['id']
        fetchdata=Attachment.objects.filter(pk=fetchid).delete()
        return Response({"message":"successful","status":"200","data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})

