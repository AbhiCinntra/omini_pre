from django.shortcuts import render
from rest_framework.decorators import api_view

from rest_framework.response import Response
from .serializers import *
import requests, json

import os
from django.core.files.storage import FileSystemStorage
# Create your views here.

@api_view(['POST'])
def create(request):
    try:
        DiscountName = request.data['DiscountName']
        Type = request.data['Type']
        SpecialInstr = request.data['SpecialInstr']

        attachmentsImage_url = ""
        File = request.data['Attach']
        attachmentsImage_url = ""
        if File !="" :
            print("in if")
            target ='./bridge/static/DiscountPolicy'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+File.name, File)
            productImage_url = fss.url(file)
            attachmentsImage_url = productImage_url.replace('/bridge/', '/')
            print(attachmentsImage_url)
        else:
            print('no images')

        discountPolicy = DiscountPolicy(DiscountName = DiscountName, Type = Type, SpecialInstr = SpecialInstr, Attach = attachmentsImage_url).save()
        
        return Response({"message":"successful","status":200,"data":[]})
    except Exception as e:
        return Response({"message": str(e),"status":201,"data":[]})

@api_view(['GET'])
def all(request):
    try:
        discountPolicyObj = DiscountPolicy.objects.all()
        discountPolicyJson = DiscountPolicySerializer(discountPolicyObj, many=True)
        return Response({"message":"successful","status":200,"data":discountPolicyJson.data})
    except Exception as e:
        return Response({"message": str(e),"status":201,"data":[]})