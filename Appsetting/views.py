from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from .forms import AppsettingForm  
from .models import *
from Employee.models import Employee  

from django.contrib import messages

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import *
from rest_framework.parsers import JSONParser
# Create your views here.  

#Appsetting All API
@api_view(["GET"])
def all(request):
    Appsettings_obj = Appsetting.objects.all()        
    Appsetting_json = AppsettingSerializer(Appsettings_obj, many=True)
    return Response({"message": "Success","status": 200,"data":Appsetting_json.data})
