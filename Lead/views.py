import json
from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse

from Employee.serializers import EmployeeSerializer
from global_methods import getAllReportingToUserId
from .forms import LeadForm  
from .models import *
from Employee.models import Employee  

from django.contrib import messages

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import *
from rest_framework.parsers import JSONParser

#added by millan for multi image store on 26-09-2022
from Attachment.models import Attachment
from Attachment.serializers import AttachmentSerializer
import os
from django.core.files.storage import FileSystemStorage
#added by millan for multi image store on 26-09-2022

from django.db.models import Q #updated by millan on 07-10-2022

# Create your views here.  

#Lead Create API
@api_view(['POST'])
def create(request):
    try:
        leads = request.data
        log = []
        
        for lead in leads:
            date=lead['date']
            location=lead['location']
            companyName=lead['companyName']
            numOfEmployee = lead['numOfEmployee']
            turnover = lead['turnover']
            source=lead['source']
            contactPerson=lead['contactPerson']
            designation=lead['designation']
            phoneNumber=lead['phoneNumber']
            message=lead['message']
            email=lead['email']
            status=lead['status']
            leadType=lead['leadType']
            productInterest=lead['productInterest']
            assignedTo_id=lead['assignedTo']
            employeeId_id=lead['employeeId']
            timestamp=lead['timestamp']

            projectAmount = lead['projectAmount']
            customerType = lead['customerType']
            stages = lead['stages']

            U_LAT = lead['U_LAT']
            U_LONG = lead['U_LONG']
            
            #added by millan on 26-September-2022 for image upload
            Attach = lead['Attach'] 
            Caption = lead['Caption']
            
            if Lead.objects.filter(phoneNumber=phoneNumber).exists():
                log.append(phoneNumber)
            else:
                model=Lead(date=date, location=location, companyName=companyName, numOfEmployee=numOfEmployee, turnover=turnover, source=source, status=status, leadType=leadType, contactPerson=contactPerson, designation=designation, phoneNumber=phoneNumber, message=message, email=email, productInterest=productInterest, assignedTo_id=assignedTo_id, employeeId_id=employeeId_id, timestamp=timestamp, projectAmount = projectAmount, customerType = customerType, stages = stages, U_LAT = U_LAT, U_LONG = U_LONG)
                model.save()
                
                # for multi image upload added by millan on 26-09-2022
                LeadID = Lead.objects.latest('id')
                
                date_time = (timestamp.strip()).split(" ")
                
                print(request.FILES.getlist('Attach'))
                for File in request.FILES.getlist('Attach'):
                    attachmentsImage_url = ""
                    target ='./bridge/static/image/Attachment'
                    os.makedirs(target, exist_ok=True)
                    fss = FileSystemStorage()
                    file = fss.save(target+"/"+File.name, File)
                    productImage_url = fss.url(file)
                    attachmentsImage_url = productImage_url.replace('/bridge', '')
                    
                    print(attachmentsImage_url)

                    att=Attachment(File=attachmentsImage_url, Caption=Caption, LinkType="Lead", LinkID=LeadID.id, CreateDate=leads['date'], CreateTime=date_time[1]+ " " + date_time[2], UpdateDate=leads['date'], UpdateTime=date_time[1]+ " " + date_time[2])
                    att=Attachment(File=attachmentsImage_url, Caption=Caption, LinkType="Lead", LinkID=LeadID.id, CreateDate=leads['date'], CreateTime=date_time[1]+ " " + date_time[2], UpdateDate=leads['date'], UpdateTime=date_time[1]+ " " + date_time[2])
                
                    att.save()
                
                
            print(log)
            if len(log) > 0:
                log_msg = "Mobile number is already exist: "+str(log)
            else:
                log_msg = 'successful'
        return Response({"message":log_msg,"status":"200","data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})


#Lead Chat Create API
@api_view(['POST'])
def chatter(request):
    try:
        Message = request.data['Message']
        Lead_Id = request.data['Lead_Id']
        Emp_Id = request.data['Emp_Id']
        Emp_Name = request.data['Emp_Name']
        UpdateDate = request.data['UpdateDate']
        UpdateTime = request.data['UpdateTime']

        model = Chatter(Message=Message, Lead_Id=Lead_Id, Emp_Id=Emp_Id, Emp_Name=Emp_Name, UpdateDate=UpdateDate, UpdateTime=UpdateTime)
        
        model.save()
        chat = Chatter.objects.latest('id')
        print(chat.id)
        return Response({"message":"Success","status":200,"data":[{"id":chat.id}]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})


#Chatter All API
@api_view(["POST"])
def chatter_all(request):
    try:    
        Lead_Id=request.data['Lead_Id']
        print(Lead_Id)
        chat_obj = Chatter.objects.filter(Lead_Id=Lead_Id).order_by("id")
        chat_json = ChatterSerializer(chat_obj, many=True)
        return Response({"message": "Success","status": 200,"data":chat_json.data})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})


#Lead All API
@api_view(["GET"])
def all(request):
    try:
        leads_obj = Lead.objects.all()        
        lead_json = LeadSerializer(leads_obj, many=True)
        return Response({"message": "Success","status": 200,"data":lead_json.data})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})

#Lead All Filter API
@api_view(["POST"])
def all_filter(request):
    try:
        json_data = request.data
        if len(json_data) == 0:
            leads_obj = Lead.objects.filter(junk=0).order_by("-id")
            leads_json = LeadSerializer(leads_obj, many=True)
            return Response({"message": "Success","status": 200,"data":leads_json.data})
        else:
            SalesPersonID = json_data['assignedTo']
            SalesPersonID = getAllReportingToUserId(SalesPersonID)               
            # emp_obj = Employee.objects.get(pk=SalesPersonID)
            # if emp_obj.role == 'manager':
            #     emps = Employee.objects.filter(reportingTo=emp_obj.SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
            #     SalesPersonID=[SalesPersonID]
            #     for emp in emps:
            #         SalesPersonID.append(emp.id)   
            # elif emp_obj.role == 'admin':
            #     emps = Employee.objects.filter(id__gt=0)
            #     SalesPersonID=[]
            #     for emp in emps:
            #         SalesPersonID.append(emp.id)
            # else:
            #     SalesPersonID = [json_data['assignedTo']]

            print(SalesPersonID)
            leadType = request.data['leadType']
            if leadType =="None":
                leads_obj = Lead.objects.filter(assignedTo__in=SalesPersonID).order_by("-id")
            elif leadType !="All":
                leads_obj = Lead.objects.filter(assignedTo__in=SalesPersonID, leadType=leadType,junk=0).order_by("-id")
            else:
                leads_obj = Lead.objects.filter(assignedTo__in=SalesPersonID,junk=0).order_by("-id")                           
            if len(leads_obj) ==0:
                return Response({"message": "Success","status": 200,"data":[]})
            else:
                leads_json = LeadSerializer(leads_obj, many=True)
                return Response({"message": "Success","status": 200,"data":leads_json.data})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})


#Lead All Junk Filter API
@api_view(["POST"])
def all_filter_junk(request):
    try:
        json_data = request.data
        
        SalesPersonID = json_data['assignedTo']                
        emp_obj = Employee.objects.get(pk=SalesPersonID)
        
        if emp_obj.role == 'manager':
            emps = Employee.objects.filter(reportingTo=emp_obj.SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
            SalesPersonID=[SalesPersonID]
            for emp in emps:
                SalesPersonID.append(emp.id)
            
        elif emp_obj.role == 'admin':
            emps = Employee.objects.filter(id__gt=0)
            SalesPersonID=[]
            for emp in emps:
                SalesPersonID.append(emp.id)
        else:
            SalesPersonID = [json_data['assignedTo']]
        
        print(SalesPersonID)
        
        leads_obj = Lead.objects.filter(assignedTo__in=SalesPersonID, junk=1).order_by("-id")                        
            
        if len(leads_obj) ==0:
            return Response({"message": "Success","status": 200,"data":[]})
        else:
            leads_json = LeadSerializer(leads_obj, many=True)
            return Response({"message": "Success","status": 200,"data":leads_json.data})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})


#Lead One API
@api_view(["POST"])
def one(request):
    try:
        id=request.data['id']    
        lead_obj = Lead.objects.get(id=id)
        lead_json = LeadSerializer(lead_obj)
        
        #added by millan on 22-September-2022
        lead_json_dump = json.loads(json.dumps(lead_json.data))
        image = Attachment.objects.filter(LinkID = lead_obj.id, LinkType='Lead')
        image_json = AttachmentSerializer(image, many=True)
        lead_json_dump['Attach'] = image_json.data
        #added by millan on 22-September-2022
        
        return Response({"message": "Success","status": 200,"data":[lead_json.data]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})


#Lead Update API
@api_view(['POST'])
def update(request):
    try:
        fetchid = int(request.data['id'])
        model = Lead.objects.get(pk = fetchid)
        model.date  = request.data['date']
        model.location  = request.data['location']
        model.companyName  = request.data['companyName']
        model.numOfEmployee  = request.data['numOfEmployee']
        model.turnover  = request.data['turnover']
        model.source  = request.data['source']
        model.contactPerson  = request.data['contactPerson']
        model.designation  = request.data['designation']
        model.phoneNumber  = request.data['phoneNumber']
        model.message  = request.data['message']
        model.email  = request.data['email']
        model.status  = request.data['status']
        model.leadType  = request.data['leadType']
        model.productInterest  = request.data['productInterest']
        model.assignedTo_id  = request.data['assignedTo']
        model.employeeId_id  = request.data['employeeId']
        model.timestamp  = request.data['timestamp']
        model.projectAmount  = request.data['projectAmount']
        model.customerType  = request.data['customerType']
        model.stages  = request.data['stages']
        model.U_LAT  = request.data['U_LAT']
        model.U_LONG  = request.data['U_LONG']
        model.save()
        
        print(fetchid)
        context = request.data

        return Response({"message":"successful","status":200,"data":[context]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})

#BusinessPartner update_lat_long
@api_view(['POST'])
def update_lat_long(request):
    try:
        LeadId = request.data['id']
        U_LAT  = request.data['U_LAT']
        U_LONG = request.data['U_LONG']
        
        if Lead.objects.filter(pk = LeadId).exists():
            bpModel = Lead.objects.get(pk = LeadId)
            bpModel.U_LAT = U_LAT
            bpModel.U_LONG = U_LONG
            bpModel.save()

            return Response({"message":"successful","status":"200","data":[]})
        else:
            return Response({"message":"Invalid","status":"201","data":[]})

    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

#Lead delete
@api_view(['POST'])
def delete(request):
    try:
        fetchids=request.data['id']
        naid = []
        for fetchid in fetchids:
            if Lead.objects.filter(pk=fetchid).exists():
                fetchdata=Lead.objects.filter(pk=fetchid).delete()
            else:
                naid.append(fetchid)
        print(str(naid))
        return Response({"message":"successful","status":"200","data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})


# @api_view(['POST'])
# def delete(request):
    # fetchid=request.data['id']
    # try:
        # fetchdata=Lead.objects.filter(pk=fetchid).delete()
        # return Response({"message":"successful","status":"200","data":[]})
    # except:
         # return Response({"message":"Id wrong","status":"201","data":[]})

#Lead Assign
@api_view(['POST'])
def assign(request):
    try:

        fetchids=request.data['id']
        empid=request.data['employeeId']
        emp=Employee.objects.get(pk=empid)
        naid = []
        for fetchid in fetchids:
            if Lead.objects.filter(pk=fetchid).exists():
                model=Lead.objects.get(pk=fetchid)
                model.assignedTo = emp
                model.save()
            else:
                naid.append(fetchid)
        print(str(naid))
        return Response({"message":"successful","status":"200","data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})
#Type Create API
@api_view(['POST'])
def type_create(request):
    try:
        Name = request.data['Name']    
        if Type.objects.filter(Name=Name).exists():        
            return Response({"message":"Already exist","status":409,"data":[]})
        else:        
            try:
                CreatedDate = request.data['CreatedDate']
                CreatedTime = request.data['CreatedTime']

                model=Type(Name = Name, CreatedDate = CreatedDate, CreatedTime = CreatedTime)
                
                model.save()
                
                tp = Type.objects.latest('id')        
                
                return Response({"message":"successful","status":200,"data":[{"id":tp.id}]})
            except Exception as e:
                return Response({"message":"Can not create","status":"201","data":[{"Error":str(e)}]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})


#Type Update API
@api_view(['POST'])
def type_update(request):
    try:
        fetchid = request.data['id']
        model = Type.objects.get(pk = fetchid)
        model.Name  = request.data['Name']
        model.CreatedDate  = request.data['CreatedDate']
        model.CreatedTime  = request.data['CreatedTime']
        model.save()
        return Response({"message":"successful","status":200,"data":[request.data]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})


#Source Create API
@api_view(['POST'])
def source_create(request):
    try:
        Name = request.data['Name']    
        if Source.objects.filter(Name=Name).exists():        
            return Response({"message":"Already exist","status":409,"data":[]})
        else:        
            CreatedDate = request.data['CreatedDate']
            CreatedTime = request.data['CreatedTime']
            model=Source(Name = Name, CreatedDate = CreatedDate, CreatedTime = CreatedTime)            
            model.save()            
            sc = Source.objects.latest('id')
            return Response({"message":"successful","status":200,"data":[{"id":sc.id}]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})


#Type Update API
@api_view(['POST'])
def source_update(request):
    try:
        fetchid = request.data['id']
        model = Source.objects.get(pk = fetchid)
        model.Name  = request.data['Name']
        model.CreatedDate  = request.data['CreatedDate']
        model.CreatedTime  = request.data['CreatedTime']
        model.save()
        return Response({"message":"successful","status":200,"data":[request.data]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})

#LeadType All API
@api_view(["GET"])
def type_all(request):
    try:
        type_obj = Type.objects.all()        
        type_json = TypeSerializer(type_obj, many=True)
        return Response({"message": "Success","status": 200,"data":type_json.data})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})

#SourceType All API
@api_view(["GET"])
def source_all(request):
    try:
        source_obj = Source.objects.all()        
        source_json = SourceSerializer(source_obj, many=True)
        return Response({"message": "Success","status": 200,"data":source_json.data})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})


#Type delete
@api_view(['POST'])
def type_delete(request):
    try:
        fetchid=request.data['id']
        fetchdata=Type.objects.filter(pk=fetchid).delete()
        return Response({"message":"successful","status":"200","data":[]})        
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})


#Source delete
@api_view(['POST'])
def source_delete(request):
    try:
        fetchid=request.data['id']
        fetchdata=Source.objects.filter(pk=fetchid).delete()
        return Response({"message":"successful","status":"200","data":[]})        
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})

#added by millan on 06-October-2022 for adding attachment
@api_view(["POST"])
def lead_attachment_create(request):
    try:
        lead_id = request.data['lead_id']
        CreateDate = request.data['CreateDate']
        CreateTime = request.data['CreateTime']
        CreatedBy = request.data['CreatedBy']
        print(request.FILES.getlist('Attach'))
        for File in request.FILES.getlist('Attach'):
            attachmentsImage_url = ""
            target ='./bridge/static/image/LeadAttachment'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+File.name, File)
            file_size = os.stat(file)
            Size = file_size.st_size
            productImage_url = fss.url(file)
            attachmentsImage_url = productImage_url.replace('/bridge', '')
            print(attachmentsImage_url)

            att=LeadAttachment(File=attachmentsImage_url, LeadId=lead_id, CreateDate=CreateDate, CreateTime=CreateTime, CreatedBy=CreatedBy, Size=Size)
            
            att.save()  
            
        return Response({"message": "success","status": 200,"data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})

#for updating attachment
@api_view(['POST'])
def lead_attachment_update(request):
    try:
        lead_id = request.data['lead_id']
        fetchid = request.data['id']
        
        File = request.data['Attach']
        
        model = LeadAttachment.objects.get(pk = fetchid, LeadId=lead_id)
        
        model.UpdateDate = request.data['UpdateDate']
        model.UpdateTime = request.data['UpdateTime']
        
        model.UpdatedBy = request.data['UpdatedBy']

        attechmentsImage_url = ""
        if File:
            target ='./bridge/static/image/LeadAttachment'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+File.name, File)
            file_size = os.stat(file)
            Size = file_size.st_size
            productImage_url = fss.url(file)
            attechmentsImage_url = productImage_url.replace('/bridge', '')
            print(attechmentsImage_url)
            model.File = attechmentsImage_url
            model.Size = Size
        else:
            model.File= model.File
            print('no image')
        
        model.save()
        
        return Response({"message": "success","status": 200,"data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})

#for deleting an attachment
@api_view(['POST'])
def lead_attachment_delete(request):
    try:
        fetchid = request.data['id']
        
        lead_id = request.data['lead_id']
        
        if LeadAttachment.objects.filter(pk=fetchid, LeadId=lead_id).exists():
            
            LeadAttachment.objects.filter(pk=fetchid, LeadId=lead_id).delete()
            
            return Response({"message":"successful","status":"200","data":[]})
        else:
            return Response({"message":"ID Not Found","status":"201","data":[]})
        
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})

#get all attachment based on lead id
@api_view(["POST"])
def lead_attachments(request):
    try:
        lead_id=request.data['lead_id']
        if lead_id > 0:
            leadAttachObjs = LeadAttachment.objects.filter(LeadId = lead_id)
            leadAttachArr = []
            for attchObj in leadAttachObjs:
                leadAttachjson = LeadAttachmentSerilaizer(attchObj)
                leadData = json.loads(json.dumps(leadAttachjson.data))
                CreatedBy = attchObj.CreatedBy
                UpdatedBy = attchObj.UpdatedBy
                
                if leadData['CreatedBy'] > 0:
                    empObj = Employee.objects.filter(pk = CreatedBy).values('firstName', 'lastName')
                    leadData['CreatedBy'] = empObj
                    leadAttachArr.append(leadData)
                if leadData['UpdatedBy'] > 0:
                    empObj = Employee.objects.filter(pk = UpdatedBy).values('firstName', 'lastName')
                    leadData['UpdatedBy'] = empObj
                    leadAttachArr.append(leadData)
                
            return Response({"message": "Success","status": 200,"data":leadAttachArr})
        else:
            return Response({"message": "Customer ID Not Found","status": 201,"data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})

#added by millan on 13-October-2022 for adding notes
@api_view(["POST"])
def lead_notes_create(request):
    try:
        lead_id = request.data['lead_id']
        Title = request.data['Title']
        Remarks = request.data['Remarks']
        CreateDate = request.data['CreateDate']
        CreateTime = request.data['CreateTime']
        CreatedBy = request.data['CreatedBy']

        att=Notes(LeadId=lead_id, CreateDate=CreateDate, CreateTime=CreateTime, CreatedBy=CreatedBy, Title=Title, Remarks = Remarks) 
        att.save()  
            
        return Response({"message": "success","status": 200,"data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})

#added by millan on 13-October-2022 for getting notes list based on lead id
@api_view(["POST"])
def lead_notes(request):
    try:
        lead_id=request.data['lead_id']
        if lead_id > 0:
            leads_obj = Notes.objects.filter(LeadId = lead_id)
            lead_json = NotesSerilaizer(leads_obj, many=True)
            return Response({"message": "Success","status": 200,"data":lead_json.data})
        else:
            return Response({"message": "Success","status": 200,"data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})    
        
#Lead Mark Junk
@api_view(['POST'])
def mark_junk(request):
    try:
        fetchids=request.data['id']
        status=request.data['status']
        naid = []
        for fetchid in fetchids:
            print(fetchid)
            if Lead.objects.filter(pk=fetchid).exists():
                fetchdata=Lead.objects.filter(pk=fetchid).update(junk=status)
            else:
                naid.append(fetchid)
        print(str(naid))
        return Response({"message":"successful","status":"200","data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})