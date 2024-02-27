from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from .forms import BPEmployee  
from .models import BPEmployee  
import requests, json

from django.contrib import messages

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import BPEmployeeSerializer
from rest_framework.parsers import JSONParser
# Create your views here.

# import setting file
from django.conf import settings
from django.db.models import Q

#BPEmployee Create API
@api_view(['POST'])
def create(request):
    try:
        Title = request.data['Title']
        FirstName = request.data['FirstName']
        MiddleName = request.data['MiddleName']
        LastName = request.data['LastName']
        Position = request.data['Position']
        Address = request.data['Address']
        MobilePhone = request.data['MobilePhone']
        Fax = request.data['Fax']
        E_Mail = request.data['E_Mail']
        Remarks1 = request.data['Remarks1']
        DateOfBirth = request.data['DateOfBirth']
        Gender = request.data['Gender']
        Profession = request.data['Profession']
        CardCode = request.data['CardCode']
        
        U_BPID = request.data['U_BPID']
        U_BRANCHID = "1" #request.data['U_BRANCHID']
        U_NATIONALTY = request.data['U_NATIONALTY']
        
        CreateDate = request.data['CreateDate']
        CreateTime = request.data['CreateTime']
        UpdateDate = request.data['UpdateDate']
        UpdateTime = request.data['UpdateTime']
        
        if BPEmployee.objects.filter(CardCode=CardCode, FirstName=FirstName).exists():
            return Response({"message":"Contact Person already exists","status":201,"data":[]})
        else:
            model = BPEmployee(U_BRANCHID=U_BRANCHID, U_BPID=U_BPID, CardCode=CardCode, Title=Title, FirstName=FirstName, MiddleName=MiddleName, LastName=LastName, Position=Position, Address=Address, MobilePhone=MobilePhone, Fax=Fax, E_Mail=E_Mail, Remarks1=Remarks1, U_NATIONALTY=U_NATIONALTY, DateOfBirth=DateOfBirth, Gender=Gender, Profession=Profession, CreateDate=CreateDate, CreateTime=CreateTime, UpdateDate=UpdateDate, UpdateTime=UpdateTime)

            model.save()    
            em = BPEmployee.objects.latest('id')

            ename = str(str(request.data['FirstName'])+" "+str(request.data['MiddleName'])+" "+str(request.data['LastName']))
            ename = ename.replace("  "," ")
            em_data = {
                "ContactEmployees": [
                    {
                        "Name": ename,
                        "FirstName": request.data['FirstName'],
                        "MiddleName": request.data['MiddleName'],
                        "LastName": request.data['LastName'],
                        "E_Mail": request.data['E_Mail'],
                        "Position": request.data['Position'],
                        "MobilePhone": request.data['MobilePhone'],
                        "Address": request.data['Address'],
                        "Profession": request.data['Profession']
                    }
                ]
            }
            print(em_data)
                
            res = settings.CALLAPI('patch', "/BusinessPartners('"+CardCode+"')", 'api', em_data)
            
            if len(res.content) !=0 :
                res1 = json.loads(res.content)
                SAP_MSG = res1['error']['message']['value']
                return Response({"message":"Partely successful","status":202,"SAP_error":SAP_MSG, "data":[{"em_data": em_data}]})
            else:
                bpres = settings.CALLAPI('get', "/BusinessPartners('"+CardCode+"')", 'api', em_data)
                
                bpres1 = json.loads(bpres.content)
                lastbp = len(bpres1['ContactEmployees']) - 1
                InternalCode = bpres1['ContactEmployees'][lastbp]['InternalCode']
                
                bpmodel = BPEmployee.objects.get(id=em.id)
                bpmodel.InternalCode = InternalCode
                bpmodel.save()

            return Response({"message":"successful","status":200, "data":[{"id":em.id,"InternalCode":InternalCode,"em_data": em_data}]})

    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})

#BPEmployee All API
@api_view(["POST"])
def all(request):    
    CardCode=request.data['CardCode']
    bpemployee_obj = BPEmployee.objects.filter(CardCode=CardCode) 
    bpemployee_json = BPEmployeeSerializer(bpemployee_obj, many=True)
    return Response({"message": "Success","status": 200,"data":bpemployee_json.data})


#BPEmployee One API
@api_view(["POST"])
def one(request):
    id=request.data['id']
    bpemployee_obj = BPEmployee.objects.get(id=id)
    bpemployee_json = BPEmployeeSerializer(bpemployee_obj)
    return Response({"message": "Success","status": 200,"data":[bpemployee_json.data]})

#BPEmployee Update API
@api_view(['POST'])
def update(request):
    try:
        fetchid = request.data['id']
        model = BPEmployee.objects.get(pk = fetchid)
        
        model.Title = request.data['Title']
        model.FirstName = request.data['FirstName']
        model.MiddleName = request.data['MiddleName']
        model.LastName = request.data['LastName']
        model.Position = request.data['Position']
        model.Address = request.data['Address']
        model.MobilePhone = request.data['MobilePhone']
        model.Fax = request.data['Fax']
        model.E_Mail = request.data['E_Mail']
        model.Remarks1 = request.data['Remarks1']
        model.DateOfBirth = request.data['DateOfBirth']
        model.Gender = request.data['Gender']
        model.Profession = request.data['Profession']
        model.CardCode = request.data['CardCode']
        model.U_BPID = request.data['U_BPID']
        model.U_BRANCHID = "1", #request.data['U_BRANCHID']
        model.U_NATIONALTY = request.data['U_NATIONALTY']
        # model.CreateDate = request.data['CreateDate']
        # model.CreateTime = request.data['CreateTime']
        # model.UpdateDate = request.data['UpdateDate']
        # model.UpdateTime = request.data['UpdateTime']

        model.save()
        ename = str(str(request.data['FirstName'])+" "+str(request.data['MiddleName'])+" "+str(request.data['LastName']))
        ename = ename.replace("  "," ")

        em_data = {
            "CardCode":request.data['CardCode'],
            "ContactEmployees": [
                {
                    'Title':request.data['Title'],
                    "Name": ename,
                    'FirstName':request.data['FirstName'],
                    'MiddleName':request.data['MiddleName'],
                    'LastName':request.data['LastName'],
                    'Position':request.data['Position'],
                    'Address':request.data['Address'],
                    'MobilePhone':request.data['MobilePhone'],
                    'Fax':request.data['Fax'],
                    'E_Mail':request.data['E_Mail'],
                    'Remarks1':request.data['Remarks1'],
                    'InternalCode':request.data['InternalCode'],
                    'DateOfBirth':request.data['DateOfBirth'],
                    'Gender':'M',
                    'Profession':request.data['Profession'],
                    'CardCode':request.data['CardCode']
                    # 'CreateDate':request.data['CreateDate'],
                    # 'CreateTime':request.data['CreateTime'],
                    # 'UpdateDate':request.data['UpdateDate'],
                    # 'UpdateTime':request.data['UpdateTime']
                }
            ]
        }
        
        res = settings.CALLAPI('patch', "/BusinessPartners('"+model.CardCode+"')", 'api', em_data)
        
        if len(res.content) !=0 :
            res1 = json.loads(res.content)
            SAP_MSG = res1['error']['message']['value']
            return Response({"message":"Partely successful","status":"202","SAP_error":SAP_MSG, "data":[]})
        else:
            return Response({"message":"successful","status":"200", "data":[]})
        
        # return Response({"message":"successful","status":"200", "data":[request.data]})
    except Exception as e:
            return Response({"message":str(e),"status":"201","data":[]})

#BPEmployee delete
@api_view(['POST'])
def delete(request):
    try:
        fetchid=request.data['id']
        fetchdata=BPEmployee.objects.filter(pk=fetchid).delete()
        return Response({"message":"successful","status":"200","data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})
