from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from .forms import CountriesForm  
from .models import *

from django.contrib import messages

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import *
from rest_framework.parsers import JSONParser
# Create your views here.  

#Countries All API
@api_view(["GET"])
def all(request):
    cnt_obj = Countries.objects.all()
    cnt_json = CountriesSerializer(cnt_obj, many=True)
    return Response({"message": "Success","status": 200,"data":cnt_json.data})
