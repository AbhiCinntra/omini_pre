from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
import requests, json

from django.contrib import messages

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from Attachment.models import Attachment
from Attachment.serializers import AttachmentSerializer
import os
from django.core.files.storage import FileSystemStorage
from Payment.models import Payment
from Payment.serializers import PaymentSerializer
from BusinessPartner.models import BPEmployee
from BusinessPartner.serializers import BPEmployeeSerializer

from Invoice.models import Invoice
from Invoice.serializers import InvoiceSerializer
# Create your views here.  

#Payment Create API
@api_view(['POST'])
def create(request):
    try:
        InvoiceNo = request.data['InvoiceNo']
        TransactId = request.data['TransactId']
        TotalAmt = request.data['TotalAmt']
        TransactMod = request.data['TransactMod'] 
        DueAmount = request.data['DueAmount']
        PaymentDate = request.data['PaymentDate']
        ReceivedAmount = request.data['ReceivedAmount'] 
        Remarks = request.data['Remarks']
        createTime = request.data['createTime']
        createdBy = request.data['createdBy']
        createDate = request.data['createDate']
        
        CardCode = request.data['CardCode']
        
        Attach = request.data['Attach']  
        
        model = Payment(InvoiceNo=InvoiceNo, TransactId=TransactId, TotalAmt=TotalAmt, TransactMod=TransactMod, DueAmount=DueAmount, PaymentDate=PaymentDate, ReceivedAmount=ReceivedAmount, Remarks = Remarks, createTime=createTime, createdBy=createdBy, createDate=createDate, CardCode=CardCode)
        
        model.save()
        
        PaymentID = Payment.objects.latest('id')
        
        for File in request.FILES.getlist('Attach'):
            attachmentsImage_url = ""
            target ='./bridge/static/image/Payment'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+File.name, File)
            productImage_url = fss.url(file)
            attachmentsImage_url = productImage_url.replace('/bridge', '')
            
            print(attachmentsImage_url)

            att=Attachment(File=attachmentsImage_url, LinkType="Payment", LinkID=PaymentID.id, CreateDate=model.updateDate, CreateTime=model.updateTime)
        
            att.save()
        return Response({"message":"successful","status":200,"data":[]})        

    except Exception as e:
        return Response({"message":"Error","status":201,"data":[{"Error":str(e)}]})


#Payment All API
@api_view(["GET"])
def all(request):
    try:
        payment_obj = Payment.objects.all().order_by("-id")
        result = showPayment(payment_obj)
        return Response({"message": "Success","status": 200,"data":result})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

#Payment One API
@api_view(["POST"])
def one(request):
    try:
        id = request.data['id']
        if Payment.objects.filter(pk=id).exists():
            pay_obj = Payment.objects.filter(pk=id)
            result = showPayment(pay_obj)
            return Response({"message": "Success","status": 200,"data":result})
        else:
            return Response({"message": "Id Doesn't Exist", "status": 201, "data": []})
    except Exception as e:
        return Response({"message": str(e), "status": 201, "data": []})

#Payment Data for all payments and one payment
def showPayment(objs):
    allPayment = [];
    for obj in objs:
        createPerson = obj.createdBy  
        updatePerson = obj.updatedBy  
        cc = obj.CardCode
        
        pay_json = PaymentSerializer(obj)
        finalPayData = json.loads(json.dumps(pay_json.data))
            
        if createPerson > 0:
            createPersonObj = BPEmployee.objects.filter(pk = createPerson).values("FirstName", "MiddleName","LastName")
            createPersonjson = BPEmployeeSerializer(createPersonObj, many=True)
            if len(createPersonjson.data) > 0:
                finalPayData['createdBy'] = [json.loads(json.dumps(createPersonjson.data[0]))]   
            else:
                finalPayData['createdBy'] = []
        else:
            finalPayData['createdBy'] = []
            
        if updatePerson > 0:
            updatePersonObj = BPEmployee.objects.filter(pk = updatePerson).values("FirstName", "MiddleName","LastName")
            updatePersonjson = BPEmployeeSerializer(updatePersonObj, many=True)
            if len(updatePersonjson.data) > 0:
                finalPayData['updatedBy'] = [json.loads(json.dumps(updatePersonjson.data[0]))]
            else:
                finalPayData['updatedBy'] = []
        else:
            finalPayData['updatedBy'] = []
            
        if Attachment.objects.filter(LinkID = obj.id, LinkType="Payment").exists():
            Attach_dls = Attachment.objects.filter(LinkID = obj.id, LinkType="Payment")
            Attach_json = AttachmentSerializer(Attach_dls, many=True)
            finalPayData['Attach'] = Attach_json.data
        else:
            finalPayData['Attach'] = []
            
        # if cc !="":
            # ccObj = Invoice.objects.filter(CardCode = cc).values('CardCode')
            # ccjson = InvoiceSerializer(ccObj, many=True)
            # if len(ccjson.data) > 0:
                # finalPayData['CardCode'] = json.loads(json.dumps(ccjson.data[0]))
            # else:
                # finalPayData['CardCode'] = []
        # else:
            # finalPayData['CardCode'] = []
        
        allPayment.append(finalPayData)
    return allPayment

#Payment Update API
@api_view(['POST'])
def update(request):
    try:
        fetchid = request.data['id']
        model = Payment.objects.get(pk = fetchid)
        model.InvoiceNo = request.data['InvoiceNo']
        model.TransactId = request.data['TransactId']
        model.TotalAmt = request.data['TotalAmt']
        model.TransactMod = request.data['TransactMod'] 
        model.DueAmount = request.data['DueAmount']
        model.PaymentDate = request.data['PaymentDate']
        model.ReceivedAmount = request.data['ReceivedAmount'] 
        model.Remarks = request.data['Remarks']
        model.updateDate = request.data['updateDate']
        model.updateTime = request.data['updateTime']
        model.updatedBy = request.data['updatedBy']
        model.CardCode = request.data['CardCode']
        
        Attach = request.data['Attach']  
        for File in request.FILES.getlist('Attach'):
            attachmentsImage_url = ""
            target ='./bridge/static/image/Payment'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+File.name, File)
            productImage_url = fss.url(file)
            attachmentsImage_url = productImage_url.replace('/bridge', '')
            
            print(attachmentsImage_url)

            att=Attachment(File=attachmentsImage_url, LinkType="Payment", LinkID=fetchid, CreateDate=model.updateDate, CreateTime=model.updateTime)
        
            att.save()

        model.save()

        return Response({"message":"successful","status":200,"data":[]})
    except:
        return Response({"message":"ID Wrong","status":201,"data":[]})
    
#Payment delete
@api_view(['POST'])
def delete(request):
    try:
        fetchids= request.data['id']
        for ids in fetchids:
            if Payment.objects.filter(pk=ids).exists():
                Payment.objects.filter(pk=ids).delete()
            else:
                return Response({"message":"Id Doesn't Exist","status":"405","data":[]}) 
        return Response({"message":"successful","status":"200","data":[]})   
    except:
        return Response({"message":"Id wrong","status":"201","data":[]})

#Payment Image Delete API
@api_view(['POST'])
def payment_img_delete(request):
    pay_id= request.data['id']
    
    image_id = request.data['image_id']
    
    try:
        if Attachment.objects.filter(pk=image_id , LinkID=pay_id).exists():
            Attachment.objects.filter(pk=image_id, LinkID=pay_id).delete()
            
            return Response({"message":"successful","status":"200","data":[]})        
        else:
            return Response({"message":"Id Not Found","status":"201","data":[]})        
    except:
        return Response({"message":"Id wrong","status":"201","data":[]})

