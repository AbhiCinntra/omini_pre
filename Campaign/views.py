import json
from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse

from Employee.serializers import EmployeeSerializer
from Industries.models import Industries
from Industries.serializers import IndustriesSerializer
from Opportunity.models import Opportunity
from BusinessPartner.models import BPEmployee, BusinessPartner
# from bridge.Campaign.emailCampaign import sendMail

from .models import *
from Employee.models import Employee
from Lead.models import *

from django.contrib import messages

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import *
from rest_framework.parsers import JSONParser
from rest_framework import status

import os
from django.core.files.storage import FileSystemStorage

#Campaign Set Create API
@api_view(['POST'])
def create_campset(request):
    try:
        CampaignSetName =request.data['CampaignSetName']
        CampaignSetOwner =request.data['CampaignSetOwner']
        CampaignAccess =request.data['CampaignAccess']
        Description =request.data['Description']

        LeadSource =request.data['LeadSource']
        LeadPriority =request.data['LeadPriority']
        LeadStatus =request.data['LeadStatus']
        LeadFromDate =request.data['LeadFromDate']
        LeadToDate =request.data['LeadToDate']

        #OppDivision =request.data['#OppDivision']
        OppType =request.data['OppType']
        OppSalePerson =request.data['OppSalePerson']
        OppStage =request.data['OppStage']
        OppFromDate =request.data['OppFromDate']
        OppToDate =request.data['OppToDate']

        BPType = request.data['BPType']
        BPSalePerson = request.data['BPSalePerson']
        BPCountry = request.data['BPCountry']
        BPState = request.data['BPState']
        BPCountryCode = request.data['BPCountryCode']
        BPStateCode = request.data['BPStateCode']
        BPIndustry =request.data['BPIndustry']
        BPFromDate =request.data['BPFromDate']
        BPToDate =request.data['BPToDate']

        # MemberList =request.data['MemberList']

        # Status =request.data['Status']
        CreateBy =request.data['CreateBy']
        CreateDate =request.data['CreateDate']
        CreateTime=request.data['CreateTime']
        
        AllLead = request.data['AllLead']
        AllOpp = request.data['AllOpp']
        AllBP = request.data['AllBP']

        
        model = CampaignSet(CampaignSetName = CampaignSetName, CampaignSetOwner_id = CampaignSetOwner, CampaignAccess = CampaignAccess, Description = Description, LeadSource = LeadSource, LeadPriority = LeadPriority, LeadStatus = LeadStatus, LeadFromDate = LeadFromDate, LeadToDate = LeadToDate, OppType = OppType, OppSalePerson = OppSalePerson, OppStage = OppStage, OppFromDate = OppFromDate, OppToDate = OppToDate, BPType = BPType, BPSalePerson = BPSalePerson, BPCountry = BPCountry, BPState = BPState, BPIndustry = BPIndustry, BPFromDate = BPFromDate, BPToDate = BPToDate, MemberList = '', CreateBy_id = CreateBy, CreateDate = CreateDate, CreateTime= CreateTime, BPCountryCode = BPCountryCode, BPStateCode = BPStateCode, AllLead = AllLead, AllOpp = AllOpp, AllBP = AllBP)
        model.save()

        campset = CampaignSet.objects.latest('id')
        print(campset.id)
        ListCampaignSetMember(request.data, campset.id)
        return Response({"message":"Success","status":"200","data":[]})
    except Exception as e:
        return Response({"message":"Error","status":"201","data":[{"ErrorMsg": str(e)}]})


#Campaign Create API
@api_view(['POST'])
def create_camp(request):
    try:
        CampaignSetId =request.data['CampaignSetId']
        CampaignName =request.data['CampaignName']
        CampaignOwner =request.data['CampaignOwner']
        StartDate =request.data['StartDate']
        EndDate =request.data['EndDate']
        Type =request.data['Type']
        Frequency =request.data['Frequency']
        WeekDay =request.data['WeekDay']
        MonthlyDate =request.data['MonthlyDate']
        Subject =request.data['Subject']
        Message =request.data['Message']
        # Status =request.data['Status']
        CreateDate = request.data['CreateDate']
        CreateTime = request.data['CreateTime']
        RunTime = request.data['RunTime']
        Attachments = request.data['Attachments']
        
        attechmentsImage_url = ""
        if Attachments:
            target ='./bridge/static/image/campaign'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+Attachments.name, Attachments)
            productImage_url = fss.url(file)
            attechmentsImage_url = productImage_url.replace('/bridge', '')
        print(attechmentsImage_url)

        model = Campaign(CampaignSetId_id = CampaignSetId, CampaignName = CampaignName, CampaignOwner_id = CampaignOwner, StartDate = StartDate, EndDate = EndDate, Type = Type, Frequency = Frequency, WeekDay = WeekDay, MonthlyDate = MonthlyDate, Message = Message, CreateDate = CreateDate, CreateTime = CreateTime, Subject = Subject, RunTime = RunTime, Attachments = attechmentsImage_url)
        
        model.save()
        camp = Campaign.objects.latest('id')
        print(camp.id)
        
        # EmailCampain(CampaignSetId, camp.id)
        return Response({"message":"Success","status":"200","data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})


#CampaignSet All API
@api_view(["GET"])
def all_campset(request):
    try:
        campset_obj = CampaignSet.objects.all().order_by("-id")
        # campset_json = CampaignSetSerializer(campset_obj, many=True)
        result = showCamSet(campset_obj)
        return Response({"message": "Success","status": 200,"data":result})
    except Exception as e:
       return Response({"message": "error","status": 201,"data":[str(e)]}) 

#Campaign All API
@api_view(["GET"])
def all_camp(request):
    camp_obj = Campaign.objects.all().order_by("-id")
    # camp_json = CampaignSerializer(camp_obj, many=True)
    result = showCampaign(camp_obj)    
    return Response({"message": "Success","status": 200,"data":result})

#CampaignSet One API
@api_view(["POST"])
def one_campset(request):
    try:
        id=request.data['id']    
        campset_obj = CampaignSet.objects.filter(id=id)
        # campset_json = CampaignSetSerializer(campset_obj)
        result = showCamSet(campset_obj)
        return Response({"message": "Success","status": 200,"data":result})
    except Exception as e:
       return Response({"message": "error","status": 201,"data":[str(e)]})

#Campaign One API
@api_view(["POST"])
def one_camp(request):
    try:            
        id=request.data['id']    
        camp_obj = Campaign.objects.filter(id=id)
        # camp_json = CampaignSerializer(camp_obj)
        result = showCampaign(camp_obj)
        return Response({"message": "Success","status": 200,"data":result})
    except Exception as e:
       return Response({"message": "error","status": 201,"data":[str(e)]})

# Filter Campaign
@api_view(["POST"])
def filter_campaign(request):
    try:            
        CampaignSetId = request.data['CampaignSetId']    
        camp_obj = Campaign.objects.filter(CampaignSetId = CampaignSetId)
        # camp_json = CampaignSerializer(camp_obj)
        result = showCampaign(camp_obj)
        return Response({"message": "Success","status": 200,"data":result})
    except Exception as e:
       return Response({"message": "error","status": 201,"data":[str(e)]})


# change campaign set status
@api_view(["POST"])
def campaignset_satus(request):
    try:            
        CampaignSetId = request.data['CampaignSetId'] 
        Status = request.data['Status']
        if CampaignSet.objects.filter(pk = CampaignSetId).exists():
            CampaignSet.objects.filter(pk = CampaignSetId).update(Status = Status)
            Campaign.objects.filter(CampaignSetId_id = CampaignSetId).update(Status = Status)
            return Response({"message": "Success","status": 200,"data":[]})
        else:
            return Response({"message": "error","status": 201,"data":["Wrong CampaignSet Id"]})     
    except Exception as e:
       return Response({"message": "error","status": 201,"data":[str(e)]})
# {"CampaignSetId": 1, "Status": 0}

# change campaign status
@api_view(["POST"])
def campaign_satus(request):
    try:            
        CampaignId = request.data['CampaignId']   
        Status = request.data['Status']
        if Campaign.objects.filter(pk = CampaignId).exists():
            Campaign.objects.filter(pk = CampaignId).update(Status = Status)
            return Response({"message": "Success","status": 200,"data":[]})
        else:
            return Response({"message": "error","status": 201,"data":["Wrong Campaign Id"]})    
    except Exception as e:
       return Response({"message": "error","status": 201,"data":[str(e)]})
# {"CampaignId": 1, "Status": 0}


# ------------------------------
# ----- Show Campaign Fun-------
# ------------------------------
def showCampaign(objs):
    allCampaign = []
    for obj in objs:
        CampaignOwner = obj.CampaignOwner
        
        camjson = CampaignSerializer(obj)
        finalCam = json.loads(json.dumps(camjson.data))

        if CampaignOwner.id != "":
            sobj = Employee.objects.filter(SalesEmployeeCode = CampaignOwner.id).values("SalesEmployeeCode","SalesEmployeeName")
            sobj_json = EmployeeSerializer(sobj, many=True)
            finalCam['CampaignOwner'] = sobj_json.data
        else:
            finalCam['CampaignOwner'] = []
            
        allCampaign.append(finalCam)
    return allCampaign
# ----------------------------------


# ----------------------------------
# ----- Show Campaign Set Fun-------
# ----------------------------------
def showCamSet(objs):
    allCamSet = []
    for obj in objs:
        camSetId = obj.id
        OppSalePersonId = obj.OppSalePerson
        BPSalePersonId = obj.BPSalePerson
        CampaignSetOwnerId = obj.CampaignSetOwner
        CreateById = obj.CreateBy
        BPIndustryId = obj.BPIndustry

        print('----')
        print(OppSalePersonId,BPSalePersonId,CampaignSetOwnerId.id)

        camjson = CampaignSetSerializer(obj)
        finalCamSet = json.loads(json.dumps(camjson.data))

        memberObj = CampaignSetMembers.objects.filter(CampSetId_id = camSetId)
        memberjson = CampaignSetMembersSerializer(memberObj, many=True)
        finalCamSet['MemberList'] = json.loads(json.dumps(memberjson.data))
        
        if OppSalePersonId != "":
            OppSalePersonbj = Employee.objects.filter(SalesEmployeeCode__in = OppSalePersonId.split(",")).values("SalesEmployeeCode","SalesEmployeeName")
            OppSalePerson_json = EmployeeSerializer(OppSalePersonbj, many=True)
            finalCamSet['OppSalePerson'] = OppSalePerson_json.data
        else:
            finalCamSet['OppSalePerson'] = []

        if BPSalePersonId != "":
            BPSalePersonobj = Employee.objects.filter(SalesEmployeeCode__in = BPSalePersonId.split(",")).values("SalesEmployeeCode","SalesEmployeeName")
            BPSalePersonJson = EmployeeSerializer(BPSalePersonobj, many=True)
            finalCamSet['BPSalePerson'] = BPSalePersonJson.data
        else:
            finalCamSet['BPSalePerson'] = []
        
        if CampaignSetOwnerId.id != "":
            sobj = Employee.objects.filter(SalesEmployeeCode = CampaignSetOwnerId.id).values("SalesEmployeeCode","SalesEmployeeName")
            sobj_json = EmployeeSerializer(sobj, many=True)
            finalCamSet['CampaignSetOwner'] = sobj_json.data
        else:
            finalCamSet['CampaignSetOwner'] = []
        
        if CreateById.id != "":
            CreateByobj = Employee.objects.filter(SalesEmployeeCode = CreateById.id).values("SalesEmployeeCode","SalesEmployeeName")
            CreateByJson = EmployeeSerializer(CreateByobj, many=True)
            finalCamSet['CreateBy'] = CreateByJson.data
        else:
            finalCamSet['CreateBy'] = []
        if BPIndustryId !="":
            ind = Industries.objects.filter(IndustryCode__in = BPIndustryId.split(",")).values("IndustryCode","IndustryName")
            ind_json = IndustriesSerializer(ind, many=True)
            finalCamSet['BPIndustry'] = ind_json.data
        else:
            finalCamSet['BPIndustry'] = []

        allCamSet.append(finalCamSet)
    return allCamSet
# -------------------------------------------


# -------------------------------------------
#Campaign set update
@api_view(['POST'])
def update_campset(request):
    try:
        CamSetId = request.data['id']
        fetchObj = CampaignSet.objects.get(pk = CamSetId)
        fetchJson = CampaignSetSerializer(fetchObj, data = request.data)
        if fetchJson.is_valid():
            fetchJson.save()
            ListCampaignSetMember(fetchJson.data, CamSetId)
            return Response({"status":"200","message":"successfully","data":[fetchJson.data]})
        return Response(fetchJson.errors,status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"status":"201","message":"error","data":[str(e)]})

#Activity Update API
@api_view(['POST'])
def update_camp(request):
    try:
        request.data._mutable = True
        
        CampainId = request.data['id']
        Attachments = request.data['Attachments']

        fetchObj = Campaign.objects.get(pk = CampainId)

        attechmentsImage_url = ""
        if Attachments:
            target ='./bridge/static/image/campaign'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+Attachments.name, Attachments)
            productImage_url = fss.url(file)
            attechmentsImage_url = productImage_url.replace('/bridge', '')
            print(attechmentsImage_url)
            request.data['Attachments'] = attechmentsImage_url
        else:
            request.data['Attachments'] = fetchObj.Attachments
            print('no image')
            
        fetchJson = CampaignSerializer(fetchObj, data = request.data)
        if fetchJson.is_valid():
            fetchJson.save()
            return Response({"status":"200","message":"successfully","data":[fetchJson.data]})
        return Response(fetchJson.errors,status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"status":"201","message":"error","data":[str(e)]})
# ---------------------------------------


# ---------------------------------------
# ----- List Campaign Set Member --------
# ---------------------------------------
def ListCampaignSetMember(requestData, CamSetId):
    print('------ListCampaignSetMember------')

    userList = []

    # ----------------------------------
    # -------Filter for Lead -----------
    # ----------------------------------

    AllLeadCheck = int(requestData['AllLead'])
    AllOppCheck = int(requestData['AllOpp'])
    AllBPCheck = int(requestData['AllBP'])
    
    leadFlag = False;
    oppFlag = False;
    bpFlag = False

    if AllLeadCheck == 1:
        leadwhere = ''
        leadFlag = True;
    else:
        leadwhere = 'WHERE 1 '
        LeadSource = requestData['LeadSource'].strip()
        LeadPriority = requestData['LeadPriority'].strip()
        LeadStatus = requestData['LeadStatus'].strip()
        LeadFromDate = requestData['LeadFromDate'].strip()
        LeadToDate = requestData['LeadToDate'].strip()
        

        if LeadSource != "":
            leadwhere += 'and `source` in("'+ LeadSource.replace(',','","') +'")'
            leadFlag = True;

        if LeadPriority != "":
            leadwhere += 'and `leadType` in("'+ LeadPriority.replace(',','","') +'")'
            leadFlag = True;

        if LeadStatus != "":
            leadwhere += 'and `status` in("'+ LeadStatus.replace(',','","') +'")'
            leadFlag = True;

        if LeadFromDate != "" and LeadToDate != "":
            leadwhere += 'and `date` >= "'+ LeadFromDate + '" and `date` <= "'+  LeadToDate +'" '
            leadFlag = True;

    if leadFlag:
        sqlSelectLead = "SELECT `id`, `contactPerson`, `phoneNumber`, `email`, `leadType`, `status` FROM `Lead_lead` " + str(leadwhere)
        print(sqlSelectLead)
        leadObj = Lead.objects.raw(sqlSelectLead)
        for contactPrson in leadObj:
            userData = {
                'Name': contactPrson.contactPerson,
                'Phone': contactPrson.phoneNumber,
                'Email': contactPrson.email
            }
            userList.append(userData)
    else:
        print('>>>>>>>>>>> no lead <<<<<<<<<<<<<<<<')

    # ----------------------------------------
    # --------- Oppertunity data -------------
    # ----------------------------------------
    if AllOppCheck == 1:
        oppwhere = ''
        oppFlag = True;
    else:
        oppwhere = 'WHERE 1 '
        OppType = requestData['OppType'].strip()
        OppSalePerson = requestData['OppSalePerson'].strip()
        OppFromDate = requestData['OppFromDate'].strip()
        OppToDate = requestData['OppToDate'].strip()


        if OppType != "":
            oppwhere += 'and `U_TYPE` = "'+ OppType +'" '
            oppFlag = True;

        if OppSalePerson != "":
            oppwhere += 'and `SalesPerson` in("'+ str(OppSalePerson).replace(',','","') +'")'
            oppFlag = True;

        if OppFromDate != "" and OppToDate != "":
            oppwhere += 'and `StartDate` >= "'+ OppFromDate + '" and `ClosingDate` <= "'+  OppToDate +'" '
            oppFlag = True;

    if oppFlag:

        sqlSelectOpp = "SELECT DISTINCT ContactPerson, ContactPersonName,id FROM Opportunity_opportunity " + oppwhere
        print(sqlSelectOpp)
        oppObj = Opportunity.objects.raw(sqlSelectOpp)
        for oppData in oppObj:
            # print(oppData)
            ContactPersonId = oppData.id
            sqlSelectBpEmp = "SELECT `id`,`FirstName`, `MobilePhone`, `E_Mail` FROM `BusinessPartner_bpemployee` WHERE `id` = "+ str(ContactPersonId)
            bpObj = BPEmployee.objects.raw(sqlSelectBpEmp)
            for bpEmp in bpObj:
                # print('-----Emp data----')
                # print(data)
                userData = {
                    'Name': bpEmp.FirstName,
                    'Phone': bpEmp.MobilePhone,
                    'Email': bpEmp.E_Mail
                }
                userList.append(userData)
    else:
        print('>>>>>>>>>>> no OPP <<<<<<<<<<<<<<<<')
    # ----------------------------------------
    # ----------- Customer data --------------
    # ----------------------------------------
    if AllBPCheck == 1:
        bpwhere = ''
        bpFlag = True;
    else:
        bpwhere = 'WHERE 1 '
        BPType = requestData['BPType'].strip()
        BPSalePerson = requestData['BPSalePerson']
        BPCountry = requestData['BPCountry'].strip()
        BPState = requestData['BPState'].strip()
        BPIndustry = requestData['BPIndustry']
        BPFromDate = requestData['BPFromDate'].strip()
        BPToDate = requestData['BPToDate'].strip()

        if BPType != "":
            bpwhere += 'and BusinessPartner_businesspartner.U_TYPE = "'+ str(BPType) +'" '
            bpFlag = True

        if BPSalePerson != "":
            bpwhere += 'and BusinessPartner_businesspartner.SalesPersonCode in("'+ str(BPSalePerson).replace(',','","') +'") '
            bpFlag = True

        if BPFromDate != "" and BPToDate != "":
            bpwhere += 'and BusinessPartner_businesspartner.CreateDate >= "'+ str(BPFromDate) + '" and BusinessPartner_businesspartner.CreateDate <= "'+  str(BPToDate) +'" '
            bpFlag = True

        if BPIndustry != "":
            bpwhere += 'and BusinessPartner_businesspartner.Industry in("'+ str(BPIndustry).replace(',','","') +'") '
            bpFlag = True
        
        if BPCountry != "":
            bpwhere += 'and BusinessPartner_bpaddresses.Country = "'+ str(BPCountry) +'" '
            bpFlag = True
        
        if BPState != "":
            oppwhere += 'and BusinessPartner_bpaddresses.State = "'+ str(BPState) +'" '
            bpFlag = True

    if bpFlag:
        sqlSelectBP = "SELECT BusinessPartner_businesspartner.id FROM BusinessPartner_businesspartner JOIN BusinessPartner_bpaddresses ON BusinessPartner_businesspartner.id = BusinessPartner_bpaddresses.BPID " + str(bpwhere)
        print(sqlSelectBP)
        bpObj = BusinessPartner.objects.raw(sqlSelectBP)
        for bp in bpObj:
            # print(oppData)
            ContactPersonId = bp.id
            sqlSelectBpEmp = "SELECT `id`,`FirstName`, `MobilePhone`, `E_Mail` FROM `BusinessPartner_bpemployee` WHERE `id` = "+ str(ContactPersonId)
            bpEObj = BPEmployee.objects.raw(sqlSelectBpEmp)
            for bpEmp in bpEObj:
                # print('-----Emp data----')
                # print(data)
                userData = {
                    'Name': bpEmp.FirstName,
                    'Phone': bpEmp.MobilePhone,
                    'Email': bpEmp.E_Mail
                }
                userList.append(userData)
    else:
        print('>>>>>>>>>>> no BP <<<<<<<<<<<<<<<<')

    # alluser 
    for user in userList:
        # print(user)
        Name = user['Name']
        Phone = user['Phone']
        Email = user['Email']

        if CampaignSetMembers.objects.filter(Phone = Phone, CampSetId_id = CamSetId).exists():
            print('--- Campain Member already exist data ---')
        else:
            print('---Campain Member Insert---')
            print(user)
            CampaignSetMembers(
                Name = Name,
                Phone = Phone,
                Email = Email,
                CampSetId_id = CamSetId
            ).save()
            
#added by millan on 08-September-2022
#campaign set members api based on camapiagnset
@api_view(["POST"])
def get_member(request):
    try: 
        if CampaignSetMembers.objects.filter(CampSetId_id = request.data['CampSetId']).exists():
            CampSetId = request.data['CampSetId']
            campaignMember = CampaignSetMembers.objects.filter(CampSetId = CampSetId)
            cm_obj = CampaignSetMembersSerializer(campaignMember, many=True)
            finalCampaignMembers = json.loads(json.dumps(cm_obj.data))
            return Response({"message": "Success","status": 200,"data":finalCampaignMembers})
        else:
            return Response({"message": "Error! CampSetId Not Found","status": 201,"data":[]})
    except Exception as e: 
        return Response({"message": str(e),"status": 201,"data":[]})

#added by millan on 26-September-2022
@api_view(["POST"])
def member_create(request):
    # try:
        campMember = request.data
        for cm in campMember:
            CampSetId = cm['CampSetId']
            Name = cm['Name']
            Phone = cm['Phone']
            Email = cm['Email']
            if CampaignSetMembers.objects.filter(Phone=Phone, Email=Email, CampSetId_id = CampSetId).exists():
                print("same data")
            else:
                model = CampaignSetMembers(CampSetId_id = CampSetId, Name = Name, Phone = Phone, Email = Email)
                model.save()
    
        return Response({"message": "success","status": 200,"data":[]})
    # except Exception as e: 
    #     return Response({"message": str(e),"status": 201,"data":[]})
