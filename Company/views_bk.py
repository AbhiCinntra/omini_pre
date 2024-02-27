from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from .forms import CompanyForm  
from .models import Branch, Company  

from django.contrib import messages

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import BranchSerializer, CompanySerializer
from rest_framework.parsers import JSONParser
# Create your views here.  

#Company Create API
@api_view(['POST'])
def create(request):
    name = request.data['name']
    desc = request.data['desc']
    phone = request.data['phone']
    email = request.data['email']
    
    state = request.data['state']
    city = request.data['city']
    pincode = request.data['pincode']
    address = request.data['address']
    
    natureOfIndustry = request.data['natureOfIndustry']
    ERP = request.data['ERP']
    serverIP = request.data['serverIP']
    port = request.data['port']
    user = request.data['user']
    password = request.data['password']
    
    license_limit = request.data['license_limit']
    active = request.data['active']
    timestamp = request.data['timestamp']

    model=Company(name = name, desc = desc,  phone = phone, email = email, state=state, city=city, pincode=pincode, address=address,  natureOfIndustry = natureOfIndustry, ERP = ERP, serverIP = serverIP, port = port, user = user, password = password, license_limit = license_limit, active = active, timestamp = timestamp)
    
    model.save()
    return Response({"message":"successful","status":"200","data":[]})

#Company All API
@api_view(["GET"])
def all(request):
    companys_obj = Company.objects.all() 
    company_json = CompanySerializer(companys_obj, many=True)
    return Response({"message": "Success","status": 200,"data":company_json.data})

#Company One API
@api_view(["POST"])
def one(request):
    id=request.data['id']
    company_obj = Company.objects.get(id=id)
    company_json = CompanySerializer(company_obj)
    return Response({"message": "Success","status": 200,"data":[company_json.data]})


#Company Update API
@api_view(['POST'])
def update(request):
    fetchid = request.data['id']
    try:
        model = Company.objects.get(pk = fetchid)

        model.id = request.data['id']
        model.name = request.data['name']
        model.desc = request.data['desc']
        model.phone = request.data['phone']
        model.email = request.data['email']

        model.state = request.data['state']
        model.city = request.data['city']
        model.pincode = request.data['pincode']
        model.address = request.data['address']
        
        model.natureOfIndustry = request.data['natureOfIndustry']
        model.ERP = request.data['ERP']
        model.serverIP = request.data['serverIP']
        model.port = request.data['port']
        model.user = request.data['user']
        model.password = request.data['password']
        
        model.license_limit = request.data['license_limit']
        model.active = request.data['active']
        model.save()
        context = {
            "id":request.data['id'],
            'name':request.data['name'],
            'desc':request.data['desc'],
            'phone':request.data['phone'],
            'email':request.data['email'],
            'state':request.data['state'],
            'city':request.data['city'],
            'pincode':request.data['pincode'],
            'address':request.data['address'],
            
            'natureOfIndustry':request.data['natureOfIndustry'],
            'ERP':request.data['ERP'],
            'serverIP':request.data['serverIP'],
            'port':request.data['port'],
            'user':request.data['user'],
            'password':request.data['password'],

            'license_limit':request.data['license_limit'],
            'active':request.data['active']
            }

        return Response({"message":"successful","status":"200","data":[context]})
    except:
        return Response({"message":"ID Wrong","status":"201","data":[]})

#Company delete
@api_view(['POST'])
def delete(request):
    fetchid=request.data['id']
    try:
        fetchdata=Company.objects.filter(pk=fetchid).delete()
        return Response({"message":"successful","status":"200","data":[]})
    except:
        return Response({"message":"Id wrong","status":"201","data":[]})


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(["GET"])
def all_branches(request):
    try:
        branch_obj = Branch.objects.filter(Disabled = 'tNO')
        branch_json = BranchSerializer(branch_obj, many=True)
        return Response({"message": "Success","status": 200,"data":branch_json.data})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
