from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from .models import *
import requests, json
from django.contrib import messages

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import *
from rest_framework.parsers import JSONParser
# Create your views here.  

#States Create API
@api_view(["POST"])
def create(request):
    Code = request.data["Code"]
    Country = request.data["Country"]
    Name = request.data["Name"]

    if Countries.objects.filter(Code=Country).exists():
        if States.objects.filter(Code=Code, Country=Country).exists():
            return Response({"message":"State code already exist", "status":"201", "data":[]})
        
        else:
            if States.objects.filter(Name=Name, Country=Country).exists():
                return Response({"message":"State Name already exist", "status":"201", "data":[]})
            else:
                model = States(Code=Code, Country=Country, Name=Name)
                model.save()                
                return Response({"message":"Success", "status":"200", "data":[]})
    else:
        return Response({"message":"Country code not valid", "status":"201", "data":[]})


#States All API
@api_view(["POST"])
def all(request):
    Country = request.data['Country']
    st_obj = States.objects.filter(Country=Country)
    print(len(st_obj))
    if len(st_obj) > 0:
        st_json = StatesSerializer(st_obj, many=True)
        return Response({"message": "Success", "status": 200,"data":st_json.data})
    else:
        return Response({"message": "States are not available in this Country","status": 201, "data":[]})
