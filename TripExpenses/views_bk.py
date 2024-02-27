import json
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from Expense.models import Expense
from Expense.serializers import ExpenseSerializer
from BusinessPartner.models import BPEmployee
from BusinessPartner.serializers import BPEmployeeSerializer

from Attachment.models import Attachment
from Attachment.serializers import AttachmentSerializer
import os
from django.core.files.storage import FileSystemStorage

from Employee.models import Employee
from Employee.serializers import EmployeeSerializer
from TripExpenses.models import *
from TripExpenses.serializers import TripExpensesSerializer

#Expense Create API
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def trip_checkin(request):
    try:
        print(request.data)
        BPType = request.data['BPType']
        BPName = request.data['BPName']
        CardCode = request.data['CardCode']
        SalesPersonCode = request.data['SalesPersonCode']
        ModeOfTransport = request.data['ModeOfTransport']
        CheckInDate = request.data['CheckInDate']
        CheckInTime = request.data['CheckInTime']
        CheckInLat = request.data['CheckInLat']
        CheckInLong = request.data['CheckInLong']
        CheckInRemarks = request.data['CheckInRemarks']

        CheckInAttach = request.FILES['CheckInAttach']
        CheckInStatus = 'Start'
        checkinattach_url = ""
        if CheckInAttach:
            target ='./bridge/static/image/TripExpenses'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+CheckInAttach.name, CheckInAttach)
            productImage_url = fss.url(file)
            checkinattach_url = productImage_url.replace('/bridge/', '/')

        TripExpenses( BPType = BPType, BPName = BPName, CardCode = CardCode, SalesPersonCode = SalesPersonCode, ModeOfTransport = ModeOfTransport, CheckInDate = CheckInDate, CheckInTime = CheckInTime, CheckInLat = CheckInLat, CheckInLong = CheckInLong, CheckInAttach = checkinattach_url, CheckInRemarks = CheckInRemarks, CheckInStatus = CheckInStatus).save()
        objTripExp = TripExpenses.objects.latest("id")
        return Response({"message": "successful", "status": "200", "data": [{ "id": objTripExp.id }]})
    except Exception as e:
        return Response({"message": str(e), "status": "201", "data": []})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Expense Create API
@api_view(['POST'])
def trip_checkout(request):
    try:
        Tripid = request.data['id']
        if TripExpenses.objects.filter(pk = Tripid).exists():
            CheckOutAttach = request.data['CheckOutAttach']
            SalesPersonCode = request.data['SalesPersonCode']
            CheckInStatus = 'Stop'
            tripModel = TripExpenses.objects.get(pk = Tripid)
            tripModel.CheckOutDate = request.data['CheckOutDate']
            tripModel.CheckOutTime = request.data['CheckOutTime']
            tripModel.CheckOutLat = request.data['CheckOutLat']
            tripModel.CheckOutLong = request.data['CheckOutLong']
            tripModel.CheckOutRemarks = request.data['CheckOutRemarks']
            tripModel.TotalDistanceAuto = request.data['TotalDistanceAuto']
            tripModel.TotalDistanceManual = request.data['TotalDistanceManual']
            tripModel.TotalExpenses = request.data['TotalExpenses']
            tripModel.CheckInStatus = CheckInStatus
            
            checkoutattach_url = ""
            if CheckOutAttach !="" :
                target ='./bridge/static/image/TripExpenses'
                os.makedirs(target, exist_ok=True)
                fss = FileSystemStorage()
                file = fss.save(target+"/"+CheckOutAttach.name, CheckOutAttach)
                productImage_url = fss.url(file)
                checkoutattach_url = productImage_url.replace('/bridge/', '/')
                tripModel.CheckOutAttach = checkoutattach_url
            tripModel.save()

            return Response({"message": "successful", "status": "200", "data": []})
        else:
            return Response({"message": "Invalid Trip Id", "status": "201", "data": []})
    except Exception as e:
        return Response({"message": str(e), "status": "201", "data": []})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['GET'])
def all_tripexpenses(request):
    try:
        tripObj = TripExpenses.objects.all().order_by("-id")
        tripJson = TripExpensesSerializer(tripObj, many=True)
        return Response({"message": "successful", "status": "200", "data": tripJson.data})
    except Exception as e:
        return Response({"message": str(e), "status": "201", "data": []})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def one_tripexpenses(request):
    try:
        TripId = request.data['id']
        if TripExpenses.objects.filter(pk = TripId).exists():
            tripObj = TripExpenses.objects.filter(pk = TripId).order_by("-id").first()
            tripJson = TripExpensesSerializer(tripObj, many=False)
            return Response({"message": "successful", "status": "200", "data": [tripJson.data]})
        else:
            return Response({"message": "Invalid id?", "status": "201", "data": []})
    except Exception as e:
        return Response({"message": str(e), "status": "201", "data": []})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def all_filter_tripexpenses(request):
    try:
        SalesPersonCode = request.data['SalesPersonCode']
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        if Employee.objects.filter(SalesEmployeeCode = SalesPersonCode).exists():
            tripObj = "" 
            if str(FromDate) != "":
                tripObj = TripExpenses.objects.filter(SalesPersonCode = SalesPersonCode, CheckInDate__gte = FromDate, CheckInDate__lte = ToDate).order_by("-id")
            else:
                tripObj = TripExpenses.objects.filter(SalesPersonCode = SalesPersonCode).order_by("-id")
            tripJson = TripExpensesSerializer(tripObj, many=True)
            return Response({"message": "successful", "status": "200", "data": tripJson.data})
        else:
            return Response({"message": "Invalid SalesEmployeeCode?", "status": "201", "data": []})
    except Exception as e:
        return Response({"message": str(e), "status": "201", "data": []})