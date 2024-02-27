from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from .forms import BPDepartment
from .models import BPDepartment
import requests, json

from django.contrib import messages

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import BPDepartmentSerializer
from rest_framework.parsers import JSONParser
# Create your views here.  

#BPDepartment Create API
@api_view(['POST'])
def create(request):
    
    Name = request.data['Name']
    Description = request.data['Description']

    model = BPDepartment(Name=Name, Description=Description)

    model.save()    
    dep = BPDepartment.objects.latest('id')

    with open("../bridge/bridge/db.json") as f:
        db = f.read()
        data = json.loads(db)

    r = requests.post('http://103.107.67.94:50001/b1s/v1/Login', data=json.dumps(data), verify=False)
    token = json.loads(r.text)['SessionId']
    print(token)

    dep_data = {
                "Name": request.data['Name'],
                "Description": request.data['Description']
                }

    res = requests.post('http://103.107.67.94:50001/b1s/v1/Departments', data=json.dumps(dep_data), cookies=r.cookies, verify=False)

    live = json.loads(res.text)

    fetchid = dep.id

    if "Code" in live:
        print(live['Code'])
        
        model = BPDepartment.objects.get(pk = fetchid)
        model.Code = live['Code']
        model.save()
        
        return Response({"message":"successful","status":200,"data":[{"id":dep.id, "Code":live['Code']}]})
    else:
        SAP_MSG = live['error']['message']['value']
        print(SAP_MSG)
        if "already exists" in SAP_MSG:
            fetchdata=BPDepartment.objects.filter(pk=fetchid).delete()
            return Response({"message":"Not created","SAP_error":SAP_MSG, "status":202,"data":[]})
        else:
            return Response({"message":"Partely successful","SAP_error":SAP_MSG, "status":202,"data":[]})

#BPDepartment All API
@api_view(["GET"])
def all(request):    
    bpdepartment_obj = BPDepartment.objects.all() 
    bpdepartment_json = BPDepartmentSerializer(bpdepartment_obj, many=True)
    return Response({"message": "Success","status": 200,"data":bpdepartment_json.data})


#BPDepartment One API
@api_view(["POST"])
def one(request):
    id=request.data['id']
    bpdepartment_obj = BPDepartment.objects.get(id=id)
    bpdepartment_json = BPDepartmentSerializer(bpdepartment_obj)
    return Response({"message": "Success","status": 200,"data":[bpdepartment_json.data]})

#BPDepartment Update API
@api_view(['POST'])
def update(request):
    fetchid = request.data['id']
    try:
        model = BPDepartment.objects.get(pk = fetchid)
        model.Name = request.data['Name']
        model.Description = request.data['Description']
        model.save()

        context = {
            'id':request.data['id'],
            'Name':request.data['Name'],
            'Description':request.data['Description']
            }
            
        with open("../bridge/bridge/db.json") as f:
            db = f.read()
            print(db)
        data = json.loads(db)

        r = requests.post('http://103.107.67.94:50001/b1s/v1/Login', data=json.dumps(data), verify=False)
        token = json.loads(r.text)['SessionId']
        print(token)
        
        dep_data = {
            'Name':request.data['Name'],
            'Description':request.data['Description']
        }
        
        print(dep_data)
        

        print('http://103.107.67.94:50001/b1s/v1/Departments('+model.Code+')');
    
        res = requests.patch('http://103.107.67.94:50001/b1s/v1/Departments('+model.Code+')', data=json.dumps(dep_data), cookies=r.cookies, verify=False)
        
        if len(res.content) !=0 :
            res1 = json.loads(res.content)
            SAP_MSG = res1['error']['message']['value']
            return Response({"message":"Partely successful","status":"202","SAP_error":SAP_MSG, "data":[context]})
        else:
            return Response({"message":"successful","status":"200", "data":[context]})
    except:
        return Response({"message":"ID Wrong","status":"201","data":[context]})


#BPDepartment delete
@api_view(['POST'])
def delete(request):
    fetchid=request.data['id']
    try:
        dep=BPDepartment.objects.get(pk=fetchid)
        Code = dep.Code
        
        fetchdata=BPDepartment.objects.filter(pk=fetchid).delete()
        
        with open("../bridge/bridge/db.json") as f:
            db = f.read()
        print(db)
        data = json.loads(db)
        print(data)
    
        try:
            r = requests.post('http://103.107.67.94:50001/b1s/v1/Login', data=json.dumps(data), verify=False)
            token = json.loads(r.text)['SessionId']
            print(token)
            print('http://103.107.67.94:50001/b1s/v1/Departments('+Code+')')
            res = requests.delete('http://103.107.67.94:50001/b1s/v1/Departments('+Code+')', cookies=r.cookies, verify=False)
            print(res.content)
            return Response({"message":"successful","status":"200","data":[]})
        except:
            return Response({"message":"successful","status":"200","data":[]})        
    except:
         return Response({"message":"Id wrong","status":"201","data":[]})

