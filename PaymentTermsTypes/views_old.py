from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from .forms import PaymentTermsTypesForm  
from .models import PaymentTermsTypes  
import requests, json

from django.contrib import messages

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import PaymentTermsTypesSerializer
from rest_framework.parsers import JSONParser
# Create your views here.  

#PaymentTermsTypes Create API
@api_view(['POST'])
def create(request):
    try:
        PaymentTermsGroupName = request.data['PaymentTermsGroupName']
        model=PaymentTermsTypes(PaymentTermsGroupName = PaymentTermsGroupName)
        model.save()
        pay = PaymentTermsTypes.objects.latest('id')
        pay.GroupNumber = pay.id
        pay.save()

        return Response({"message":"successful","status":200,"data":[{"id":pay.id, "GroupNumber":pay.GroupNumber}]})
    except Exception as e:
        return Response({"message":"Error","status":201,"data":[]})


#PaymentTermsTypes All API
@api_view(["GET"])
def all(request):
    PaymentTermsTypes_obj = PaymentTermsTypes.objects.all() 
    industrie_json = PaymentTermsTypesSerializer(PaymentTermsTypes_obj, many=True)
    return Response({"message": "Success","status": 200,"data":industrie_json.data})


#PaymentTermsTypes One API
@api_view(["POST"])
def one(request):
    id=request.data['id']
    industrie_obj = PaymentTermsTypes.objects.get(id=id)
    industrie_json = PaymentTermsTypesSerializer(industrie_obj)
    return Response({"message": "Success","status": 200,"data":[industrie_json.data]})

#PaymentTermsTypes Update API
@api_view(['POST'])
def update(request):
    fetchid = request.data['id']
    try:
        model = PaymentTermsTypes.objects.get(pk = fetchid)
        model.PaymentTermsGroupName = request.data['PaymentTermsGroupName']
        model.GroupNumber = request.data['GroupNumber']
        model.save()

        context = {
            "id":request.data['id'],
            'PaymentTermsGroupName':request.data['PaymentTermsGroupName'],
            'GroupNumber':request.data['GroupNumber']
            }
           
        return Response({"message":"successful","status":"200", "data":[context]})
    except:
        return Response({"message":"ID Wrong","status":"201","data":[context]})

#PaymentTermsTypes delete
@api_view(['POST'])
def delete(request):
    fetchid=request.data['id']
    try:
        PaymentTermsTypes.objects.filter(pk=fetchid).delete()
        return Response({"message":"successful","status":"200","data":[]})        
    except:
        return Response({"message":"Id wrong","status":"201","data":[]})

