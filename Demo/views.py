from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from .forms import DemoForm  
from .models import Demo  
import requests, json

from django.contrib import messages

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import DemoSerializer
from rest_framework.parsers import JSONParser
# Create your views here.  

#Branch Create API
@api_view(['POST'])
def create(request):
    name = request.data['name']
    phone = request.data['phone']
    email = request.data['email']
    company = request.data['company']
    timestamp = request.data['timestamp']
    
    with open("../bridge/bridge/db.json") as f:
        db = f.read()
        print(db)
    data = json.loads(db)
    
    if Demo.objects.filter(phone=request.data['phone']).exists():
        return Response({"message":"successful","status":"200","data":[data]})
    else:
        model=Demo(name = name, phone = phone, email = email, company=company, timestamp = timestamp)
        model.save()
        return Response({"message":"successful","status":"200","data":[data]})
