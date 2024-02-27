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

#Expense Create API
@api_view(['POST'])
def create(request):
    try:
        trip_name = request.data['trip_name']
        type_of_expense = request.data['type_of_expense']
        expense_from = request.data['expense_from']
        expense_to = request.data['expense_to']
        totalAmount = request.data['totalAmount']
        createDate = request.data['createDate']
        createTime = request.data['createTime']
        createdBy = request.data['createdBy']
        remarks = request.data['remarks']
        employeeId = request.data['employeeId']
        
        Attach = request.data['Attach']

        startLat = ""
        startLong = ""
        endLat = ""
        endLong = ""
        travelDistance = ""
        if 'startLat' in request.data:
            startLat = request.data['startLat']
            startLong = request.data['startLong']
            endLat = request.data['endLat']
            endLong = request.data['endLong']
            travelDistance = request.data['travelDistance']
        
        
        model = Expense(remarks=remarks, trip_name=trip_name, type_of_expense=type_of_expense, expense_from=expense_from, expense_to=expense_to, totalAmount=totalAmount, createDate=createDate, createTime=createTime, createdBy=createdBy, employeeId = employeeId, startLat = startLat, startLong = startLong, endLat = endLat, endLong = endLong, travelDistance = travelDistance)

        model.save()
        
        ExpenseID = Expense.objects.latest('id')
        
        print(request.FILES.getlist('Attach'))
        for File in request.FILES.getlist('Attach'):
            attachmentsImage_url = ""
            target ='./bridge/static/image/Expense'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+File.name, File)
            productImage_url = fss.url(file)
            attachmentsImage_url = productImage_url.replace('/bridge', '')
            
            print(attachmentsImage_url)

            att=Attachment(File=attachmentsImage_url, LinkType="Expense", LinkID=ExpenseID.id, CreateDate=createDate, CreateTime=createTime)
        
            att.save()
        
        return Response({"message": "successful", "status": "200", "data": []})
    except Exception as e:
        return Response({"message": str(e), "status": "201", "data": []})

#Expense All API
@api_view(["GET"])
def all(request):
    expn_obj = Expense.objects.all().order_by("-id")
    result = showExpense(expn_obj)
    return Response({"message": "Success","status": 200,"data":result})

#Expense One API
@api_view(["POST"])
def one(request):
    try:
        id = request.data['id']
        if Expense.objects.filter(pk=request.data['id']).exists():
            expn_obj = Expense.objects.filter(pk=request.data['id'])
            result = showExpense(expn_obj)
            return Response({"message": "Success","status": 200,"data":result})
        else:
            return Response({"message": "Id Doesn't Exist", "status": 201, "data": []})
    except Exception as e:
        return Response({"message": str(e), "status": 201, "data": []})

#Expense Update API
@api_view(['POST'])
def update(request):
    try:
        fetchid = request.data['id']
        model = Expense.objects.get(pk = fetchid)
        model.remarks = request.data['remarks']
        model.trip_name = request.data['trip_name']
        model.type_of_expense = request.data['type_of_expense']
        model.expense_from = request.data['expense_from']
        model.expense_to = request.data['expense_to']
        model.totalAmount = request.data['totalAmount']
        model.updateDate = request.data['updateDate']
        model.updateTime = request.data['updateTime']
        model.updatedBy = request.data['updatedBy']
        model.employeeId = request.data['employeeId']
        
        Attach = request.data['Attach']  
        for File in request.FILES.getlist('Attach'):
            attachmentsImage_url = ""
            target ='./bridge/static/image/Expense'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+File.name, File)
            productImage_url = fss.url(file)
            attachmentsImage_url = productImage_url.replace('/bridge', '')
            
            print(attachmentsImage_url)

            att=Attachment(File=attachmentsImage_url, LinkType="Expense", LinkID=fetchid, CreateDate=model.updateDate, CreateTime=model.updateTime)
        
            att.save()

        model.save()

        return Response({"message":"successful","status":200,"data":[]})
    except:
        return Response({"message":"ID Wrong","status":201,"data":[]})
    
#Expense Delete API
@api_view(['POST'])
def delete(request):
    fetchids= request.data['id']
    try:
        for ids in fetchids:
            Expense.objects.filter(pk=ids).delete()
            
        return Response({"message":"successful","status":"200","data":[]})   
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})

#Expense Data for all expenses and one expense
def showExpense(objs):
    allexpn = [];
    for obj in objs:
        createPerson = obj.createdBy  
        updatePerson = obj.updatedBy  
        employeePer = obj.employeeId  
        
        expn_json = ExpenseSerializer(obj)
        finalExpnData = json.loads(json.dumps(expn_json.data))
            
        if Employee.objects.filter(pk = createPerson).exists():
            createPersonObj = Employee.objects.filter(pk = createPerson).values('id','firstName', 'lastName')
            createPersonjson = EmployeeSerializer(createPersonObj, many=True)
            finalExpnData['createdBy'] = createPersonjson.data
        else:
            finalExpnData['createdBy'] = []
            
        if Employee.objects.filter(pk = updatePerson).exists():
            updatePersonObj = Employee.objects.filter(pk = updatePerson).values('id','firstName', 'lastName')
            updatePersonjson = EmployeeSerializer(updatePersonObj, many=True)
            finalExpnData['updatedBy'] = updatePersonjson.data
        else:
            finalExpnData['updatedBy'] = []
            
        if Attachment.objects.filter(LinkID = obj.id, LinkType="Expense").exists():
            Attach_dls = Attachment.objects.filter(LinkID = obj.id, LinkType="Expense")
            Attach_json = AttachmentSerializer(Attach_dls, many=True)
            finalExpnData['Attach'] = Attach_json.data
        else:
            finalExpnData['Attach'] = []
            
        if Employee.objects.filter(pk = employeePer).exists():
            employeePerObj = Employee.objects.filter(pk = employeePer).values('id','firstName', 'lastName')
            employeePerjson = EmployeeSerializer(employeePerObj, many=True)
            finalExpnData['employeeId'] = employeePerjson.data
        else:
            finalExpnData['employeeId'] = []
        
        allexpn.append(finalExpnData)
    return allexpn

#Expense Delete API
@api_view(['POST'])
def expense_img_delete(request):
    expense_id= request.data['id']
    
    image_id = request.data['image_id']
    
    try:
        if Attachment.objects.filter(pk=image_id , LinkID=expense_id).exists():
            Attachment.objects.filter(pk=image_id, LinkID=expense_id).delete()
            
            return Response({"message":"successful","status":"200","data":[]})        
        else:
            return Response({"message":"Id Not Found","status":"201","data":[]})        
    except:
        return Response({"message":"Id wrong","status":"201","data":[]})
