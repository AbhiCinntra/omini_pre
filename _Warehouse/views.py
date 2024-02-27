from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from .models import *
from Employee.models import Employee

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


# Create your views here.  

#Warehouse Create API
@api_view(['POST'])
def create(request):
    if Warehouse.objects.filter(Name=request.data['Name']).exists():
        return Response({"message":"Already exist Name","status":"409","data":[]})
    else:
        try:
            Name = request.data['Name']
            Address = request.data['Address']
            City = request.data['City']
            State = request.data['State']
            Pin = request.data['Pin']
            Country = request.data['Country']
            Status = request.data['Status']
            CreatedDate = request.data['CreatedDate']
            CreatedTime = request.data['CreatedTime']
            UpdatedDate = request.data['UpdatedDate']
            UpdatedTime = request.data['UpdatedTime']
            
            model = Warehouse(Name = Name, Address = Address, City = City, State = State, Pin = Pin, Country = Country, Status = Status, CreatedDate = CreatedDate, CreatedTime = CreatedTime, UpdatedDate = UpdatedDate, UpdatedTime = UpdatedTime)
            
            model.save()
            w = Warehouse.objects.latest('id')
            return Response({"message":"successful","status":200,"data":[{"id":w.id}]})
        except Exception as e:
            return Response({"message":"Not Created","status":201,"data":[{"Error":str(e)}]})

#Warehouse Update API
@api_view(['POST'])
def update(request):
    fetchid = request.data['id']
    try:
        model = Warehouse.objects.get(pk = fetchid)

        model.Name = request.data['Name']
        model.Address = request.data['Address']
        model.City = request.data['City']
        model.State = request.data['State']
        model.Pin = request.data['Pin']
        model.Country = request.data['Country']
        model.Status = request.data['Status']
        model.CreatedDate = request.data['CreatedDate']
        model.CreatedTime = request.data['CreatedTime']
        model.UpdatedDate = request.data['UpdatedDate']
        model.UpdatedTime = request.data['UpdatedTime']
        model.save()
        
        return Response({"message":"successful","status":200, "data":[request.data]})
    except Exception as e:
        return Response({"message":"Not Update","status":201,"data":[{"Error":str(e)}]})

#Warehouse All API
@api_view(["GET"])
def all(request):
    Warehouses_obj = Warehouse.objects.all().order_by("-id")
    allwr = WarehouseSerializer(Warehouses_obj, many=True)
    return Response({"message": "Success","status": 200,"data":allwr.data})


#Warehouse One API
@api_view(["POST"])
def one(request):
    id=request.data['id']    
    Warehouses_obj = Warehouse.objects.get(id=id)    
    allwr = WarehouseSerializer(Warehouses_obj, many=False)
    return Response({"message": "Success","status": 200,"data":allwr.data})

#Warehouse delete
@api_view(['POST'])
def delete(request):
    fetchid=request.data['id']
    try:
        fetchdata=Warehouse.objects.filter(pk=fetchid).delete()
        return Response({"message":"successful","status":"200","data":[]})        
    except:
         return Response({"message":"Id wrong","status":"201","data":[]})


#Inventory Create API
@api_view(['POST'])
def inventory_create(request):
    try:
        ItemCode = request.data['ItemCode']
        WarehouseID = request.data['WarehouseID']
        Add = int(request.data['Add'])
        Remove = int(request.data['Remove'])
        Type = request.data['Type']
        Emp = request.data['Emp']
        Remark = request.data['Remark']
        CreatedDate = request.data['CreatedDate']
        CreatedTime = request.data['CreatedTime']
        
        if Add > 0 and Remove > 0:
            return Response({"message":"successful","status":201,"data":[{"Error":"Please select one Add or Remove"}]})
        
        Inventory_obj = Inventory.objects.filter(ItemCode=ItemCode, WarehouseID=WarehouseID).order_by("-id")[:1]
        if len(Inventory_obj) < 1:
            invt = 0
        else:
            for inv in Inventory_obj:
                invt = inv.Inventory
            
        if Remove > invt:
            msg = "Inventory should be less than stock: Inventory:"+str(invt)+" and Remove:"+str(Remove)
        
            return Response({"message":msg, "status":201, "data":[]})
        
        if Add > 0:
            invt = invt + Add
        elif Remove > 0:
            invt = invt - Remove            
        else:
            return Response({"message":"successful","status":201,"data":[{"Error":"Something went wrong"}]})
        
        model = Inventory(ItemCode = ItemCode, WarehouseID = WarehouseID, Add = Add, Remove = Remove, Inventory = invt, Type = Type, Emp  = Emp, Remark = Remark, CreatedDate = CreatedDate, CreatedTime = CreatedTime)        
        model.save()
        
        invt_obj = Inventory.objects.latest('id')
        print(invt_obj.Inventory)
        
        return Response({"message":"successful","status":200,"data":[{"Inventory":invt_obj.Inventory}]})
    except Exception as e:
        return Response({"message":"Not Created","status":201,"data":[{"Error":str(e)}]})

#Inventory All API
@api_view(["POST"])
def inventory_one(request):
    ItemCode = request.data['ItemCode']
    WarehouseID = request.data['WarehouseID']
    Inventory_obj = Inventory.objects.filter(ItemCode=ItemCode, WarehouseID=WarehouseID).order_by("-id")[:1]
    inv = InventorySerializer(Inventory_obj, many=True)
    return Response({"message": "Success","status": 200,"data":inv.data})
