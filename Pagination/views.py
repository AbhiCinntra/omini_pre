from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import *
from rest_framework import status    
import requests, json

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import *
from rest_framework.parsers import JSONParser

from pytz import timezone
from datetime import datetime as dt

date = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d')
yearmonth = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m')
time = dt.now(timezone("Asia/Kolkata")).strftime('%H:%M %p')

@api_view(['POST'])
def create(request):
    serializer = PagePostSerializer(data=request.data)
    print(serializer)
    if serializer.is_valid():
        serializer.save()
        return Response({'status':status.HTTP_200_OK,'message':'Success','data':[]})
    return Response({'status':status.HTTP_400_BAD_REQUEST,'message':'Invalid_data', 'data':[]})


@api_view(['GET'])
def all(request):
    page_obj = Pagination.objects.all()
    page_data = PageGetSerializer(page_obj, many=True)
    return Response({"message":"Success","status":200,"data":page_data.data})