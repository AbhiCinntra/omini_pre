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

# import setting file
from django.conf import settings

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
        fetchid= inds.id

        inds_data = {
            "IndustryDescription": request.data['IndustryDescription'],
            "IndustryName": request.data['IndustryName']
        }
        res = settings.CALLAPI('post','/Industries', 'api', inds_data)
        live = json.loads(res.text)
        if "IndustryCode" in live:
            print(live['IndustryCode'])
            model = Industries.objects.get(pk = fetchid)
            model.IndustryCode = live['IndustryCode']
            model.save()

            return Response({"message":"successful","status":200,"data":[inds_data]})
        else:
            SAP_MSG = live['error']['message']['value']
            print(SAP_MSG)
            fetchdata=Industries.objects.filter(pk=fetchid).delete()
            return Response({"message":SAP_MSG,"SAP_error":SAP_MSG, "status":202,"data":[inds_data]})

        # return Response({"message":"successful","status":200,"data":[{"Inds_Id":inds.id, "IndustryCode":inds.IndustryCode}]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})

#Industries All API
@api_view(["GET"])
def all(request):
    try:
        industries_obj = Industries.objects.all() 
        industrie_json = IndustriesSerializer(industries_obj, many=True)
        return Response({"message": "Success","status": 200,"data":industrie_json.data})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})

#Industries One API
@api_view(["POST"])
def one(request):
    try:
        id=request.data['id']
        industrie_obj = Industries.objects.get(id=id)
        industrie_json = IndustriesSerializer(industrie_obj)
        return Response({"message": "Success","status": 200,"data":[industrie_json.data]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})
        

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

        inds_data = {
            "IndustryDescription": request.data['IndustryDescription'],
            "IndustryName": request.data['IndustryName']
        }
        
        print(inds_data)
        res = settings.CALLAPI('patch', '/Industries('+model.IndustryCode+')', 'api', inds_data)
        
        if len(res.content) !=0 :
            res1 = json.loads(res.content)
            SAP_MSG = res1['error']['message']['value']
            return Response({"message":"Partely successful","status":202,"SAP_error":SAP_MSG, "data":[request.data]})
        else:
            return Response({"message":"successful","status":200, "data":[request.data]})
            
        # return Response({"message":"successful","status":"200","data":[context]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})

#Industries delete
@api_view(['POST'])
def delete(request):
    fetchid=request.data['id']
    try:
        Industries.objects.filter(pk=fetchid).delete()
        return Response({"message":"successful","status":"200","data":[]})        
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})



# update Category
@api_view(['GET'])
def syncIndustries(request):
    try:
        # Import and sync item category
        itemINDS ="Industries/INDS.py"
        exec(compile(open(itemINDS, "rb").read(), itemINDS, 'exec'), {})
        
        return Response({"message":"Successful","status":200, "data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"Model": "Items" ,"data":[]})

