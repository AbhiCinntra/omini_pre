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

# import setting file
from django.conf import settings

# Create your views here.  

#PaymentTermsTypes Create API
@api_view(['POST'])
def create(request):
    try:
        PaymentTermsGroupName = request.data['PaymentTermsGroupName']
        model=PaymentTermsTypes(PaymentTermsGroupName = PaymentTermsGroupName)
        model.save()
        
        pay = PaymentTermsTypes.objects.latest('id')
        fetchid = pay.id
    
        pay_data = {
            "PaymentTermsGroupName": request.data['PaymentTermsGroupName']
        }
        
        res = settings.CALLAPI('post', '/PaymentTermsTypes', 'api', pay_data)    
        live = json.loads(res.text)
        
        if "GroupNumber" in live:
            print(live['GroupNumber'])
            
            model = PaymentTermsTypes.objects.get(pk = fetchid)
            model.GroupNumber = live['GroupNumber']
            model.save()
            
            return Response({"message":"successful","status":200,"data":[{"id":pay.id, "GroupNumber":live['GroupNumber']}]})
        else:
            SAP_MSG = live['error']['message']['value']
            print(SAP_MSG)
            PaymentTermsTypes.objects.filter(pk=fetchid).delete()
            return Response({"message":SAP_MSG,"SAP_error":SAP_MSG, "status":202,"data":[pay_data]})

        # return Response({"message":"successful","status":200,"data":[{"id":pay.id, "GroupNumber":pay.GroupNumber}]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})


#PaymentTermsTypes All API
@api_view(["GET"])
def all(request):
    try:
        PaymentTermsTypes_obj = PaymentTermsTypes.objects.all() 
        industrie_json = PaymentTermsTypesSerializer(PaymentTermsTypes_obj, many=True)
        return Response({"message": "Success","status": 200,"data":industrie_json.data})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})

#PaymentTermsTypes One API
@api_view(["POST"])
def one(request):
    try:
        id=request.data['id']
        industrie_obj = PaymentTermsTypes.objects.get(id=id)
        industrie_json = PaymentTermsTypesSerializer(industrie_obj)
        return Response({"message": "Success","status": 200,"data":[industrie_json.data]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})


#PaymentTermsTypes Update API
@api_view(['POST'])
def update(request):
    fetchid = request.data['id']
    try:
        model = PaymentTermsTypes.objects.get(pk = fetchid)
        model.PaymentTermsGroupName = request.data['PaymentTermsGroupName']
        model.GroupNumber = request.data['GroupNumber']
        model.save()

        pay_data = {
            "PaymentTermsGroupName": request.data['PaymentTermsGroupName']
        }
        
        print(pay_data)
        res = settings.CALLAPI('patch', '/PaymentTermsTypes('+model.GroupNumber+')', 'api', pay_data)
        
        if len(res.content) !=0 :
            res1 = json.loads(res.content)
            SAP_MSG = res1['error']['message']['value']
            return Response({"message":"Partely successful","status":"202","SAP_error":SAP_MSG, "data":[request.data]})
        else:
            return Response({"message":"successful","status":"200", "data":[request.data]})
           
        # return Response({"message":"successful","status":"200", "data":[context]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})

#PaymentTermsTypes delete
@api_view(['POST'])
def delete(request):
    fetchid=request.data['id']
    try:
        PaymentTermsTypes.objects.filter(pk=fetchid).delete()
        return Response({"message":"successful","status":"200","data":[]})        
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})



# update syncPaymentTermsType
@api_view(['GET'])
def syncPaymentTermsType(request):
    try:
        # Import and sync item category
        itemPMT ="PaymentTermsTypes/PMT.py"
        exec(compile(open(itemPMT, "rb").read(), itemPMT, 'exec'), {})
        
        return Response({"message":"Successful","status":200, "data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"Model": "Items" ,"data":[]})


