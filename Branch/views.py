from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from .forms import BranchForm  
from .models import Branch  

from django.contrib import messages

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import BranchSerializer
from rest_framework.parsers import JSONParser
# Create your views here.  

#Branch Create API
@api_view(['POST'])
def create(request):
    companyId = request.data['companyId']
    name = request.data['name']
    desc = request.data['desc']
    phone = request.data['phone']
    email = request.data['email']
    
    state = request.data['state']
    city = request.data['city']
    pincode = request.data['pincode']
    address = request.data['address']

    
    
    branch = request.data['branch']
    active = request.data['active']
    timestamp = request.data['timestamp']

    model=Branch(companyId=companyId, name = name, desc = desc,  phone = phone, email = email, state=state, city=city, pincode=pincode, address=address, branch = branch, active = active, timestamp = timestamp)
    
    model.save()
    return Response({"message":"successful","status":"200","data":[]})

#Branch All API
@api_view(["GET"])
def all(request):
    Branchs_obj = Branch.objects.all() 
    Branch_json = BranchSerializer(Branchs_obj, many=True)
    return Response({"message": "Success","status": 200,"data":Branch_json.data})

#Branch One API
@api_view(["POST"])
def one(request):
    id=request.data['id']
    Branch_obj = Branch.objects.get(id=id)
    Branch_json = BranchSerializer(Branch_obj)
    return Response({"message": "Success","status": 200,"data":[Branch_json.data]})


#Branch Update API
@api_view(['POST'])
def update(request):
    fetchid = request.data['id']
    try:
        model = Branch.objects.get(pk = fetchid)
        model.companyId = request.data['companyId']
        model.name = request.data['name']
        model.desc = request.data['desc']
        model.phone = request.data['phone']
        model.email = request.data['email']

        model.state = request.data['state']
        model.city = request.data['city']
        model.pincode = request.data['pincode']
        model.address = request.data['address']
        model.branch = request.data['branch']
        model.active = request.data['active']
        model.save()
        context = {
            "id":request.data['id'],
            'companyId':request.data['companyId'],
            'name':request.data['name'],
            'desc':request.data['desc'],
            'phone':request.data['phone'],
            'email':request.data['email'],
            'state':request.data['state'],
            'city':request.data['city'],
            'pincode':request.data['pincode'],
            'address':request.data['address'],            
            'branch':request.data['branch'],
            'active':request.data['active']
            }

        return Response({"message":"successful","status":"200","data":[context]})
    except:
        return Response({"message":"ID Wrong","status":"201","data":[]})

#Branch delete
@api_view(['POST'])
def delete(request):
    fetchid=request.data['id']
    try:
        fetchdata=Branch.objects.filter(pk=fetchid).delete()
        return Response({"message":"successful","status":"200","data":[]})
    except:
         return Response({"message":"Id wrong","status":"201","data":[]})

