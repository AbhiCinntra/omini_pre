from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from .forms import IndustriesForm  
from .models import Industries  
import requests, json

from django.contrib import messages

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import IndustriesSerializer
from rest_framework.parsers import JSONParser
# Create your views here.  

#Industries Create API
@api_view(['POST'])
def create(request):
    try:
        IndustryDescription = request.data['IndustryDescription']
        IndustryName = request.data['IndustryName']
        model=Industries(IndustryDescription = IndustryDescription, IndustryName = IndustryName)
        model.save()

        inds = Industries.objects.latest('id')
        inds.IndustryCode = inds.id
        inds.save()

        return Response({"message":"successful","status":200,"data":[{"Inds_Id":inds.id, "IndustryCode":inds.IndustryCode}]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[{"Error": str(e)}]})

#Industries All API
@api_view(["GET"])
def all(request):
    try:
        industries_obj = Industries.objects.all() 
        industrie_json = IndustriesSerializer(industries_obj, many=True)
        return Response({"message": "Success","status": 200,"data":industrie_json.data})
    except Exception as e:
        return Response({"message":"Error","status":201,"data":[{"Error": str(e)}]})

#Industries One API
@api_view(["POST"])
def one(request):
    try:
        id=request.data['id']
        industrie_obj = Industries.objects.get(id=id)
        industrie_json = IndustriesSerializer(industrie_obj)
        return Response({"message": "Success","status": 200,"data":[industrie_json.data]})
    except Exception as e:
        return Response({"message":"Error","status":201,"data":[{"Error": str(e)}]})
        
        
#Industries Update API
@api_view(['POST'])
def update(request):
    fetchid = request.data['id']
    try:
        model = Industries.objects.get(pk = fetchid)
        model.IndustryDescription = request.data['IndustryDescription']
        model.IndustryName = request.data['IndustryName']
        model.IndustryCode = request.data['IndustryCode']

        model.save()
        context = {
            "id":request.data['id'],
            'IndustryDescription':request.data['IndustryDescription'],
            'IndustryName':request.data['IndustryName'],
            'IndustryCode':request.data['IndustryCode'],
        }
            
        return Response({"message":"successful","status":"200","data":[context]})
    except:
        return Response({"message":"ID Wrong","status":"201","data":[context]})

#Industries delete
@api_view(['POST'])
def delete(request):
    fetchid=request.data['id']
    try:
        Industries.objects.filter(pk=fetchid).delete()
        return Response({"message":"successful","status":"200","data":[]})        
    except:
         return Response({"message":"Id wrong","status":"201","data":[]})

