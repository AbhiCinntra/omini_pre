import math
from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from Employee.models import Employee
from Employee.serializers import EmployeeSerializer
from PaymentTermsTypes.models import PaymentTermsTypes

# import PaymentTermsTypes
from PaymentTermsTypes.serializers import PaymentTermsTypesSerializer
from Order.models import Order
from Activity.serializers import ActivitySerializer
from Pagination.models import Pagination
from Invoice.models import CreditNotes, CreditNotesDocumentLines, DocumentLines, IncomingPaymentInvoices, IncomingPayments, Invoice
from Company.models import Branch
from PurchaseInvoices.models import PurchaseCreditNotes, PurchaseInvoices, VendorPayments, VendorPaymentsInvoices
from global_methods import getAllReportingToIds, get_mm_yy, getAllReportingToUserId, getZoneByEmployee, groupby
from .models import *  
from Activity.models import Activity
import requests, json
from JournalEntries.models import *

from django.contrib import messages

from DeliveryNote.views import pending_order
import pandas as pd

from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import *
from rest_framework.parsers import JSONParser

#added by millan on 03-10-2022
import os
from django.core.files.storage import FileSystemStorage

from datetime import date, timedelta   

# import setting file
from django.conf import settings
from django.db.models import Q
from datetime import datetime

import mysql.connector

# sql connection custom function
def sqlconn():
    mydb = mysql.connector.connect(
        host      = settings.DATABASES['default']['HOST'],
        user      = settings.DATABASES['default']['USER'],
        password  = settings.DATABASES['default']['PASSWORD'],
        database  = settings.DATABASES['default']['NAME']
    )
    mycursor = mydb.cursor(dictionary=True, buffered=True)
    return mycursor

# Create your views here.  
#BusinessPartner Create API
@api_view(['POST'])
def create(request):
    bp_data = ""
    BpId = 0
    try:
        if BusinessPartner.objects.filter(CardName=request.data['CardName']).exists():
            return Response({"message":"Already exist Card Name","status":"201","data":[]})
        else:    
            CardName        = request.data['CardName']
            Industry        = request.data['Industry']
            CardType        = request.data['CardType']
            Website         = request.data['Website']
            EmailAddress    = request.data['EmailAddress']
            Phone1          = request.data['Phone1']
            DiscountPercent = request.data['DiscountPercent']
            Currency        = request.data['Currency']
            IntrestRatePercent = request.data['IntrestRatePercent']
            CommissionPercent = request.data['CommissionPercent']
            Notes           = request.data['Notes']
            PayTermsGrpCode = request.data['PayTermsGrpCode']
            CreditLimit     = request.data['CreditLimit']
            AttachmentEntry = request.data['AttachmentEntry']
            SalesPersonCode = request.data['SalesPersonCode'] 
            ContactPerson   = request.data['ContactEmployees'][0]['Name']
            U_PARENTACC     = request.data['U_PARENTACC']
            U_BPGRP         = request.data['U_BPGRP']
            U_CONTOWNR      = request.data['U_CONTOWNR']
            U_RATING        = request.data['U_RATING']
            U_TYPE          = request.data['U_TYPE']
            U_ANLRVN        = request.data['U_ANLRVN']
            U_CURBAL        = request.data['U_CURBAL']
            U_ACCNT         = request.data['U_ACCNT']
            U_INVNO         = request.data['U_INVNO']
            U_LAT           = request.data['U_LAT']
            U_LONG          = request.data['U_LONG']
            CreateDate      = request.data['CreateDate']
            CreateTime      = request.data['CreateTime']
            UpdateDate      = request.data['UpdateDate']
            UpdateTime      = request.data['UpdateTime']
            U_LEADID        = request.data['U_LEADID']
            U_LEADNM        = request.data['U_LEADNM']
            GroupType       = request.data['GroupType']
            CustomerType    = request.data['CustomerType']
            PriceCategory   = request.data['PriceCategory']
            PaymantMode     = request.data['PaymantMode']
            DeliveryMode    = request.data['DeliveryMode']
            Turnover        = request.data['Turnover']
            TCS             = request.data['TCS']
            Link            = request.data['Link']
            BeneficiaryName = request.data['BeneficiaryName']
            BankName        = request.data['BankName']
            ACNumber        = request.data['ACNumber']
            IfscCode        = request.data['IfscCode']
            Unit            = request.data['Unit']
            FreeDelivery    = request.data['FreeDelivery']
            CreatedBy       = request.data['CreatedBy']
            
            model = BusinessPartner(CardName = CardName, Industry = Industry, CardType = CardType, Website = Website, EmailAddress = EmailAddress, Phone1 = Phone1, DiscountPercent = DiscountPercent, Currency = Currency, IntrestRatePercent = IntrestRatePercent, CommissionPercent = CommissionPercent, Notes = Notes, PayTermsGrpCode = PayTermsGrpCode, CreditLimit = CreditLimit, AttachmentEntry = AttachmentEntry, SalesPersonCode = SalesPersonCode, ContactPerson = request.data['ContactEmployees'][0]['Name'], U_PARENTACC = U_PARENTACC, U_BPGRP = U_BPGRP, U_CONTOWNR = U_CONTOWNR, U_RATING = U_RATING, U_TYPE = U_TYPE, U_ANLRVN = U_ANLRVN, U_CURBAL = U_CURBAL, U_ACCNT = U_ACCNT, U_INVNO = U_INVNO, U_LAT = U_LAT, U_LONG = U_LONG, CreateDate = CreateDate, CreateTime = CreateTime, UpdateDate = UpdateDate, UpdateTime = UpdateTime, U_LEADID = U_LEADID, U_LEADNM = U_LEADNM, GroupType = GroupType, CustomerType = CustomerType, PriceCategory = PriceCategory, PaymantMode = PaymantMode, DeliveryMode = DeliveryMode, Turnover = Turnover, TCS = TCS, Link = Link, BeneficiaryName = BeneficiaryName, BankName = BankName, ACNumber = ACNumber, IfscCode = IfscCode, Unit = Unit, FreeDelivery = FreeDelivery, CreatedBy = CreatedBy)
            
            model.save()
            bp = BusinessPartner.objects.latest('id')
            BpId = bp.id
            CardCode = "C"+str(BpId)
            bp.CardCode = CardCode
            bp.save()

            bpemp = BPEmployee(U_BPID=BpId, CardCode=CardCode, U_BRANCHID=1, MobilePhone=request.data['ContactEmployees'][0]['MobilePhone'], FirstName=request.data['ContactEmployees'][0]['Name'], E_Mail=request.data['ContactEmployees'][0]['E_Mail'], CreateDate=CreateDate, CreateTime=CreateTime, UpdateDate=UpdateDate, UpdateTime=UpdateTime)
            
            bpemp.save()
            em = BPEmployee.objects.latest('id')
            bpemp.InternalCode = em.id
            bpemp.save()
            
            if request.data['BPAddresses'][0]['AddressType']=='bo_BillTo' :
                bpadd = request.data['BPAddresses'][0]
                #print(request.data['BPAddresses'][0]['AddressType'])
                model_add = BPAddresses(BPID=BpId, AddressName = bpadd['AddressName'], Street = bpadd['Street'], Block = bpadd['Block'], ZipCode = bpadd['ZipCode'], City = bpadd['City'], Country = bpadd['Country'], AddressType = bpadd['AddressType'], RowNum=0, BPCode = CardCode, U_STATE = bpadd['U_STATE'], State = bpadd['State'], U_COUNTRY = bpadd['U_COUNTRY'], U_SHPTYP = bpadd['U_SHPTYP'], District = bpadd['District'])
                model_add.save()
            
            # if request.data['BPAddresses'][1]['AddressType']=='bo_ShipTo' :
                bpadd1 = request.data['BPAddresses'][0]
                #print(request.data['BPAddresses'][0]['AddressType'])
                model_br = BPBranch(BPID=BpId, BranchName=CardName, AddressName = bpadd1['AddressName'], Street = bpadd1['Street'], Block = bpadd1['Block'], ZipCode = bpadd1['ZipCode'], City = bpadd1['City'], Country = bpadd1['Country'], AddressType = bpadd1['AddressType'], RowNum=1, BPCode = CardCode, U_STATE = bpadd1['U_STATE'], Default=1, State = bpadd1['State'], U_COUNTRY = bpadd1['U_COUNTRY'], U_SHPTYP = bpadd1['U_SHPTYP'], CreateDate = CreateDate, CreateTime = CreateTime, UpdateDate = UpdateDate, UpdateTime = UpdateTime, District = bpadd['District'])
                model_br.save()
        
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            localBPAddresses = request.data['BPAddresses']
            SAPBPAddresses = [
                {
                    "AddressName": localBPAddresses[0]['AddressName'],
                    "Street": localBPAddresses[0]['Street'],
                    "Block": localBPAddresses[0]['Block'],
                    "ZipCode": localBPAddresses[0]['ZipCode'],
                    "City": localBPAddresses[0]['City'],
                    "Country": localBPAddresses[0]['Country'],
                    "State": localBPAddresses[0]['State'],
                    "AddressType": "bo_BillTo",
                    "BPCode": localBPAddresses[0]['BPCode'],
                    "RowNum": 0
                },
                {
                    "AddressName": localBPAddresses[0]['AddressName'],
                    "Street": localBPAddresses[0]['Street'],
                    "Block": localBPAddresses[0]['Block'],
                    "ZipCode": localBPAddresses[0]['ZipCode'],
                    "City": localBPAddresses[0]['City'],
                    "Country": localBPAddresses[0]['Country'],
                    "State": localBPAddresses[0]['State'],
                    "AddressType": "bo_ShipTo",
                    "BPCode": localBPAddresses[0]['BPCode'],
                    "RowNum": 1
                }
            ]

            Series = 1
            if str(CardType) == "cSupplier":
                Series = 2

            bp_data = {
                "CardCode": CardCode,
                "CardName": request.data['CardName'],
                "Industry": request.data['Industry'],
                "Phone1": request.data['Phone1'],
                "Cellular": request.data['Phone1'], # can not be invalid mobile number
                "Website": request.data['Website'],
                "CardType": request.data['CardType'],
                "EmailAddress": request.data['EmailAddress'],
                "SalesPersonCode": request.data['SalesPersonCode'],
                "ContactPerson": request.data['ContactEmployees'][0]['Name'],
                "DiscountPercent": request.data['DiscountPercent'],
                # "Currency": request.data['Currency'],
                # "IntrestRatePercent": request.data['IntrestRatePercent'],
                # "CommissionPercent": request.data['CommissionPercent'],
                "PayTermsGrpCode": request.data['PayTermsGrpCode'],
                # "PriceListNum":PriceCategory,
                "BPBranchAssignment": 1, # branch need to be assign to BP
                "Series": Series,
                "BPFiscalTaxIDCollection": [
                    {
                        "TaxId0": "CVKPA5001K"
                    }
                ],
                "ContactEmployees": [
                {
                    "CardCode": CardCode,
                    "Name": request.data['ContactEmployees'][0]['Name'],
                    "MobilePhone": request.data['ContactEmployees'][0]['MobilePhone']
                }],
                
                "BPAddresses": SAPBPAddresses
            }

            #print(bp_data)
        
            res = settings.CALLAPI('post', '/BusinessPartners', 'api', bp_data)
            live = json.loads(res.text)
            #print("SAP Response: ", live)
            if "ContactEmployees" in live:
                #print("Success to create in SAP")
                InternalCode = live['ContactEmployees'][0]['InternalCode']
                BusinessPartner.objects.filter(pk = BpId).update(CardCode = live['CardCode'])
                BPEmployee.objects.filter(id=em.id).update(CardCode = live['CardCode'], InternalCode = InternalCode)
                BPBranch.objects.filter(BPID=BpId).update(BPCode = live['CardCode'])
                BPAddresses.objects.filter(BPID=BpId).update(BPCode = live['CardCode'])
                return Response({"message":"successful","status":200,"data":[{"bp_id":BpId, "CardCode":live['CardCode'], "bp_data": bp_data}]})
            else:
                #print("bp not create in sap")
                BusinessPartner.objects.filter(pk=BpId).delete()
                BPEmployee.objects.filter(U_BPID=BpId).delete()
                BPBranch.objects.filter(BPID=BpId).delete()
                BPAddresses.objects.filter(BPID=BpId).delete()
                #print(live['error']['message']['value'])
                SAP_MSG = live['error']['message']['value']
                return Response({"message":SAP_MSG,"SAP_error":SAP_MSG, "status":202,"data":[{"bp_data": bp_data}]})

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        # return Response({"message":"successful","status":"200","data":[]})
    except Exception as e:
        BusinessPartner.objects.filter(pk=BpId).delete()
        BPEmployee.objects.filter(U_BPID=BpId).delete()
        BPBranch.objects.filter(BPID=BpId).delete()
        BPAddresses.objects.filter(BPID=BpId).delete()
        return Response({"message":str(e),"status":"201","data":[]})

#BusinessPartner All API
@api_view(["GET"])
def all(request):
    try:
        # allbp = [];
        businesspartners_obj = BusinessPartner.objects.all().order_by("-id")[0:20]
        result = showBP(businesspartners_obj)
        return Response({"message": "Success","status": 200,"data":result})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

#BusinessPartner All API
@api_view(["GET"])
def all_old(request):    
    businesspartners_obj = BusinessPartner.objects.all().order_by("-id")
    for bp in businesspartners_obj:
        bpaddr = BPAddresses.objects.filter(BPID=bp.id)
        bpaddr_json = BPAddressesSerializer(bpaddr, many=True)
        
        jss = json.loads(json.dumps(bpaddr_json.data))
        bp.U_BPADDRESS = jss
        
    businesspartner_json = BusinessPartnerSerializer(businesspartners_obj, many=True)
    return Response({"message": "Success","status": 200,"data":businesspartner_json.data})

#BusinessPartner All API
@api_view(["GET"])
def all_bp(request):
    try:    
        businesspartners_obj = BusinessPartner.objects.all().values("id","CardName","CardCode","EmailAddress","Phone1","PayTermsGrpCode","CreditLimit","CreditLimitLeft")
        # businesspartners_json = BPSerializer(businesspartners_obj, many=True)
        result = showBPReport(businesspartners_obj)
        return Response({"message": "Success","status": 200,"data":result})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

#BusinessPartner All API
@api_view(["POST"])
def all_bp_filter(request):
    try:
        bpZone = request.data['bpZone']
        bpZoneArr = bpZone.split(",")
        businesspartners_obj = BusinessPartner.objects.filter(U_U_UTL_Zone__in = bpZoneArr).values("id","CardName","CardCode","EmailAddress","Phone1","PayTermsGrpCode","CreditLimit","CreditLimitLeft")
        # businesspartners_json = BPSerializer(businesspartners_obj, many=True)
        result = showBPReport(businesspartners_obj)
        return Response({"message": "Success","status": 200,"data":result})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
    

#BusinessPartner One API
@api_view(["POST"])
def one(request):
    # onebp = [];
    try:
        CardCode=request.data['CardCode']
        if CardCode != "":
            businesspartners_obj = BusinessPartner.objects.filter(CardCode = CardCode)
            result = showBP(businesspartners_obj)
            return Response({"message": "Success","status": 200,"data":result})
        else:
            return Response({"message": "Error","status": 201,"data":'Please Select CardCode'})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

#BusinessPartner Update API
@api_view(['POST'])
def update(request):
    fetchid = request.data['id']
    try:
        # added by millan for check existing business partner name exclude(pk=self.instance.pk).get(username=username)
        if BusinessPartner.objects.exclude(pk=fetchid).filter(CardName=request.data['CardName']).exists():
            return Response({"message":"CardName Already Exists","status":"409","data":[]})
        # added by millan for check existing business partner name
        else:
            if BusinessPartner.objects.filter(pk = fetchid).exists():
                model = BusinessPartner.objects.get(pk = fetchid)
                model.CardName = request.data['CardName']
                model.Industry = request.data['Industry']
                model.CardType = request.data['CardType']
                model.Website = request.data['Website']
                model.EmailAddress = request.data['EmailAddress']
                model.Phone1 = request.data['Phone1']
                model.DiscountPercent = request.data['DiscountPercent']
                model.Currency = request.data['Currency']
                model.IntrestRatePercent = request.data['IntrestRatePercent']
                model.CommissionPercent = request.data['CommissionPercent']
                model.Notes = request.data['Notes']
                model.PayTermsGrpCode = request.data['PayTermsGrpCode']
                model.CreditLimit = request.data['CreditLimit']
                model.AttachmentEntry = request.data['AttachmentEntry']
                model.SalesPersonCode = request.data['SalesPersonCode'] 
                model.ContactPerson = request.data['ContactEmployees'][0]['Name']
                # model.ContactPerson = request.data['ContactEmployees'][0]['FirstName']
                model.U_PARENTACC = request.data['U_PARENTACC']
                model.U_BPGRP = request.data['U_BPGRP']
                model.U_CONTOWNR = request.data['U_CONTOWNR']
                model.U_RATING = request.data['U_RATING']
                model.U_TYPE = request.data['U_TYPE']
                model.U_ANLRVN = request.data['U_ANLRVN']
                model.U_CURBAL = request.data['U_CURBAL']
                model.U_ACCNT = request.data['U_ACCNT']
                model.U_INVNO = request.data['U_INVNO']
                model.U_LAT = request.data['U_LAT']
                model.U_LONG = request.data['U_LONG']
                model.CreateDate = request.data['CreateDate']
                model.CreateTime = request.data['CreateTime']
                model.UpdateDate = request.data['UpdateDate']
                model.UpdateTime = request.data['UpdateTime']
                model.GroupType = request.data['GroupType']
                model.CustomerType = request.data['CustomerType']
                model.PriceCategory = request.data['PriceCategory']
                model.PaymantMode = request.data['PaymantMode']
                model.DeliveryMode = request.data['DeliveryMode']
                model.Turnover = request.data['Turnover']
                # new keys
                model.TCS = request.data['TCS']
                model.Link = request.data['Link']
                model.BeneficiaryName = request.data['BeneficiaryName']
                model.BankName = request.data['BankName']
                model.ACNumber = request.data['ACNumber']
                model.IfscCode = request.data['IfscCode']
                model.Unit = request.data['Unit']
                model.FreeDelivery = request.data['FreeDelivery']
                model.save()
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #
                #
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                if BPAddresses.objects.filter(BPID = model.id).exists():
                    model_add = BPAddresses.objects.get(BPID = model.id)
                    model_add.AddressName = request.data['BPAddresses'][0]['AddressName']
                    model_add.Street = request.data['BPAddresses'][0]['Street']
                    model_add.Block = request.data['BPAddresses'][0]['Block']
                    model_add.City = request.data['BPAddresses'][0]['City']
                    model_add.State = request.data['BPAddresses'][0]['State']
                    model_add.ZipCode = request.data['BPAddresses'][0]['ZipCode']
                    model_add.Country = request.data['BPAddresses'][0]['Country']
                    model_add.U_SHPTYP = request.data['BPAddresses'][0]['U_SHPTYP']
                    model_add.U_COUNTRY = request.data['BPAddresses'][0]['U_COUNTRY']
                    model_add.U_STATE = request.data['BPAddresses'][0]['U_STATE']
                    model_add.save()
                else:
                    # BP Address
                    bpadd = request.data['BPAddresses'][0]
                    model_add = BPAddresses(BPID=model.id, AddressName = bpadd['AddressName'], Street = bpadd['Street'], Block = bpadd['Block'], ZipCode = bpadd['ZipCode'], City = bpadd['City'], Country = bpadd['Country'], AddressType = bpadd['AddressType'], RowNum=0, BPCode = model.CardCode, U_STATE = bpadd['U_STATE'], State = bpadd['State'], U_COUNTRY = bpadd['U_COUNTRY'], U_SHPTYP = bpadd['U_SHPTYP'], District = bpadd['District'])
                    model_add.save()

                    # BP Branch
                    model_br = BPBranch(BPID=model.id, BranchName=model.CardName, AddressName = bpadd['AddressName'], Street = bpadd['Street'], Block = bpadd['Block'], ZipCode = bpadd['ZipCode'], City = bpadd['City'], Country = bpadd['Country'], AddressType = bpadd['AddressType'], RowNum=1, BPCode = model.CardCode, U_STATE = bpadd['U_STATE'], Default=1, State = bpadd['State'], U_COUNTRY = bpadd['U_COUNTRY'], U_SHPTYP = bpadd['U_SHPTYP'], CreateDate = request.data['CreateDate'], CreateTime = request.data['CreateTime'], UpdateDate = request.data['UpdateDate'], UpdateTime =  request.data['UpdateTime'], District = bpadd['District'])
                    model_br.save()
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #
                #
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                bpemp = BPEmployee.objects.get(InternalCode = request.data['ContactEmployees'][0]['InternalCode'])
                #print(bpemp)
                bpemp.MobilePhone = request.data['ContactEmployees'][0]['MobilePhone'] 
                bpemp.FirstName = request.data['ContactEmployees'][0]['Name']
                # bpemp.FirstName = request.data['ContactEmployees'][0]['FirstName']
                bpemp.E_Mail = request.data['ContactEmployees'][0]['E_Mail']
                bpemp.UpdateDate = request.data['UpdateDate']
                bpemp.UpdateTime = request.data['UpdateTime']
                bpemp.save()        
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #
                #
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                if BPBranch.objects.filter(BPCode = model.CardCode, Default=1).exists():
                    model_br = BPBranch.objects.get(BPCode = model.CardCode, Default=1)
                    model_br.Default=0
                    model_br.save()
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #
                #
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                bp_data = {
                    "CardCode": model.CardCode,
                    "CardName": request.data['CardName'],
                    "Industry": request.data['Industry'],
                    "Phone1": request.data['Phone1'],
                    "Cellular": request.data['Phone1'], # can not be invalid mobile number
                    "Website": request.data['Website'],
                    "CardType": request.data['CardType'],
                    "EmailAddress": request.data['EmailAddress'],
                    "SalesPersonCode": request.data['SalesPersonCode'],
                    "ContactPerson": request.data['ContactEmployees'][0]['Name'],
                    "DiscountPercent": request.data['DiscountPercent'],
                    "Currency": request.data['Currency'],
                    "IntrestRatePercent": request.data['IntrestRatePercent'],
                    "CommissionPercent": request.data['CommissionPercent'],
                    "PayTermsGrpCode": request.data['PayTermsGrpCode'],
                    # "PriceListNum":request.data['PriceCategory'],
                    "BPBranchAssignment": 1, # branch need to be assign to BP
                    "ContactEmployees": [{
                        "InternalCode": request.data['ContactEmployees'][0]['InternalCode'],
                        "Name": request.data['ContactEmployees'][0]['Name'],
                        "MobilePhone": request.data['ContactEmployees'][0]['MobilePhone'],
                        "E_Mail": request.data['ContactEmployees'][0]['E_Mail']
                    }],
                    "BPAddresses": [{
                        "BPCode": request.data['BPAddresses'][0]['BPCode'],
                        "RowNum": request.data['BPAddresses'][0]['RowNum'],
                        "AddressType": "bo_BillTo",
                        "AddressName": request.data['BPAddresses'][0]['AddressName'],
                        "Block": request.data['BPAddresses'][0]['Block'],
                        "Street": request.data['BPAddresses'][0]['Street'],
                        "ZipCode": request.data['BPAddresses'][0]['ZipCode'],
                        "City": request.data['BPAddresses'][0]['City'],
                        "State": request.data['BPAddresses'][0]['State'],
                        "Country": request.data['BPAddresses'][0]['Country']
                    }]
                }
                
                res = settings.CALLAPI('patch', "/BusinessPartners('"+model.CardCode+"')", 'api', bp_data)
                if len(res.content) !=0 :
                    res1 = json.loads(res.content)
                    SAP_MSG = res1['error']['message']['value']
                    return Response({"message":SAP_MSG,"status":202,"SAP_error":SAP_MSG, "data":[{"bp_data": bp_data}]})
                else:
                    return Response({"message":"successful","status":200, "data":[{"bp_data": bp_data}]})
            else:
                return Response({"message":"Invalid BP","status":201, "data":[]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

#BusinessPartner delete
@api_view(['POST'])
def delete(request):
    fetchid=request.data['id']
    try:
        bp=BusinessPartner.objects.get(pk=fetchid)
        fetchdata = BusinessPartner.objects.filter(pk = fetchid).delete()
        addr      = BPAddresses.objects.filter(BPID = fetchid).delete()
        bpem      = BPEmployee.objects.filter(U_BPID = fetchid).delete()
        bpbr      = BPBranch.objects.filter(BPID = fetchid).delete()
        return Response({"message":"successful","status":"200","data":[]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

#BusinessPartner update_lat_long
@api_view(['POST'])
def update_lat_long(request):
    try:
        BPId   = request.data['id']
        U_LAT  = request.data['U_LAT']
        U_LONG = request.data['U_LONG']

        if BusinessPartner.objects.filter(pk = BPId).exists():
            bpModel = BusinessPartner.objects.get(pk = BPId)
            bpModel.U_LAT = U_LAT
            bpModel.U_LONG = U_LONG
            bpModel.save()

            return Response({"message":"successful","status":"200","data":[]})
        else:
            return Response({"message":"Invalid","status":"201","data":[]})

    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> BP Type >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# create BP type
@api_view(['POST'])
def createtype(request):
    try:
        Type = request.data['Type']
        oppTypeObj = BPType(Type = Type).save()
        oppTypeId = BPType.objects.latest('id')

        return Response({"message":"successful","status":200, "data":[{"TypeId": oppTypeId.id}]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

# create BP type
@api_view(['GET'])
def alltype(request):
    try:
        oppTypeObj = BPType.objects.all().order_by('-Type')
        oppTypeJson = BPTypeSerializer(oppTypeObj, many=True)
        return Response({"message":"successful","status":200, "data":oppTypeJson.data})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})


def showBPReport(objs):
    allbp = []
    for obj in objs:
        CardCode = obj['CardCode']
        PayTermsGrpCode = obj['PayTermsGrpCode']
        CreditLimit = obj['CreditLimit']
        # ptgcObj = PaymentTermsTypes.objects.filter(GroupNumber = PayTermsGrpCode).first()
        # creditLimitDayes = ptgcObj['PaymentTermsGroupName']

        GSTIN = ""
        BPAddress = ""
        if BPBranch.objects.filter(BPCode = CardCode).exists():
            bpBranch = BPBranch.objects.filter(BPCode = CardCode).first()
            GSTIN = str(bpBranch.GSTIN)
            BPAddress = f"{bpBranch.Street} {bpBranch.City} {bpBranch.ZipCode}"

        # GroupName = ""
        # if BusinessPartnerGroups.objects.filter(Code = obj['GroupCode']).exists():
        #     bpGroup = BusinessPartnerGroups.objects.filter(Code = obj['GroupCode']).first()
        #     GroupName = bpGroup.Name

        finalBpData = {
            "CardName": obj['CardName'],
            "CardCode": obj['CardCode'],
            "EmailAddress": obj['EmailAddress'],
            "Phone1": obj['Phone1'],
            "GSTIN": GSTIN,
            "BPAddress": BPAddress,
            # "GroupName": GroupName,
            "CreditLimit": CreditLimit,
            "CreditLimitLeft": obj['CreditLimitLeft'],
            # "CreditLimitDayes": creditLimitDayes,
        }
        allbp.append(finalBpData)
    return allbp

# to get object of business_partner salesPersonCode, PaymentTerms and Business Type
def showBP(objs):
    allbp = [];
    for obj in objs:
        #print(obj.U_TYPE)
        bpType = obj.U_TYPE
        cardCodeType=obj.CardCode
        paymentType = obj.PayTermsGrpCode
        salesPersonType = obj.SalesPersonCode
        createdBy = obj.CreatedBy
        Unit = obj.Unit

        bpjson = BusinessPartnerSerializer(obj)
        finalBpData = json.loads(json.dumps(bpjson.data))

        # Business Partner GroupCode
        if BusinessPartnerGroups.objects.filter(Code = obj.GroupCode).exists():
            bpGroup = BusinessPartnerGroups.objects.filter(Code = obj.GroupCode).first()
            finalBpData['GroupName'] = bpGroup.Name
        else:
            finalBpData['GroupName'] = ""

        # # Business Credit Limit by payment termstype
        # if PaymentTermsTypes.objects.filter(GroupNumber = obj.PayTermsGrpCode).exists():
        #     ptgcObj = PaymentTermsTypes.objects.filter(GroupNumber = obj.PayTermsGrpCode).first()
        #     finalBpData['CreditLimitDayes'] = ptgcObj.PaymentTermsGroupName
        # else:
        #     finalBpData['CreditLimitDayes'] = ""

        # BP branch
        if Branch.objects.filter(BPLId = Unit).exists():
            unitObj = Branch.objects.get(BPLId = Unit)
            finalBpData['UnitName'] = unitObj.BPLName
        else:
            finalBpData['UnitName'] = ""
        
        # BP type 
        if bpType != "":
            bpTypeObj = BPType.objects.filter(pk = bpType)
            bpTypejson = BPTypeSerializer(bpTypeObj, many = True)
            finalBpData['U_TYPE']=json.loads(json.dumps(bpTypejson.data))
        else:
            finalBpData['U_TYPE'] = []
            
        if paymentType != "":
            paymentTypeObj = PaymentTermsTypes.objects.filter(GroupNumber = paymentType)
            paymentjson = PaymentTermsTypesSerializer(paymentTypeObj, many = True)
            finalBpData['PayTermsGrpCode'] = json.loads(json.dumps(paymentjson.data))
        else:
            finalBpData['PayTermsGrpCode'] = []
            
        if salesPersonType != "":
            salesPersonObj = Employee.objects.filter(SalesEmployeeCode = salesPersonType).values("id","SalesEmployeeName", "SalesEmployeeCode")
            salesjson = EmployeeSerializer(salesPersonObj, many =True)
            finalBpData['SalesPersonCode'] = json.loads(json.dumps(salesjson.data))
        else:
            finalBpData['SalesPersonCode'] = []
        
        if createdBy != "":
            salesPersonObj = Employee.objects.filter(SalesEmployeeCode = createdBy).values("id","SalesEmployeeName", "SalesEmployeeCode")
            salesjson = EmployeeSerializer(salesPersonObj, many =True)
            finalBpData['CreatedBy'] = json.loads(json.dumps(salesjson.data))
        else:
            finalBpData['CreatedBy'] = []
        
        #print("cardCodeType: ", cardCodeType)
        if cardCodeType != "":
            cardObj = BPEmployee.objects.filter(U_BPID = obj.id).values("id","FirstName", "CardCode", "InternalCode", "MobilePhone", "E_Mail")
            cardjson = BPEmployeeSerializer(cardObj, many = True)
            finalBpData['ContactEmployees'] = json.loads(json.dumps(cardjson.data))
        else:
            finalBpData['ContactEmployees'] = []
            
        if cardCodeType != "":
            bpaddr = BPAddresses.objects.filter(BPID=obj.id)
            bpaddr_json = BPAddressesSerializer(bpaddr, many=True)
            jss0 = json.loads(json.dumps(bpaddr_json.data))
            
            bpbr = BPBranch.objects.filter(BPID=obj.id)
            bpbr_json = BPBranchSerializer(bpbr, many=True)
            jss1 = json.loads(json.dumps(bpbr_json.data))
            finalBpData['BPAddresses'] = jss0 + jss1
        else:
            finalBpData['BPAddresses'] = []
        
        allbp.append(finalBpData)
    return allbp
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#added by millan on 08-September-2022
#bp selected fields api
@api_view(["GET"])
def get_bp(request):
    try: 
        businesspartners_obj = BusinessPartner.objects.all().values("CardName", "EmailAddress", "Phone1", "id", "CardCode", "PriceCategory")
        bp_obj = BusinessPartnerSerializer(businesspartners_obj, many=True)
        finalBP = json.loads(json.dumps(bp_obj.data))
        return Response({"message": "Success","status": 200,"data":finalBP})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#added by millan on 03-October-2022 for adding attachment and description
@api_view(["POST"])
def bp_attachment_create(request):
    try:
        cust_id = request.data['cust_id']
        CreateDate = request.data['CreateDate']
        CreateTime = request.data['CreateTime']
        #print(request.FILES)
        #print(request.FILES.getlist('Attach'))
        for File in request.FILES.getlist('Attach'):
            attachmentsImage_url = ""
            target ='./bridge/static/image/BPAttachment'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+File.name, File)
            file_size = os.stat(file)
            Size = file_size.st_size
            productImage_url = fss.url(file)
            attachmentsImage_url = productImage_url.replace('/bridge', '')
            #print(attachmentsImage_url)

            att=Attachment(File=attachmentsImage_url, CustId=cust_id, CreateDate=CreateDate, CreateTime=CreateTime, Size=Size)
            
            att.save()  
            
        return Response({"message": "success","status": 200,"data":[]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#for updating attachment
@api_view(['POST'])
def bp_attachment_update(request):
    try:
        cust_id = request.data['cust_id']
        fetchid = request.data['id']
        
        File = request.data['Attach']
        
        model = Attachment.objects.get(pk = fetchid, CustId=cust_id)
        
        model.UpdateDate = request.data['UpdateDate']
        model.UpdateTime = request.data['UpdateTime']

        attechmentsImage_url = ""
        if File:
            target ='./bridge/static/image/BPAttachment'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+File.name, File)
            file_size = os.stat(file)
            Size = file_size.st_size
            productImage_url = fss.url(file)
            attechmentsImage_url = productImage_url.replace('/bridge', '')
            #print(attechmentsImage_url)
            model.File = attechmentsImage_url
            model.Size = Size
        else:
            model.File= model.File
            #print('no image')
        
        model.save()
        
        return Response({"message": "success","status": 200,"data":[]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#for deleting an attachment
@api_view(['POST'])
def bp_attachment_delete(request):
    try:
        fetchid = request.data['id']
        
        cust_id = request.data['cust_id']
        
        if Attachment.objects.filter(pk=fetchid, CustId=cust_id).exists():
            
            Attachment.objects.filter(pk=fetchid, CustId=cust_id).delete()
            
            return Response({"message":"successful","status":"200","data":[]})
        else:
            return Response({"message":"ID Not Found","status":"201","data":[]})
        
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#get all attachment based on customer_id
@api_view(["POST"])
def bp_attachments(request):
    try:
        cust_id=request.data['cust_id']
        if cust_id > 0:
            bpAttachObj = Attachment.objects.filter(CustId = cust_id)
            
            bpAttachjson = BPAttachmentSerilaizer(bpAttachObj, many = True)
            
            return Response({"message": "Success","status": 200,"data":bpAttachjson.data})
        else:
            return Response({"message": "Customer ID Not Found","status": 201,"data":[]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#added by millan on 06-10-2022 to get sales of each particular month based on card code
@api_view(["POST"])
def monthlySales(request):
    try:
        CardCode = request.data['CardCode']
        monSales = []
        if Order.objects.filter(CardCode = CardCode).exists:
            sql_query = f"SELECT id, SUM(DocTotal) MonthlyTotal, CreateDate, SUBSTR(CreateDate,1,7) as mon FROM `order_order` where CardCode ='{CardCode}' GROUP BY mon"
            monsl = Order.objects.raw(sql_query)
            for desc in monsl:
                crDate = desc.mon.split('-')
                monSales.append({"MonthlySales":desc.MonthlyTotal, "Year":crDate[0], "Month":crDate[1]})
        
            return Response({"message": "success","status": 200,"data":monSales})
        else:
            return Response({"message": "Card Code Not Found","status": 201,"data":[]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#added by millan on 14-10-2022 to get sales of each particular month based on card code
@api_view(["POST"])
def top5Activity(request):
    try:
        Emp = request.data['Emp']

        empIds = getAllReportingToUserId(Emp)

        todays_date = date.today()
        cur_day = todays_date.day
        fif_day = cur_day + 5
        top5Act = []
        #print("cur_day:", cur_day, "fif_day:", fif_day)
        if Activity.objects.filter(Emp__in = empIds).exists():
            strEmpIds = ""
            for id in empIds:
                strEmpIds = strEmpIds+","+str(id)
            # sql_query = f"SELECT * FROM `Activity_activity` where Emp = {Emp} and (SUBSTR(CreateDate, 9, 10)) BETWEEN {cur_day} AND {fif_day} LIMIT 5"
            sql_query = f"SELECT * FROM `Activity_activity` where Emp in({strEmpIds[1:]}) and (SUBSTR(CreateDate, 8, 9)) BETWEEN {cur_day} AND {fif_day} LIMIT 5"
            #print(sql_query)
            top5sl = Activity.objects.raw(sql_query)
            top5Act = ActivitySerializer(top5sl, many=True).data
        
        return Response({"message": "Success","status": 200,"data":top5Act})
        # else:
        #     return Response({"message": "Invalid Employee id","status": 201,"data":[]})                
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# update BP Credit Limit
@api_view(['GET'])
def updatebpcreditlimit(request):
    try:
        skip=0
        todayDate = date.today() - timedelta(days=10)
        #print(todayDate)
        while skip != "":
            bpUrl = f"/BusinessPartners?$select = CardCode,CreditLimit,CurrentAccountBalance,OpenDeliveryNotesBalance,OpenOrdersBalance,OpenChecksBalance&$filter = UpdateDate ge '{todayDate}'"
            res = settings.CALLAPI('get', bpUrl, 'api', '')
            #print(bpUrl)
            resData = json.loads(res.text)
            if 'odata.nextLink' in resData:
                nextLink = resData['odata.nextLink']
                #print(">>>>>>>>>>>>>>>>>>>>> nextLink: ", nextLink)
                nextLink = nextLink.split("=")
                skip = nextLink[2]
            else:
                #print("nextLink: ", "")
                skip = ""

            for obj in resData['value']:
                CardCode = obj['CardCode']
                if BusinessPartner.objects.filter(CardCode = CardCode).exists():
                    bpObj = BusinessPartner.objects.filter(CardCode = CardCode).first()
                    #print("CardName", bpObj.CardName)
                    updatedCreditLimit = float(obj['CreditLimit'])
                    CurrentAccountBalance = obj['CurrentAccountBalance']
                    OpenDeliveryNotesBalance = obj['OpenDeliveryNotesBalance']
                    OpenOrdersBalance = obj['OpenOrdersBalance']
                    OpenChecksBalance = obj['OpenChecksBalance'] # not in currently used

                    totalCreditLimitUsed = float(float(CurrentAccountBalance) + float(OpenDeliveryNotesBalance) + float(OpenOrdersBalance))
                    newLeftCreditLimit = float(updatedCreditLimit - totalCreditLimitUsed)
                    BusinessPartner.objects.filter(CardCode = CardCode).update(
                        CreditLimit = updatedCreditLimit, 
                        CreditLimitLeft = newLeftCreditLimit,
                        CurrentAccountBalance = CurrentAccountBalance,
                        OpenDeliveryNotesBalance = OpenDeliveryNotesBalance,
                        OpenOrdersBalance = OpenOrdersBalance,
                        OpenChecksBalance = OpenChecksBalance
                    )
                else:
                    #print("CardCode", CardCode)
                    pass

        return Response({"message":"Successful","status":200, "data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"Model": "BP" ,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# update BP Credit Limit by BP
@api_view(['POST'])
def updatebpcreditlimitbybp(request):
    try:
    # if True:
        CardCode = request.data['CardCode']
        if BusinessPartner.objects.filter(CardCode = CardCode).exists():
            res = settings.CALLAPI('get', f"/BusinessPartners('{CardCode}')", 'api', '')
            resData = json.loads(res.text)
            if 'odata.metadata' in resData:
                #print("CreditLimit: ", resData['CreditLimit'])
                bpObj = BusinessPartner.objects.get(CardCode = CardCode)

                updatedCreditLimit = float(resData['CreditLimit'])
                CurrentAccountBalance = resData['CurrentAccountBalance']
                OpenDeliveryNotesBalance = resData['OpenDeliveryNotesBalance']
                OpenOrdersBalance = resData['OpenOrdersBalance']
                OpenChecksBalance = resData['OpenChecksBalance'] # not in currently used

                totalCreditLimitUsed = float(float(CurrentAccountBalance) + float(OpenDeliveryNotesBalance) + float(OpenOrdersBalance))
                newLeftCreditLimit = float(updatedCreditLimit - totalCreditLimitUsed)

                BusinessPartner.objects.filter(CardCode = CardCode).update(
                    CreditLimit = updatedCreditLimit, 
                    CreditLimitLeft = newLeftCreditLimit,
                    CurrentAccountBalance = CurrentAccountBalance,
                    OpenDeliveryNotesBalance = OpenDeliveryNotesBalance,
                    OpenOrdersBalance = OpenOrdersBalance,
                    OpenChecksBalance = OpenChecksBalance
                )

                context = {
                    "CreditLimit": updatedCreditLimit,
                    "CreditLimitLeft": newLeftCreditLimit,
                }
            return Response({"message":"Successful","status":200, "data":[context]})
        else:
            return Response({"message":"Invalid BP CardCode","status":201, "data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"Model": "BP" ,"data":[]})
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#BusinessPartner All API
@api_view(["POST"])
def all_filter(request):
    try:
        SalesPersonCode = request.data['SalesPersonCode']
        result = []
        if Employee.objects.filter(SalesEmployeeCode = SalesPersonCode).exists():
            empObj = Employee.objects.get(SalesEmployeeCode = SalesPersonCode)
            empUnit = int(empObj.unit)
            if str(empObj.role) == 'Sales Executive':
                #print("in if: ", empUnit)
                businesspartners_obj = BusinessPartner.objects.filter(Q(SalesPersonCode = SalesPersonCode) | Q(CreatedBy = SalesPersonCode)).exclude(Link = 'Commission Agent').order_by("-id")[0:20]
                result = showBP(businesspartners_obj)
            # elif empUnit == 'Central Level':
            elif empUnit == 2:
                #print("in elif: ", empUnit)
                businesspartners_obj = BusinessPartner.objects.all().exclude(Link = 'Commission Agent').order_by("-id")[0:20]
                result = showBP(businesspartners_obj)
            else:
                #print("in else: ", empUnit)
                allEmp = getAllReportingToIds(SalesPersonCode)
                #print("getAllReportingToIds: ", allEmp)
                businesspartners_obj = BusinessPartner.objects.filter(Q(SalesPersonCode__in = allEmp) | Q(CreatedBy__in = allEmp)).exclude(Link = 'Commission Agent').order_by("-id")[0:20]
                result = showBP(businesspartners_obj)
        else:
            return Response({"message": "Invalid SalesPersonCode?","status": 201,"data":[]})
        return Response({"message": "Success","status": 200,"data":result})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#BusinessPartner All API
@api_view(["POST"])
def all_filter_pagination(request):
    try:
        SalesPersonCode = request.data['SalesPersonCode']
        PageNo = request.data['PageNo']
        MaxSize = request.data['MaxSize']
        SearchText = request.data['SearchText']
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        OrderByName = "a-z" #a-z/z-a
        if 'OrderByName' in request.data:
            OrderByName = str(request.data['OrderByName']).strip()
        orderby = "CardCode"
        if str(OrderByName) == 'z-a':
            orderby = "-CardCode"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        if Employee.objects.filter(SalesEmployeeCode = SalesPersonCode).exists():

            # allEmp = getAllReportingToIds(SalesPersonCode)
            zones = getZoneByEmployee(SalesPersonCode)
            #print("getAllReportingToIds: ", allEmp)
            TotalBP = 0

            businesspartners_obj = []
            if str(SearchText).strip() != "":
                businesspartners_obj = BusinessPartner.objects.filter( Q(U_U_UTL_Zone__in = zones) & Q( Q(CardCode__icontains = SearchText) | Q(CardName__icontains = SearchText) | Q(EmailAddress__icontains = SearchText) | Q(CustomerType__icontains = SearchText) | Q(Phone1__icontains = SearchText) ) ).exclude(Link = 'Commission Agent').order_by(orderby)
            else:
                businesspartners_obj = BusinessPartner.objects.filter( Q(U_U_UTL_Zone__in = zones)).exclude(Link = 'Commission Agent').order_by(orderby)

            TotalBP = len(businesspartners_obj)

            if MaxSize != "All":
                page_obj = Pagination.objects.filter(MaxSize=MaxSize).first()
                size = int(page_obj.MaxSize)
                endWith = (PageNo * size)
                startWith = (endWith - size)
                businesspartners_obj = businesspartners_obj[startWith:endWith]

            result = showBP(businesspartners_obj)
            return Response({"message": "Success","status": 200, "TotalBP": TotalBP, "data":result})
        else:
            return Response({"message": "Invalid SalesPersonCode?","status": 201,"data":[]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Groups
@api_view(["GET"])
def all_bp_groupcode(request):
    try:
        groupCodeObj = BusinessPartnerGroups.objects.all().order_by('Name')
        groupCodeJson = BusinessPartnerGroupsSerilaizer(groupCodeObj, many=True)
        return Response({"message": "Success","status": 200, "data":groupCodeJson.data})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# zones
@api_view(["GET"])
def all_bp_zones(request):
    try:
        zoneObj = BusinessPartnerZone.objects.all().order_by('Name')
        zoneJson = BusinessPartnerZoneSerilaizer(zoneObj, many=True)
        return Response({"message": "Success","status": 200, "data":zoneJson.data})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# bp list with total purchase
# @api_view(['POST'])
# def filter_ledger_dashboard(request):
#     # try:
#         print("filter_ledger_dashboard", request.data)
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         Filter = request.data['Filter']
#         SalesType = request.data['Type']
#         FromDate = request.data['FromDate']
#         ToDate = request.data['ToDate']
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         SalesPersonCode = -1
#         if 'SalesPersonCode' in request.data:
#             SalesPersonCode = request.data['SalesPersonCode']
#         zones = getZoneByEmployee(SalesPersonCode)
#         zonesStr = "','".join(zones)
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         SearchText = ""
#         if 'SearchText' in request.data:
#             SearchText = request.data['SearchText']
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         OrderByName = "a-z" #a-z/z-a
#         OrderByAmt = "asc" #desc
#         if 'OrderByName' in request.data:
#             OrderByName = str(request.data['OrderByName']).strip()
#         if 'OrderByAmt' in request.data:
#             OrderByAmt = str(request.data['OrderByAmt']).strip()
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         orderby = ""
#         if str(OrderByName).lower() == 'a-z':
#             orderby = "Order By GroupName asc"
#         elif str(OrderByName).lower() == 'z-a':
#             orderby = "Order By GroupName desc"
#         elif str(OrderByAmt).lower() == 'asc':
#             orderby = "Order By DocTotal asc"
#         elif str(OrderByAmt).lower() == 'desc':
#             orderby = "Order By DocTotal desc"
#         else:
#             orderby = "Order By GroupName asc"
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
#         mycursor = mydb.cursor(dictionary=True, buffered=True)
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         fromToDate = ""
#         if str(FromDate) != "":
#             fromToDate = f"AND inv.DocDate >= '{FromDate}' AND inv.DocDate <= '{ToDate}'"
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         sqlQuery = ""
#         if str(Filter).lower() == 'group':
#             SearchQuery = ''
#             if str(SearchText) != '':
#                 SearchQuery = f"AND (bpgroup.Name like '%%{SearchText}%%' OR bpgroup.Code like '%%{SearchText}%%')"
#             if str(SalesType).lower() == "gross":
#                 sqlQuery = f"""
#                     SELECT
#                         bp.GroupCode,
#                         IFNULL(bpgroup.Name, '') as GroupName,
#                         IFNULL(SUM(inv.DocTotal), 0) AS `DocTotal`,
#                         IFNULL(SUM(inv.PaidToDateSys), 0) AS `PaidToDateSys`,
#                         IFNULL(SUM(inv.DocTotal - inv.PaidToDateSys), 0) AS `PendingTotal`
#                     FROM BusinessPartner_businesspartner bp
#                     LEFT JOIN BusinessPartner_businesspartnergroups bpgroup ON bpgroup.Code = bp.GroupCode
#                     LEFT JOIN Invoice_invoice inv ON bp.CardCode = inv.CardCode
#                     WHERE 
#                         inv.CancelStatus = 'csNo'
#                         AND bp.U_U_UTL_Zone IN('{zonesStr}')
#                         {SearchQuery}
#                         {fromToDate}
#                     GROUP BY bp.GroupCode {orderby}
#                 """
#             else:
#                 sqlQuery = f"""
#                     SELECT
#                         bp.GroupCode,
#                         IFNULL(bpgroup.Name, '') as GroupName,
#                         IFNULL(SUM(A.DocTotal), 0) AS 'DocTotal',
#                         IFNULL(SUM(A.NetTotal), 0) AS 'NetTotal',
#                         IFNULL(SUM(A.PaidToDateSys), 0) AS `PaidToDateSys`,
#                         IFNULL(SUM(A.DocTotal - A.PaidToDateSys), 0) AS `PendingTotal`
#                     FROM BusinessPartner_businesspartner bp
#                     LEFT JOIN BusinessPartner_businesspartnergroups bpgroup ON bpgroup.Code = bp.GroupCode
#                     INNER JOIN (
#                         SELECT
#                             inv.CardCode,
#                             inv.id,
#                             inv.DocTotal,
#                             inv.PaidToDateSys,
#                             IFNULL(SUM(INVLine.LineTotal), 0) AS LineTotal,
#                             IFNULL(
#                                 SUM(CASE
#                                     WHEN inv.DiscountPercent != 0.0 THEN INVLine.LineTotal - (INVLine.LineTotal * inv.DiscountPercent / 100)
#                                     ELSE INVLine.LineTotal
#                                 END), 0
#                             ) AS NetTotal
#                         FROM Invoice_invoice inv
#                         LEFT JOIN Invoice_documentlines INVLine ON INVLine.InvoiceID = inv.id
#                         WHERE 
#                             inv.CancelStatus = 'csNo'
#                             {fromToDate}
#                         GROUP BY inv.CardCode, inv.id
#                     ) A ON bp.CardCode = A.CardCode
#                     WHERE 
#                         bp.U_U_UTL_Zone IN('{zonesStr}')
#                         {SearchQuery}
#                     GROUP BY bp.GroupCode, GroupName;
#                 """
#         else:
#             SearchQuery = ''
#             if str(SearchText) != '':
#                 SearchQuery = f"AND (bp.U_U_UTL_Zone like '%%{SearchText}%%')"

#             if str(SalesType).lower() == "gross":
#                 sqlQuery = f"""
#                     SELECT 
#                         bp.U_U_UTL_Zone as GroupCode,
#                         bp.U_U_UTL_Zone as GroupName, 
#                         IFNULL(SUM(inv.DocTotal), 0) AS `DocTotal`, 
#                         IFNULL(SUM(inv.PaidToDateSys), 0) AS `PaidToDateSys`, 
#                         IFNULL(SUM(inv.DocTotal - inv.PaidToDateSys), 0) AS `PendingTotal` 
#                     FROM BusinessPartner_businesspartner bp 
#                     LEFT JOIN Invoice_invoice inv ON bp.CardCode = inv.CardCode 
#                     WHERE 
#                         inv.CancelStatus = 'csNo'
#                         AND bp.U_U_UTL_Zone IN('{zonesStr}')
#                         {SearchQuery}
#                         {fromToDate}
#                     GROUP BY bp.U_U_UTL_Zone {orderby}
#                 """
#             else:
#                 sqlQuery = f"""
#                     SELECT
#                         bp.U_U_UTL_Zone as GroupCode,
#                         bp.U_U_UTL_Zone as GroupName, 
#                         IFNULL(SUM(A.DocTotal), 0) AS 'DocTotal',
#                         IFNULL(SUM(A.NetTotal), 0) AS 'NetTotal',
#                         IFNULL(SUM(A.PaidToDateSys), 0) AS `PaidToDateSys`,
#                         IFNULL(SUM(A.DocTotal - A.PaidToDateSys), 0) AS `PendingTotal`
#                     FROM BusinessPartner_businesspartner bp
#                     LEFT JOIN BusinessPartner_businesspartnergroups bpgroup ON bpgroup.Code = bp.GroupCode
#                     INNER JOIN (
#                         SELECT
#                             inv.CardCode,
#                             inv.id,
#                             inv.DocTotal,
#                             inv.PaidToDateSys,
#                             IFNULL(SUM(INVLine.LineTotal), 0) AS LineTotal,
#                             IFNULL(
#                                 SUM(CASE
#                                     WHEN inv.DiscountPercent != 0.0 THEN INVLine.LineTotal - (INVLine.LineTotal * inv.DiscountPercent / 100)
#                                     ELSE INVLine.LineTotal
#                                 END), 0
#                             ) AS NetTotal
#                         FROM Invoice_invoice inv
#                         LEFT JOIN Invoice_documentlines INVLine ON INVLine.InvoiceID = inv.id
#                         WHERE 
#                             inv.CancelStatus = 'csNo'
#                             {fromToDate}
#                         GROUP BY inv.CardCode, inv.id
#                     ) A ON bp.CardCode = A.CardCode
#                     WHERE 
#                         bp.U_U_UTL_Zone IN('{zonesStr}')
#                         {SearchQuery}
#                     GROUP BY bp.U_U_UTL_Zone {orderby}
#                 """

#         print(sqlQuery)
#         mycursor.execute(sqlQuery)
#         groupData = mycursor.fetchall()

#         # return Response({"message": "Success","status": 200, "data":groupData})

#         print("Code list count", len(groupData))
#         if 'PageNo' in request.data:
#             PageNo = int(request.data['PageNo'])
#             MaxSize = request.data['MaxSize']
#             if MaxSize != "All":
#                 size = int(MaxSize)
#                 endWith = (PageNo * size)
#                 startWith = (endWith - size)
#                 groupData = groupData[startWith:endWith]

#         totalSales = 0
#         totalPayments = 0
#         totalPendings = 0
#         dataContext = []
#         for groupObj in groupData:
#             GroupCode     = groupObj['GroupCode']
#             GroupName     = groupObj['GroupName']
#             DocTotal      = groupObj['DocTotal']
#             PaidToDateSys = groupObj['PaidToDateSys']
#             PendingTotal  = groupObj['PendingTotal']

#             if str(SalesType).lower() == "net":
#                 DocTotal = groupObj['NetTotal']

#             bpData = {
#                 "GroupName": GroupName,
#                 "GroupCode": GroupCode,
#                 "TotalSales": round(DocTotal, 2)
#             }
#             dataContext.append(bpData)
#             totalSales = float(totalSales) + float(DocTotal)
#             totalPayments = float(totalPayments) + float(PaidToDateSys)
#             totalPendings = float(totalPendings) + float(PendingTotal)


#         TotalSales = totalSales
#         TotalReceivePayment = round(totalPayments, 2)
#         DifferenceAmount = round(float(totalPendings), 2)
#         # DifferenceAmount = round(float(float(TotalSales) - float(allPayment)), 2)

#         return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": TotalSales, "TotalReceivePayment": TotalReceivePayment, "DifferenceAmount": DifferenceAmount})
#     # except Exception as e:
#     #     return Response({"message": str(e),"status": 201,"data":[]})
    

@api_view(['POST'])
def filter_ledger_dashboard(request):
    # try:
        print("filter_ledger_dashboard", request.data)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        Filter = request.data['Filter']
        SalesType = request.data['Type']
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SalesPersonCode = -1
        if 'SalesPersonCode' in request.data:
            SalesPersonCode = request.data['SalesPersonCode']
        zones = getZoneByEmployee(SalesPersonCode)
        zonesStr = "','".join(zones)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SearchText = ""
        if 'SearchText' in request.data:
            SearchText = request.data['SearchText']
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        OrderByName = "a-z" #a-z/z-a
        OrderByAmt = "asc" #desc
        if 'OrderByName' in request.data:
            OrderByName = str(request.data['OrderByName']).strip()
        if 'OrderByAmt' in request.data:
            OrderByAmt = str(request.data['OrderByAmt']).strip()
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        orderby = ""
        if str(OrderByName).lower() == 'a-z':
            orderby = "Order By GroupName asc"
        elif str(OrderByName).lower() == 'z-a':
            orderby = "Order By GroupName desc"
        elif str(OrderByAmt).lower() == 'asc':
            orderby = "Order By DocTotal asc"
        elif str(OrderByAmt).lower() == 'desc':
            orderby = "Order By DocTotal desc"
        else:
            orderby = "Order By GroupName asc"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        fromToDate = ""
        if str(FromDate) != "":
            fromToDate = f"AND inv.DocDate >= '{FromDate}' AND inv.DocDate <= '{ToDate}'"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        sqlQuery = ""
        if str(Filter).lower() == 'group':
            SearchQuery = ''
            if str(SearchText) != '':
                SearchQuery = f"AND (bpgroup.Name like '%%{SearchText}%%' OR bpgroup.Code like '%%{SearchText}%%')"
            if str(SalesType).lower() == "gross":
                sqlQuery = f"""
                    SELECT
                        bp.GroupCode,
                        IFNULL(bpgroup.Name, '') as GroupName,
                        IFNULL(SUM(inv.DocTotal), 0) AS `DocTotal`,
                        IFNULL(SUM(inv.PaidToDateSys), 0) AS `PaidToDateSys`,
                        IFNULL(SUM(inv.DocTotal - inv.PaidToDateSys), 0) AS `PendingTotal`
                    FROM BusinessPartner_businesspartner bp
                    LEFT JOIN BusinessPartner_businesspartnergroups bpgroup ON bpgroup.Code = bp.GroupCode
                    LEFT JOIN Invoice_invoice inv ON bp.CardCode = inv.CardCode
                    WHERE 
                        inv.CancelStatus = 'csNo'
                        AND bp.U_U_UTL_Zone IN('{zonesStr}')
                        {SearchQuery}
                        {fromToDate}
                    GROUP BY bp.GroupCode {orderby}
                """
            else:
                sqlQuery = f"""
                    SELECT
                        bp.GroupCode,
                        IFNULL(bpgroup.Name, '') as GroupName,
                        IFNULL(SUM(A.DocTotal), 0) AS 'DocTotal',
                        IFNULL(SUM(A.NetTotal), 0) AS 'NetTotal',
                        IFNULL(SUM(A.PaidToDateSys), 0) AS `PaidToDateSys`,
                        IFNULL(SUM(A.DocTotal - A.PaidToDateSys), 0) AS `PendingTotal`
                    FROM BusinessPartner_businesspartner bp
                    LEFT JOIN BusinessPartner_businesspartnergroups bpgroup ON bpgroup.Code = bp.GroupCode
                    INNER JOIN (
                        SELECT
                            inv.CardCode,
                            inv.id,
                            inv.DocTotal,
                            inv.PaidToDateSys,
                            IFNULL(SUM(INVLine.LineTotal), 0) AS LineTotal,
                            IFNULL(
                                SUM(CASE
                                    WHEN inv.DiscountPercent != 0.0 THEN INVLine.LineTotal - (INVLine.LineTotal * inv.DiscountPercent / 100)
                                    ELSE INVLine.LineTotal
                                END), 0
                            ) AS NetTotal
                        FROM Invoice_invoice inv
                        LEFT JOIN Invoice_documentlines INVLine ON INVLine.InvoiceID = inv.id
                        WHERE 
                            inv.CancelStatus = 'csNo'
                            {fromToDate}
                        GROUP BY inv.CardCode, inv.id
                    ) A ON bp.CardCode = A.CardCode
                    WHERE 
                        bp.U_U_UTL_Zone IN('{zonesStr}')
                        {SearchQuery}
                    GROUP BY bp.GroupCode, GroupName;
                """
        else:
            SearchQuery = ''
            if str(SearchText) != '':
                SearchQuery = f"AND (bp.U_U_UTL_Zone like '%%{SearchText}%%')"

            if str(SalesType).lower() == "gross":
                sqlQuery = f"""
                    SELECT 
                        bp.U_U_UTL_Zone as GroupCode,
                        bp.U_U_UTL_Zone as GroupName, 
                        IFNULL(SUM(inv.DocTotal), 0) AS `DocTotal`, 
                        IFNULL(SUM(inv.PaidToDateSys), 0) AS `PaidToDateSys`, 
                        IFNULL(SUM(inv.DocTotal - inv.PaidToDateSys), 0) AS `PendingTotal` 
                    FROM BusinessPartner_businesspartner bp 
                    LEFT JOIN Invoice_invoice inv ON bp.CardCode = inv.CardCode 
                    WHERE 
                        inv.CancelStatus = 'csNo'
                        AND bp.U_U_UTL_Zone IN('{zonesStr}')
                        {SearchQuery}
                        {fromToDate}
                    GROUP BY bp.U_U_UTL_Zone {orderby}
                """
            else:
                sqlQuery = f"""
                    SELECT
                        bp.U_U_UTL_Zone as GroupCode,
                        bp.U_U_UTL_Zone as GroupName, 
                        IFNULL(SUM(A.DocTotal), 0) AS 'DocTotal',
                        IFNULL(SUM(A.NetTotal), 0) AS 'NetTotal',
                        IFNULL(SUM(A.PaidToDateSys), 0) AS `PaidToDateSys`,
                        IFNULL(SUM(A.DocTotal - A.PaidToDateSys), 0) AS `PendingTotal`
                    FROM BusinessPartner_businesspartner bp
                    LEFT JOIN BusinessPartner_businesspartnergroups bpgroup ON bpgroup.Code = bp.GroupCode
                    INNER JOIN (
                        SELECT
                            inv.CardCode,
                            inv.id,
                            inv.DocTotal,
                            inv.PaidToDateSys,
                            IFNULL(SUM(INVLine.LineTotal), 0) AS LineTotal,
                            IFNULL(
                                SUM(CASE
                                    WHEN inv.DiscountPercent != 0.0 THEN INVLine.LineTotal - (INVLine.LineTotal * inv.DiscountPercent / 100)
                                    ELSE INVLine.LineTotal
                                END), 0
                            ) AS NetTotal
                        FROM Invoice_invoice inv
                        LEFT JOIN Invoice_documentlines INVLine ON INVLine.InvoiceID = inv.id
                        WHERE 
                            inv.CancelStatus = 'csNo'
                            {fromToDate}
                        GROUP BY inv.CardCode, inv.id
                    ) A ON bp.CardCode = A.CardCode
                    WHERE 
                        bp.U_U_UTL_Zone IN('{zonesStr}')
                        {SearchQuery}
                    GROUP BY bp.U_U_UTL_Zone {orderby}
                """

        print(sqlQuery)
        mycursor.execute(sqlQuery)
        groupData = mycursor.fetchall()

        # return Response({"message": "Success","status": 200, "data":groupData})

        print("Code list count", len(groupData))
        if 'PageNo' in request.data:
            PageNo = int(request.data['PageNo'])
            MaxSize = request.data['MaxSize']
            if MaxSize != "All":
                size = int(MaxSize)
                endWith = (PageNo * size)
                startWith = (endWith - size)
                groupData = groupData[startWith:endWith]

        totalSales = 0
        totalPayments = 0
        totalPendings = 0
        dataContext = []
        for groupObj in groupData:
            GroupCode     = groupObj['GroupCode']
            GroupName     = groupObj['GroupName']
            DocTotal      = groupObj['DocTotal']
            PaidToDateSys = groupObj['PaidToDateSys']
            PendingTotal  = groupObj['PendingTotal']

            if str(SalesType).lower() == "net":
                DocTotal = groupObj['NetTotal']

            bpData = {
                "GroupName": GroupName,
                "GroupCode": GroupCode,
                "TotalSales": round(DocTotal, 2)
            }
            dataContext.append(bpData)
            totalSales = float(totalSales) + float(DocTotal)
            totalPayments = float(totalPayments) + float(PaidToDateSys)
            totalPendings = float(totalPendings) + float(PendingTotal)


        TotalSales = totalSales
        TotalReceivePayment = round(totalPayments, 2)
        DifferenceAmount = round(float(totalPendings), 2)
        # DifferenceAmount = round(float(float(TotalSales) - float(allPayment)), 2)

        return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": TotalSales, "TotalReceivePayment": TotalReceivePayment, "DifferenceAmount": DifferenceAmount})
    # except Exception as e:
    #     return Response({"message": str(e),"status": 201,"data":[]})




# # bp list with total purchase
# @api_view(['POST'])
# def ledger_dashboard_count(request):
#     try:
#         print("ledger_dashboard_count", request.data)
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         Filter = request.data['Filter']
#         Code = request.data['Code']
#         SalesType = request.data['Type']
#         FromDate = request.data['FromDate']
#         ToDate = request.data['ToDate']

#         SalesPersonCode = -1
#         if 'SalesPersonCode' in request.data:
#             SalesPersonCode = request.data['SalesPersonCode']
#         zones = getZoneByEmployee(SalesPersonCode)
#         zonesStr = "','".join(zones)
        
#         SearchText = ""
#         if 'SearchText' in request.data:
#             SearchText = request.data['SearchText']

#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         DueDaysGroup = ''
#         if 'DueDaysGroup' in request.data:
#             DueDaysGroup = request.data['DueDaysGroup']
#         # endif
#         overDuesQuery = ""
#         if DueDaysGroup != "":
#             overDuesQuery = f"AND DueDaysGroup = {DueDaysGroup}"
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
#         mycursor = mydb.cursor(dictionary=True, buffered=True)
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         fromToDate = ""
#         receiptfromToDate = ""
#         ordfromToDate = ""
#         if str(FromDate) != "":
#             fromToDate = f"AND inv.DocDate >= '{FromDate}' AND inv.DocDate <= '{ToDate}'"
#             receiptfromToDate = f"AND INVPay.DocDate >= '{FromDate}' AND INVPay.DocDate <= '{ToDate}'"
#             ordfromToDate = f"AND ord.DocDate >= '{FromDate}' AND ord.DocDate <= '{ToDate}'"
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         sqlQuery = ""
#         if str(Filter).lower() == 'group':
#             SearchQuery = ''
#             if str(SearchText) != '':
#                 SearchQuery = f"AND (bpgroup.Name like '%%{SearchText}%%' OR bpgroup.Code like '%%{SearchText}%%')"
#             if str(SalesType).lower() == "gross":
#                 sqlQuery = f""" SELECT bp.GroupCode, IFNULL(bpgroup.Name, '') as GroupName, IFNULL(SUM(inv.DocTotal), 0) AS `DocTotal`, IFNULL(SUM(inv.PaidToDateSys), 0) AS `PaidToDateSys`, IFNULL(SUM(inv.DocTotal - inv.PaidToDateSys), 0) AS `PendingTotal` FROM BusinessPartner_businesspartner bp LEFT JOIN BusinessPartner_businesspartnergroups bpgroup ON bpgroup.Code = bp.GroupCode LEFT JOIN Invoice_invoice inv ON bp.CardCode = inv.CardCode WHERE inv.CancelStatus = 'csNo' AND bp.U_U_UTL_Zone IN('{zonesStr}') {SearchQuery} {fromToDate} """
#             else:
#                 sqlQuery = f""" SELECT bp.GroupCode, IFNULL(bpgroup.Name, '') as GroupName, IFNULL(SUM(A.DocTotal), 0) AS 'DocTotal', IFNULL(SUM(A.NetTotal), 0) AS 'NetTotal', IFNULL(SUM(A.PaidToDateSys), 0) AS `PaidToDateSys`, IFNULL(SUM(A.DocTotal - A.PaidToDateSys), 0) AS `PendingTotal` FROM BusinessPartner_businesspartner bp LEFT JOIN BusinessPartner_businesspartnergroups bpgroup ON bpgroup.Code = bp.GroupCode INNER JOIN ( SELECT inv.CardCode, inv.id, inv.DocTotal, inv.PaidToDateSys, IFNULL(SUM(INVLine.LineTotal), 0) AS LineTotal, IFNULL( SUM(CASE WHEN inv.DiscountPercent != 0.0 THEN INVLine.LineTotal - (INVLine.LineTotal * inv.DiscountPercent / 100) ELSE INVLine.LineTotal END), 0 ) AS NetTotal FROM Invoice_invoice inv LEFT JOIN Invoice_documentlines INVLine ON INVLine.InvoiceID = inv.id WHERE inv.CancelStatus = 'csNo' {fromToDate} GROUP BY inv.CardCode, inv.id ) A ON bp.CardCode = A.CardCode WHERE bp.U_U_UTL_Zone IN('{zonesStr}') {SearchQuery} """
#         else:
#             SearchQuery = ''
#             if str(SearchText) != '':
#                 SearchQuery = f"AND (bp.U_U_UTL_Zone like '%%{SearchText}%%')"

#             if str(SalesType).lower() == "gross":
#                 sqlQuery = f""" SELECT bp.U_U_UTL_Zone as GroupCode, bp.U_U_UTL_Zone as GroupName, IFNULL(SUM(inv.DocTotal), 0) AS `DocTotal`, IFNULL(SUM(inv.PaidToDateSys), 0) AS `PaidToDateSys`, IFNULL(SUM(inv.DocTotal - inv.PaidToDateSys), 0) AS `PendingTotal` FROM BusinessPartner_businesspartner bp LEFT JOIN Invoice_invoice inv ON bp.CardCode = inv.CardCode WHERE inv.CancelStatus = 'csNo' AND bp.U_U_UTL_Zone IN('{zonesStr}') {SearchQuery} {fromToDate} """
#             else:
#                 sqlQuery = f""" SELECT bp.U_U_UTL_Zone as GroupCode, bp.U_U_UTL_Zone as GroupName, IFNULL(SUM(A.DocTotal), 0) AS 'DocTotal', IFNULL(SUM(A.NetTotal), 0) AS 'NetTotal', IFNULL(SUM(A.PaidToDateSys), 0) AS `PaidToDateSys`, IFNULL(SUM(A.DocTotal - A.PaidToDateSys), 0) AS `PendingTotal` FROM BusinessPartner_businesspartner bp LEFT JOIN BusinessPartner_businesspartnergroups bpgroup ON bpgroup.Code = bp.GroupCode INNER JOIN ( SELECT inv.CardCode, inv.id, inv.DocTotal, inv.PaidToDateSys, IFNULL(SUM(INVLine.LineTotal), 0) AS LineTotal, IFNULL( SUM(CASE WHEN inv.DiscountPercent != 0.0 THEN INVLine.LineTotal - (INVLine.LineTotal * inv.DiscountPercent / 100) ELSE INVLine.LineTotal END), 0 ) AS NetTotal FROM Invoice_invoice inv LEFT JOIN Invoice_documentlines INVLine ON INVLine.InvoiceID = inv.id WHERE inv.CancelStatus = 'csNo' {fromToDate} GROUP BY inv.CardCode, inv.id ) A ON bp.CardCode = A.CardCode WHERE bp.U_U_UTL_Zone IN('{zonesStr}') {SearchQuery} """

#         print(sqlQuery)
#         mycursor.execute(sqlQuery)
#         groupData = mycursor.fetchall()
#         TotalSales = 0
#         TotalReceivePayment = 0
#         PendingTotal = 0
#         if len(groupData) > 0:
#             TotalSales          = groupData[0]['DocTotal']
#             # TotalReceivePayment = groupData[0]['PaidToDateSys']
#             PendingTotal        = groupData[0]['PendingTotal']
#             if str(SalesType).lower() == "net":
#                 TotalSales = groupData[0]['NetTotal']
        
#         # print("TotalSales", TotalSales, "PendingTotal", PendingTotal)
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         # all filter bp cardcods
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         CardCodeArr = []
#         if str(Code).strip() == "":
#             CardCodeArr = list(BusinessPartner.objects.filter(U_U_UTL_Zone__in = zones).values_list("CardCode", flat=True))
#         else:
#             if str(Filter).lower() == 'group':
#                 CardCodeArr = list(BusinessPartner.objects.filter(GroupCode = Code, U_U_UTL_Zone__in = zones).values_list("CardCode", flat=True))
#             elif str(Filter).lower() == 'zone':
#                 CardCodeArr = list(BusinessPartner.objects.filter( U_U_UTL_Zone = Code).values_list("CardCode", flat=True))
#             else:
#                 CardCodeArr = list(BusinessPartner.objects.filter(U_U_UTL_Zone__in = zones).values_list("CardCode", flat=True))

#         CardCodeStr = "','".join(CardCodeArr)
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         # Total Receipt
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         TotalCreditNote = 0
#         sqlAllReceipts = f"""
#         SELECT
#             BP.CardCode,
#             BP.CardName,
#             IFNULL(SUM(INVPay.TransferSum), 0) AS `TransferSum`
#         FROM BusinessPartner_businesspartner BP
#             LEFT JOIN Invoice_incomingpayments INVPay ON INVPay.CardCode = BP.CardCode
#         WHERE
#             INVPay.JournalRemarks != 'Canceled'
#             AND BP.U_U_UTL_Zone IN('{zonesStr}')
#             {receiptfromToDate}
#         """
#         # AND INVPay.DocDate >= '{FromDate}' AND INVPay.DocDate <= '{ToDate}'
#         # print(sqlAllReceipts)
#         mycursor.execute(sqlAllReceipts)
#         allReceiptTotal = mycursor.fetchall()        
#         if len(allReceiptTotal) > 0:
#             TotalReceivePayment = allReceiptTotal[0]['TransferSum']
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         # Total Credit Notes
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         TotalCreditNote = 0
#         sqlAllCreditNote = f"""SELECT bp.CardCode AS CardCode, bp.CardName AS CardName, IFNULL(SUM(A.DocTotal), 0) AS 'DocTotal', IFNULL(SUM(A.NetTotal), 0) AS 'NetTotal', IFNULL(SUM(A.PaidToDateSys),  0) AS `PaidToDateSys`, IFNULL( SUM(A.DocTotal - A.PaidToDateSys), 0 ) AS `PendingTotal` FROM BusinessPartner_businesspartner bp LEFT JOIN BusinessPartner_businesspartnergroups bpgroup ON bpgroup.Code = bp.GroupCode INNER JOIN( SELECT inv.CardCode, inv.id, inv.DocTotal, inv.PaidToDateSys, IFNULL(SUM(INVLine.LineTotal), 0) AS LineTotal, IFNULL( SUM( CASE WHEN inv.DiscountPercent != 0.0 THEN INVLine.LineTotal - ( INVLine.LineTotal * inv.DiscountPercent / 100 ) ELSE INVLine.LineTotal END ), 0) AS NetTotal FROM Invoice_creditnotes inv LEFT JOIN Invoice_creditnotesdocumentlines INVLine ON INVLine.CreditNotesId = inv.id WHERE inv.CancelStatus = 'csNo' {fromToDate} GROUP BY inv.CardCode, inv.id ) A ON bp.CardCode = A.CardCode WHERE bp.U_U_UTL_Zone IN('{zonesStr}') """
#         print(sqlAllCreditNote)
#         mycursor.execute(sqlAllCreditNote)
#         allCreditNoteData = mycursor.fetchall()        
#         if len(allCreditNoteData) > 0:
#             CreditNote = allCreditNoteData[0]['NetTotal']
#             if str(SalesType).lower() == "gross":
#                 CreditNote = allCreditNoteData[0]['DocTotal']
#             TotalCreditNote = CreditNote
        
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         # Total Receivables 
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         sqlPendingSales = f""" SELECT id, SUM(`TotalDue`) as TotalPending FROM `BusinessPartner_receivable` WHERE CardCode IN('{CardCodeStr}') AND `CronUpdateCount` = (SELECT MAX(`CronUpdateCount`) FROM BusinessPartner_receivable) - 1 {overDuesQuery} """
#         print(sqlPendingSales)
#         mycursor.execute(sqlPendingSales)
#         allPendingData = mycursor.fetchall()
#         DifferenceAmount = 0        
#         if len(allPendingData) > 0:
#             DifferenceAmount = allPendingData[0]['TotalPending']

#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         # Total Pending Sales
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         TotalPendingSales = 0
#         # sqlPendingSales = f"SELECT bp.CardCode as CardCode, bp.CardName as CardName, A.id, IFNULL(SUM(A.DocTotal), 0) AS 'DocTotal', IFNULL(SUM(A.TotalOpenAmount), 0) AS 'TotalOpenAmount', IFNULL(SUM(A.TotalRemainingOpenQuantity), 0) AS 'TotalRemainingOpenQuantity' FROM BusinessPartner_businesspartner bp INNER JOIN ( SELECT ord.CardCode, ord.id, ord.DocTotal, IFNULL(SUM(ORDLine.OpenAmount), 0) AS TotalOpenAmount, IFNULL(SUM(ORDLine.RemainingOpenQuantity), 0) AS TotalRemainingOpenQuantity FROM Order_order ord LEFT JOIN Order_documentlines ORDLine ON ORDLine.OrderID = ord.id WHERE ord.CancelStatus = 'csNo' AND ord.DocumentStatus = 'bost_Open' GROUP BY ord.CardCode, ord.id ) A ON bp.CardCode = A.CardCode WHERE bp.CardCode IN('{CardCodeStr}');"
#         sqlPendingSales = f"""
#             SELECT
#                 bp.CardCode as CardCode,
#                 bp.CardName as CardName,
#                 A.id,
#                 IFNULL(SUM(A.DocTotal), 0) AS 'DocTotal',
#                 IFNULL(SUM(A.TotalOpenAmount), 0) AS 'TotalOpenAmount',
#                 IFNULL(SUM(A.TotalRemainingOpenQuantity), 0) AS 'TotalRemainingOpenQuantity'
#             FROM BusinessPartner_businesspartner bp
#             INNER JOIN (
#                 SELECT
#                     ord.CardCode,
#                     ord.id,
#                     ord.DocTotal,
#                     IFNULL(SUM(ORDLine.UnitPrice * ORDLine.RemainingOpenQuantity), 0) AS TotalOpenAmountTmp,
#                     IFNULL(SUM(IF(
#                         ORDLine.DiscountPercent > 0,
#                         (((ORDLine.UnitPrice * ORDLine.RemainingOpenQuantity ) * ORDLine.DiscountPercent ) / 100),
#                         (ORDLine.UnitPrice * ORDLine.RemainingOpenQuantity)
#                     )), 0) AS TotalOpenAmount,
#                     IFNULL(SUM(ORDLine.RemainingOpenQuantity), 0) AS TotalRemainingOpenQuantity
#                 FROM Order_order ord
#                 LEFT JOIN Order_documentlines ORDLine ON ORDLine.OrderID = ord.id
#                 WHERE 
#                     ord.CancelStatus = 'csNo'
#                     AND ord.DocumentStatus = 'bost_Open'
#                     AND RemainingOpenQuantity > 0
#                     {ordfromToDate}
#                 GROUP BY ord.CardCode, ord.id
#                 Order By ord.DocDate desc
#             ) A ON bp.CardCode = A.CardCode
#             WHERE
#                 bp.U_U_UTL_Zone IN('{zonesStr}')
#         """
#         mycursor.execute(sqlPendingSales)
#         allPendingSalesData = mycursor.fetchall()        
#         if len(allPendingSalesData) > 0:
#             TotalPendingSales = allPendingSalesData[0]['TotalOpenAmount']

#         # DifferenceAmount = abs(round(float(float(PendingTotal) - float(bpCreditNote) + float(bpJELineTotal)), 2))
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         contaxt = {
#             "TotalSales": round(float(TotalSales), 2), 
#             # "TotalSales": round(float(TotalSales) - (TotalCreditNote), 2), 
#             "TotalReceivePayment": TotalReceivePayment, 
#             "DifferenceAmount":DifferenceAmount,
#             "TotalCreditNote": round(TotalCreditNote, 2),
#             "TotalPendingSales": round(TotalPendingSales, 2)
#         }
#         return Response({"message": "Success","status": 200, "data":[contaxt]})
#     except Exception as e:
#         return Response({"message": str(e),"status": 201,"data":[]})
    



# bp list with total purchase
@api_view(['POST'])
def ledger_dashboard_count(request):
    try:
        print("ledger_dashboard_count", request.data)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        Filter = request.data['Filter']
        Code = request.data['Code']
        SalesType = request.data['Type']
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']

        SalesPersonCode = -1
        if 'SalesPersonCode' in request.data:
            SalesPersonCode = request.data['SalesPersonCode']

        zone_wise = request.data["Zone"] if "Zone" in request.data else ""

        if zone_wise!="":
            zonesStr = str(zone_wise)
        else:
            zones = getZoneByEmployee(SalesPersonCode)
            zonesStr = "','".join(zones)
            
        # zones = getZoneByEmployee(SalesPersonCode)
        # zonesStr = "','".join(zones)
        
        SearchText = ""
        if 'SearchText' in request.data:
            SearchText = request.data['SearchText']

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        DueDaysGroup = ''
        if 'DueDaysGroup' in request.data:
            DueDaysGroup = request.data['DueDaysGroup']
        # endif
        overDuesQuery = ""
        if DueDaysGroup != "":
            if DueDaysGroup =="90":
                overDuesQuery = f"AND DueDaysGroup > {DueDaysGroup}"
            else:
                overDuesQuery = f"AND DueDaysGroup = {DueDaysGroup}"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        fromToDate = ""
        receiptfromToDate = ""
        ordfromToDate = ""
        if str(FromDate) != "":
            fromToDate = f"AND inv.DocDate >= '{FromDate}' AND inv.DocDate <= '{ToDate}'"
            receiptfromToDate = f"AND INVPay.DocDate >= '{FromDate}' AND INVPay.DocDate <= '{ToDate}'"
            ordfromToDate = f"AND ord.DocDate >= '{FromDate}' AND ord.DocDate <= '{ToDate}'"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        sqlQuery = ""
        if str(Filter).lower() == 'group':
            SearchQuery = ''
            if str(SearchText) != '':
                SearchQuery = f"AND (bpgroup.Name like '%%{SearchText}%%' OR bpgroup.Code like '%%{SearchText}%%')"
            if str(SalesType).lower() == "gross":
                sqlQuery = f""" SELECT bp.GroupCode, IFNULL(bpgroup.Name, '') as GroupName, IFNULL(SUM(inv.DocTotal), 0) AS `DocTotal`, IFNULL(SUM(inv.PaidToDateSys), 0) AS `PaidToDateSys`, IFNULL(SUM(inv.DocTotal - inv.PaidToDateSys), 0) AS `PendingTotal` FROM BusinessPartner_businesspartner bp LEFT JOIN BusinessPartner_businesspartnergroups bpgroup ON bpgroup.Code = bp.GroupCode LEFT JOIN Invoice_invoice inv ON bp.CardCode = inv.CardCode WHERE inv.CancelStatus = 'csNo' AND bp.U_U_UTL_Zone IN('{zonesStr}') {SearchQuery} {fromToDate} """
            else:
                sqlQuery = f""" SELECT bp.GroupCode, IFNULL(bpgroup.Name, '') as GroupName, IFNULL(SUM(A.DocTotal), 0) AS 'DocTotal', IFNULL(SUM(A.NetTotal), 0) AS 'NetTotal', IFNULL(SUM(A.PaidToDateSys), 0) AS `PaidToDateSys`, IFNULL(SUM(A.DocTotal - A.PaidToDateSys), 0) AS `PendingTotal` FROM BusinessPartner_businesspartner bp LEFT JOIN BusinessPartner_businesspartnergroups bpgroup ON bpgroup.Code = bp.GroupCode INNER JOIN ( SELECT inv.CardCode, inv.id, inv.DocTotal, inv.PaidToDateSys, IFNULL(SUM(INVLine.LineTotal), 0) AS LineTotal, IFNULL( SUM(CASE WHEN inv.DiscountPercent != 0.0 THEN INVLine.LineTotal - (INVLine.LineTotal * inv.DiscountPercent / 100) ELSE INVLine.LineTotal END), 0 ) AS NetTotal FROM Invoice_invoice inv LEFT JOIN Invoice_documentlines INVLine ON INVLine.InvoiceID = inv.id WHERE inv.CancelStatus = 'csNo' {fromToDate} GROUP BY inv.CardCode, inv.id ) A ON bp.CardCode = A.CardCode WHERE bp.U_U_UTL_Zone IN('{zonesStr}') {SearchQuery} """
        else:
            SearchQuery = ''
            if str(SearchText) != '':
                SearchQuery = f"AND (bp.U_U_UTL_Zone like '%%{SearchText}%%')"

            if str(SalesType).lower() == "gross":
                sqlQuery = f""" SELECT bp.U_U_UTL_Zone as GroupCode, bp.U_U_UTL_Zone as GroupName, IFNULL(SUM(inv.DocTotal), 0) AS `DocTotal`, IFNULL(SUM(inv.PaidToDateSys), 0) AS `PaidToDateSys`, IFNULL(SUM(inv.DocTotal - inv.PaidToDateSys), 0) AS `PendingTotal` FROM BusinessPartner_businesspartner bp LEFT JOIN Invoice_invoice inv ON bp.CardCode = inv.CardCode WHERE inv.CancelStatus = 'csNo' AND bp.U_U_UTL_Zone IN('{zonesStr}') {SearchQuery} {fromToDate} """
            else:
                sqlQuery = f""" SELECT bp.U_U_UTL_Zone as GroupCode, bp.U_U_UTL_Zone as GroupName, IFNULL(SUM(A.DocTotal), 0) AS 'DocTotal', IFNULL(SUM(A.NetTotal), 0) AS 'NetTotal', IFNULL(SUM(A.PaidToDateSys), 0) AS `PaidToDateSys`, IFNULL(SUM(A.DocTotal - A.PaidToDateSys), 0) AS `PendingTotal` FROM BusinessPartner_businesspartner bp LEFT JOIN BusinessPartner_businesspartnergroups bpgroup ON bpgroup.Code = bp.GroupCode INNER JOIN ( SELECT inv.CardCode, inv.id, inv.DocTotal, inv.PaidToDateSys, IFNULL(SUM(INVLine.LineTotal), 0) AS LineTotal, IFNULL( SUM(CASE WHEN inv.DiscountPercent != 0.0 THEN INVLine.LineTotal - (INVLine.LineTotal * inv.DiscountPercent / 100) ELSE INVLine.LineTotal END), 0 ) AS NetTotal FROM Invoice_invoice inv LEFT JOIN Invoice_documentlines INVLine ON INVLine.InvoiceID = inv.id WHERE inv.CancelStatus = 'csNo' {fromToDate} GROUP BY inv.CardCode, inv.id ) A ON bp.CardCode = A.CardCode WHERE bp.U_U_UTL_Zone IN('{zonesStr}') {SearchQuery} """

        print(sqlQuery)
        mycursor.execute(sqlQuery)
        groupData = mycursor.fetchall()
        TotalSales = 0
        TotalReceivePayment = 0
        PendingTotal = 0
        if len(groupData) > 0:
            TotalSales          = groupData[0]['DocTotal']
            # TotalReceivePayment = groupData[0]['PaidToDateSys']
            PendingTotal        = groupData[0]['PendingTotal']
            if str(SalesType).lower() == "net":
                TotalSales = groupData[0]['NetTotal']
        
        # print("TotalSales", TotalSales, "PendingTotal", PendingTotal)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # all filter bp cardcods
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        CardCodeArr = []
        if str(Code).strip() == "":
            CardCodeArr = list(BusinessPartner.objects.filter(U_U_UTL_Zone__in = zones).values_list("CardCode", flat=True))
        else:
            if str(Filter).lower() == 'group':
                CardCodeArr = list(BusinessPartner.objects.filter(GroupCode = Code, U_U_UTL_Zone__in = zones).values_list("CardCode", flat=True))
            elif str(Filter).lower() == 'zone':
                CardCodeArr = list(BusinessPartner.objects.filter( U_U_UTL_Zone = Code).values_list("CardCode", flat=True))
            else:
                CardCodeArr = list(BusinessPartner.objects.filter(U_U_UTL_Zone__in = zones).values_list("CardCode", flat=True))

        CardCodeStr = "','".join(CardCodeArr)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # Total Receipt
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        TotalCreditNote = 0
        sqlAllReceipts = f"""
        SELECT
            BP.CardCode,
            BP.CardName,
            IFNULL(SUM(INVPay.TransferSum), 0) AS `TransferSum`
        FROM BusinessPartner_businesspartner BP
            LEFT JOIN Invoice_incomingpayments INVPay ON INVPay.CardCode = BP.CardCode
        WHERE
            INVPay.JournalRemarks != 'Canceled'
            AND BP.U_U_UTL_Zone IN('{zonesStr}')
            {receiptfromToDate}
        """
        # AND INVPay.DocDate >= '{FromDate}' AND INVPay.DocDate <= '{ToDate}'
        # print(sqlAllReceipts)
        mycursor.execute(sqlAllReceipts)
        allReceiptTotal = mycursor.fetchall()        
        if len(allReceiptTotal) > 0:
            TotalReceivePayment = allReceiptTotal[0]['TransferSum']
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # Total Credit Notes
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        TotalCreditNote = 0
        sqlAllCreditNote = f"""SELECT bp.CardCode AS CardCode, bp.CardName AS CardName, IFNULL(SUM(A.DocTotal), 0) AS 'DocTotal', IFNULL(SUM(A.NetTotal), 0) AS 'NetTotal', IFNULL(SUM(A.PaidToDateSys),  0) AS `PaidToDateSys`, IFNULL( SUM(A.DocTotal - A.PaidToDateSys), 0 ) AS `PendingTotal` FROM BusinessPartner_businesspartner bp LEFT JOIN BusinessPartner_businesspartnergroups bpgroup ON bpgroup.Code = bp.GroupCode INNER JOIN( SELECT inv.CardCode, inv.id, inv.DocTotal, inv.PaidToDateSys, IFNULL(SUM(INVLine.LineTotal), 0) AS LineTotal, IFNULL( SUM( CASE WHEN inv.DiscountPercent != 0.0 THEN INVLine.LineTotal - ( INVLine.LineTotal * inv.DiscountPercent / 100 ) ELSE INVLine.LineTotal END ), 0) AS NetTotal FROM Invoice_creditnotes inv LEFT JOIN Invoice_creditnotesdocumentlines INVLine ON INVLine.CreditNotesId = inv.id WHERE inv.CancelStatus = 'csNo' {fromToDate} GROUP BY inv.CardCode, inv.id ) A ON bp.CardCode = A.CardCode WHERE bp.U_U_UTL_Zone IN('{zonesStr}') """
        print(sqlAllCreditNote)
        mycursor.execute(sqlAllCreditNote)
        allCreditNoteData = mycursor.fetchall()        
        if len(allCreditNoteData) > 0:
            CreditNote = allCreditNoteData[0]['NetTotal']
            if str(SalesType).lower() == "gross":
                CreditNote = allCreditNoteData[0]['DocTotal']
            TotalCreditNote = CreditNote
        
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # Total Receivables 
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        sqlPendingSales = f""" SELECT id, SUM(`TotalDue`) as TotalPending FROM `BusinessPartner_receivable` WHERE CardCode IN('{CardCodeStr}') AND `CronUpdateCount` = (SELECT MAX(`CronUpdateCount`) FROM BusinessPartner_receivable) - 1 {overDuesQuery} """
        print(sqlPendingSales)
        mycursor.execute(sqlPendingSales)
        allPendingData = mycursor.fetchall()
        DifferenceAmount = 0        
        if len(allPendingData) > 0:
            DifferenceAmount = allPendingData[0]['TotalPending']

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # Total Pending Sales
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        TotalPendingSales = 0
        # sqlPendingSales = f"SELECT bp.CardCode as CardCode, bp.CardName as CardName, A.id, IFNULL(SUM(A.DocTotal), 0) AS 'DocTotal', IFNULL(SUM(A.TotalOpenAmount), 0) AS 'TotalOpenAmount', IFNULL(SUM(A.TotalRemainingOpenQuantity), 0) AS 'TotalRemainingOpenQuantity' FROM BusinessPartner_businesspartner bp INNER JOIN ( SELECT ord.CardCode, ord.id, ord.DocTotal, IFNULL(SUM(ORDLine.OpenAmount), 0) AS TotalOpenAmount, IFNULL(SUM(ORDLine.RemainingOpenQuantity), 0) AS TotalRemainingOpenQuantity FROM Order_order ord LEFT JOIN Order_documentlines ORDLine ON ORDLine.OrderID = ord.id WHERE ord.CancelStatus = 'csNo' AND ord.DocumentStatus = 'bost_Open' GROUP BY ord.CardCode, ord.id ) A ON bp.CardCode = A.CardCode WHERE bp.CardCode IN('{CardCodeStr}');"
        sqlPendingSales = f"""
            SELECT
                bp.CardCode as CardCode,
                bp.CardName as CardName,
                A.id,
                IFNULL(SUM(A.DocTotal), 0) AS 'DocTotal',
                IFNULL(SUM(A.TotalOpenAmount), 0) AS 'TotalOpenAmount',
                IFNULL(SUM(A.TotalRemainingOpenQuantity), 0) AS 'TotalRemainingOpenQuantity'
            FROM BusinessPartner_businesspartner bp
            INNER JOIN (
                SELECT
                    ord.CardCode,
                    ord.id,
                    ord.DocTotal,
                    IFNULL(SUM(ORDLine.UnitPrice * ORDLine.RemainingOpenQuantity), 0) AS TotalOpenAmountTmp,
                    IFNULL(SUM(IF(
                        ORDLine.DiscountPercent > 0,
                        (((ORDLine.UnitPrice * ORDLine.RemainingOpenQuantity ) * ORDLine.DiscountPercent ) / 100),
                        (ORDLine.UnitPrice * ORDLine.RemainingOpenQuantity)
                    )), 0) AS TotalOpenAmount,
                    IFNULL(SUM(ORDLine.RemainingOpenQuantity), 0) AS TotalRemainingOpenQuantity
                FROM Order_order ord
                LEFT JOIN Order_documentlines ORDLine ON ORDLine.OrderID = ord.id
                WHERE 
                    ord.CancelStatus = 'csNo'
                    AND ord.DocumentStatus = 'bost_Open'
                    AND RemainingOpenQuantity > 0
                    {ordfromToDate}
                GROUP BY ord.CardCode, ord.id
                Order By ord.DocDate desc
            ) A ON bp.CardCode = A.CardCode
            WHERE
                bp.U_U_UTL_Zone IN('{zonesStr}')
        """
        mycursor.execute(sqlPendingSales)
        allPendingSalesData = mycursor.fetchall()        
        if len(allPendingSalesData) > 0:
            TotalPendingSales = allPendingSalesData[0]['TotalOpenAmount']

        # DifferenceAmount = abs(round(float(float(PendingTotal) - float(bpCreditNote) + float(bpJELineTotal)), 2))
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        contaxt = {
            "TotalSales": round(float(TotalSales), 2), 
            # "TotalSales": round(float(TotalSales) - (TotalCreditNote), 2), 
            "TotalReceivePayment": TotalReceivePayment, 
            "DifferenceAmount":DifferenceAmount,
            "TotalCreditNote": round(TotalCreditNote, 2),
            "TotalPendingSales": round(TotalPendingSales, 2)
        }
        return Response({"message": "Success","status": 200, "data":[contaxt]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
    



# # bp list with total purchase
# @api_view(['POST'])
# def ledger_dashboard(request):
#     try:
#         print("ledger_dashboard", request.data)
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         Filter = request.data['Filter']
#         Code = request.data['Code']
#         SalesType = request.data['Type']
#         FromDate = request.data['FromDate']
#         ToDate = request.data['ToDate']
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         SalesPersonCode = -1
#         if 'SalesPersonCode' in request.data:
#             SalesPersonCode = request.data['SalesPersonCode']
#         zones = getZoneByEmployee(SalesPersonCode)
#         zonesStr = "','".join(zones)
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         SearchText = ""
#         if 'SearchText' in request.data:
#             SearchText = request.data['SearchText']
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         OrderByName = "a-z" #a-z/z-a
#         OrderByAmt = "asc" #desc
#         if 'OrderByName' in request.data:
#             OrderByName = str(request.data['OrderByName']).strip()
#         if 'OrderByAmt' in request.data:
#             OrderByAmt = str(request.data['OrderByAmt']).strip()
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         orderby = ""
#         if str(OrderByName).lower() == 'a-z':
#             orderby = "Order By bp.CardName asc"
#         elif str(OrderByName).lower() == 'z-a':
#             orderby = "Order By bp.CardName desc"
#         elif str(OrderByAmt).lower() == 'asc':
#             orderby = "Order By DocTotal asc"
#         elif str(OrderByAmt).lower() == 'desc':
#             orderby = "Order By DocTotal desc"
#         else:
#             orderby = "Order By bp.CardName asc"
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
#         mycursor = mydb.cursor(dictionary=True, buffered=True)
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         fromToDate = ""
#         if str(FromDate) != "":
#             fromToDate = f"AND inv.DocDate >= '{FromDate}' AND inv.DocDate <= '{ToDate}'"
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         limitQuery = ""
#         if 'PageNo' in request.data:
#             PageNo = int(request.data['PageNo'])
#             MaxSize = request.data['MaxSize']
#             if MaxSize != "All":
#                 size = int(MaxSize)
#                 endWith = (PageNo * size)
#                 startWith = (endWith - size)
#                 # dataContext = dataContext[startWith:endWith]
#                 limitQuery = f"Limit {startWith}, {MaxSize}"
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         SearchQuery = ""
#         if str(SearchText) != '':
#             SearchQuery = f"AND (bp.CardCode like '%%{SearchText}%%' OR bp.CardName like '%%{SearchText}%%')"
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         filterBy = f"bp.U_U_UTL_Zone IN('{zonesStr}')"
#         if str(Filter).lower() == 'group':
#             filterBy = f"bp.U_U_UTL_Zone IN('{zonesStr}') AND bp.GroupCode = '{Code}'"
#         elif str(Filter).lower() == 'zone':
#             filterBy = f"bp.U_U_UTL_Zone = '{Code}'"
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         dataContext = []
#         sqlQuery = ""
#         if str(SalesType).lower() == "gross":
#             sqlQuery = f"""
#                 SELECT
#                     bp.CardCode,
#                     bp.CardName,
#                     IFNULL(SUM(inv.DocTotal), 0) AS `DocTotal`,
#                     IFNULL(SUM(inv.PaidToDateSys), 0) AS `PaidToDateSys`,
#                     IFNULL(SUM(inv.DocTotal - inv.PaidToDateSys), 0) AS `PendingTotal`
#                 FROM BusinessPartner_businesspartner bp
#                 LEFT JOIN BusinessPartner_businesspartnergroups bpgroup ON bpgroup.Code = bp.GroupCode
#                 LEFT JOIN Invoice_invoice inv ON bp.CardCode = inv.CardCode
#                 WHERE 
#                     {filterBy}
#                     AND inv.CancelStatus = 'csNo'
#                     {SearchQuery}
#                     {fromToDate}
#                 GROUP BY bp.CardCode {orderby} {limitQuery}
#             """
#         else:
#             sqlQuery = f"""
#                 SELECT
#                     bp.CardCode,
#                     bp.CardName,
#                     IFNULL(SUM(A.NetTotal), 0) AS 'DocTotal',
#                     IFNULL(SUM(A.PaidToDateSys), 0) AS `PaidToDateSys`,
#                     IFNULL(SUM(A.DocTotal - A.PaidToDateSys), 0) AS `PendingTotal`
#                 FROM BusinessPartner_businesspartner bp
#                 LEFT JOIN BusinessPartner_businesspartnergroups bpgroup ON bpgroup.Code = bp.GroupCode
#                 INNER JOIN (
#                     SELECT
#                         inv.CardCode,
#                         inv.id,
#                         inv.DocTotal,
#                         inv.PaidToDateSys,
#                         IFNULL(SUM(INVLine.LineTotal), 0) AS LineTotal,
#                         IFNULL(
#                             SUM(CASE
#                                 WHEN inv.DiscountPercent != 0.0 THEN INVLine.LineTotal - (INVLine.LineTotal * inv.DiscountPercent / 100)
#                                 ELSE INVLine.LineTotal
#                             END), 0
#                         ) AS NetTotal
#                     FROM Invoice_invoice inv
#                     LEFT JOIN Invoice_documentlines INVLine ON INVLine.InvoiceID = inv.id
#                     WHERE 
#                         inv.CancelStatus = 'csNo'
#                         {fromToDate}
#                     GROUP BY inv.CardCode, inv.id
#                 ) A ON bp.CardCode = A.CardCode
#                 WHERE 
#                     {filterBy}
#                     {SearchQuery}
#                 GROUP BY bp.CardCode {orderby} {limitQuery}
#             """
#         # endElse

#         print(sqlQuery)
#         mycursor.execute(sqlQuery)
#         groupData = mycursor.fetchall()
#         TotalSales = 0
#         TotalReceivePayment = 0
#         PendingTotal = 0
#         if len(groupData) > 0:
#             for data in groupData:
#                 CardCode = data['CardCode']
#                 CardName = data['CardName']
#                 totalSalesByBp = data['DocTotal']
#                 TotalReceivePayment = 0
#                 PendingTotal  = 0

#                 sqlCreditNoteQuery = f"SELECT bp.CardCode AS CardCode, bp.CardName AS CardName, IFNULL(SUM(A.DocTotal), 0) AS 'DocTotal', IFNULL(SUM(A.NetTotal), 0) AS 'NetTotal' FROM BusinessPartner_businesspartner bp LEFT JOIN BusinessPartner_businesspartnergroups bpgroup ON bpgroup.Code = bp.GroupCode INNER JOIN( SELECT inv.CardCode, inv.id, inv.DocTotal, inv.PaidToDateSys, IFNULL(SUM(INVLine.LineTotal), 0) AS LineTotal, IFNULL( SUM( CASE WHEN inv.DiscountPercent != 0.0 THEN INVLine.LineTotal -( INVLine.LineTotal * inv.DiscountPercent / 100 ) ELSE INVLine.LineTotal END ), 0 ) AS NetTotal FROM Invoice_creditnotes inv LEFT JOIN Invoice_creditnotesdocumentlines INVLine ON INVLine.CreditNotesId = inv.id WHERE inv.CancelStatus = 'csNo' {fromToDate} GROUP BY inv.CardCode, inv.id ) A ON bp.CardCode = A.CardCode WHERE bp.CardCode = '{CardCode}';"
#                 print(sqlCreditNoteQuery)
#                 mycursor.execute(sqlCreditNoteQuery)
#                 creditNoteData = mycursor.fetchall()

#                 cnDocTotal = 0
#                 if len(creditNoteData) > 0:
#                     cnDocTotal = creditNoteData[0]['DocTotal']
#                     if str(SalesType).lower() == "net":
#                         cnDocTotal = creditNoteData[0]['NetTotal']
#                     # endif
#                 # endif

#                 tempTotalSales = float(totalSalesByBp) - float(cnDocTotal)
#                 bpData = {
#                     "CardCode": CardCode,
#                     "CardName": CardName,
#                     "TotalSales": round(tempTotalSales, 2)
#                 }
#                 dataContext.append(bpData)
#                 TotalSales = TotalSales + tempTotalSales
        

#         TotalSales = round(TotalSales, 2)
#         TotalReceivePayment = round(TotalReceivePayment, 2)
#         DifferenceAmount = round(PendingTotal, 2)
#         # DifferenceAmount = round(float(float(TotalSales) - float(allPayment)), 2)

#         return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": TotalSales, "TotalReceivePayment": TotalReceivePayment, "DifferenceAmount": DifferenceAmount})
#     except Exception as e:
#         return Response({"message": str(e),"status": 201,"data":[]})



# bp list with total purchase
@api_view(['POST'])
def ledger_dashboard(request):
    try:
        print("ledger_dashboard", request.data)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        Filter = request.data['Filter']
        Code = request.data['Code']
        SalesType = request.data['Type']
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SalesPersonCode = -1
        if 'SalesPersonCode' in request.data:
            SalesPersonCode = request.data['SalesPersonCode']

        zone_wise = request.data["Zone"] if "Zone" in request.data else ""

        if zone_wise!="":
            zonesStr = str(zone_wise)
        else:
            zones = getZoneByEmployee(SalesPersonCode)
            zonesStr = "','".join(zones)

        # zones = getZoneByEmployee(SalesPersonCode)
        # zonesStr = "','".join(zones)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SearchText = ""
        if 'SearchText' in request.data:
            SearchText = request.data['SearchText']
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        OrderByName = "a-z" #a-z/z-a
        OrderByAmt = "asc" #desc
        if 'OrderByName' in request.data:
            OrderByName = str(request.data['OrderByName']).strip()
        if 'OrderByAmt' in request.data:
            OrderByAmt = str(request.data['OrderByAmt']).strip()
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        orderby = ""
        if str(OrderByName).lower() == 'a-z':
            orderby = "Order By bp.CardName asc"
        elif str(OrderByName).lower() == 'z-a':
            orderby = "Order By bp.CardName desc"
        elif str(OrderByAmt).lower() == 'asc':
            orderby = "Order By DocTotal asc"
        elif str(OrderByAmt).lower() == 'desc':
            orderby = "Order By DocTotal desc"
        else:
            orderby = "Order By bp.CardName asc"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        fromToDate = ""
        if str(FromDate) != "":
            fromToDate = f"AND inv.DocDate >= '{FromDate}' AND inv.DocDate <= '{ToDate}'"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        limitQuery = ""
        if 'PageNo' in request.data:
            PageNo = int(request.data['PageNo'])
            MaxSize = request.data['MaxSize']
            if MaxSize != "All":
                size = int(MaxSize)
                endWith = (PageNo * size)
                startWith = (endWith - size)
                # dataContext = dataContext[startWith:endWith]
                limitQuery = f"Limit {startWith}, {MaxSize}"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SearchQuery = ""
        if str(SearchText) != '':
            SearchQuery = f"AND (bp.CardCode like '%%{SearchText}%%' OR bp.CardName like '%%{SearchText}%%')"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        filterBy = f"bp.U_U_UTL_Zone IN('{zonesStr}')"
        if str(Filter).lower() == 'group':
            filterBy = f"bp.U_U_UTL_Zone IN('{zonesStr}') AND bp.GroupCode = '{Code}'"
        elif str(Filter).lower() == 'zone':
            filterBy = f"bp.U_U_UTL_Zone = '{Code}'"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        dataContext = []
        sqlQuery = ""
        if str(SalesType).lower() == "gross":
            sqlQuery = f"""
                SELECT
                    bp.CardCode,
                    bp.CardName,
                    IFNULL(SUM(inv.DocTotal), 0) AS `DocTotal`,
                    IFNULL(SUM(inv.PaidToDateSys), 0) AS `PaidToDateSys`,
                    IFNULL(SUM(inv.DocTotal - inv.PaidToDateSys), 0) AS `PendingTotal`
                FROM BusinessPartner_businesspartner bp
                LEFT JOIN BusinessPartner_businesspartnergroups bpgroup ON bpgroup.Code = bp.GroupCode
                LEFT JOIN Invoice_invoice inv ON bp.CardCode = inv.CardCode
                WHERE 
                    {filterBy}
                    AND inv.CancelStatus = 'csNo'
                    {SearchQuery}
                    {fromToDate}
                GROUP BY bp.CardCode {orderby} {limitQuery}
            """
        else:
            sqlQuery = f"""
                SELECT
                    bp.CardCode,
                    bp.CardName,
                    IFNULL(SUM(A.NetTotal), 0) AS 'DocTotal',
                    IFNULL(SUM(A.PaidToDateSys), 0) AS `PaidToDateSys`,
                    IFNULL(SUM(A.DocTotal - A.PaidToDateSys), 0) AS `PendingTotal`
                FROM BusinessPartner_businesspartner bp
                LEFT JOIN BusinessPartner_businesspartnergroups bpgroup ON bpgroup.Code = bp.GroupCode
                INNER JOIN (
                    SELECT
                        inv.CardCode,
                        inv.id,
                        inv.DocTotal,
                        inv.PaidToDateSys,
                        IFNULL(SUM(INVLine.LineTotal), 0) AS LineTotal,
                        IFNULL(
                            SUM(CASE
                                WHEN inv.DiscountPercent != 0.0 THEN INVLine.LineTotal - (INVLine.LineTotal * inv.DiscountPercent / 100)
                                ELSE INVLine.LineTotal
                            END), 0
                        ) AS NetTotal
                    FROM Invoice_invoice inv
                    LEFT JOIN Invoice_documentlines INVLine ON INVLine.InvoiceID = inv.id
                    WHERE 
                        inv.CancelStatus = 'csNo'
                        {fromToDate}
                    GROUP BY inv.CardCode, inv.id
                ) A ON bp.CardCode = A.CardCode
                WHERE 
                    {filterBy}
                    {SearchQuery}
                GROUP BY bp.CardCode {orderby} {limitQuery}
            """
        # endElse

        print(sqlQuery)
        mycursor.execute(sqlQuery)
        groupData = mycursor.fetchall()
        TotalSales = 0
        TotalReceivePayment = 0
        PendingTotal = 0
        if len(groupData) > 0:
            for data in groupData:
                CardCode = data['CardCode']
                CardName = data['CardName']
                totalSalesByBp = data['DocTotal']
                TotalReceivePayment = 0
                PendingTotal  = 0

                sqlCreditNoteQuery = f"SELECT bp.CardCode AS CardCode, bp.CardName AS CardName, IFNULL(SUM(A.DocTotal), 0) AS 'DocTotal', IFNULL(SUM(A.NetTotal), 0) AS 'NetTotal' FROM BusinessPartner_businesspartner bp LEFT JOIN BusinessPartner_businesspartnergroups bpgroup ON bpgroup.Code = bp.GroupCode INNER JOIN( SELECT inv.CardCode, inv.id, inv.DocTotal, inv.PaidToDateSys, IFNULL(SUM(INVLine.LineTotal), 0) AS LineTotal, IFNULL( SUM( CASE WHEN inv.DiscountPercent != 0.0 THEN INVLine.LineTotal -( INVLine.LineTotal * inv.DiscountPercent / 100 ) ELSE INVLine.LineTotal END ), 0 ) AS NetTotal FROM Invoice_creditnotes inv LEFT JOIN Invoice_creditnotesdocumentlines INVLine ON INVLine.CreditNotesId = inv.id WHERE inv.CancelStatus = 'csNo' {fromToDate} GROUP BY inv.CardCode, inv.id ) A ON bp.CardCode = A.CardCode WHERE bp.CardCode = '{CardCode}';"
                print(sqlCreditNoteQuery)
                mycursor.execute(sqlCreditNoteQuery)
                creditNoteData = mycursor.fetchall()

                cnDocTotal = 0
                if len(creditNoteData) > 0:
                    cnDocTotal = creditNoteData[0]['DocTotal']
                    if str(SalesType).lower() == "net":
                        cnDocTotal = creditNoteData[0]['NetTotal']
                    # endif
                # endif

                tempTotalSales = float(totalSalesByBp) - float(cnDocTotal)
                bpData = {
                    "CardCode": CardCode,
                    "CardName": CardName,
                    "TotalSales": round(tempTotalSales, 2)
                }
                dataContext.append(bpData)
                TotalSales = TotalSales + tempTotalSales
        

        TotalSales = round(TotalSales, 2)
        TotalReceivePayment = round(TotalReceivePayment, 2)
        DifferenceAmount = round(PendingTotal, 2)
        # DifferenceAmount = round(float(float(TotalSales) - float(allPayment)), 2)

        return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": TotalSales, "TotalReceivePayment": TotalReceivePayment, "DifferenceAmount": DifferenceAmount})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})




# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# @api_view(['POST'])
# def filter_receivable_dashboard(request):
#     try:
#         print("filter_receivable_dashboard", request.data)
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         SalesPersonCode = request.data['SalesPersonCode']
#         Filter        = request.data['Filter']
#         FromDate      = str(request.data['FromDate'])
#         ToDate        = str(request.data['ToDate'])
#         DueDaysGroup  = request.data['DueDaysGroup']
#         SearchText    = request.data['SearchText']
#         OrderByName   = str(request.data['OrderByName']).strip()
#         OrderByAmt    = str(request.data['OrderByAmt']).strip()
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         zones = getZoneByEmployee(SalesPersonCode)
#         zonesStr = "','".join(zones)
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         orderby = ""
#         if str(OrderByName).lower() == 'a-z':
#             orderby = "Order By CardName asc"
#         elif str(OrderByName).lower() == 'z-a':
#             orderby = "Order By CardName desc"
#         elif str(OrderByAmt).lower() == 'asc':
#             orderby = "Order By TotalPending asc"
#         elif str(OrderByAmt).lower() == 'desc':
#             orderby = "Order By TotalPending desc"
#         else:
#             orderby = "Order By DocDate asc"
#         # endElse
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         overDuesQuery = ""
#         if DueDaysGroup != "":
#             overDuesQuery = f"AND DueDaysGroup = '{DueDaysGroup}'"
#         # endIf
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         limitQuery = ""
#         if 'PageNo' in request.data:
#             PageNo = int(request.data['PageNo'])
#             MaxSize = request.data['MaxSize']
#             if str(MaxSize).lower() != "all":   
#                 size = int(MaxSize)
#                 endWith = (PageNo * size)
#                 startWith = (endWith - size)
#                 # dataContext = dataContext[startWith:endWith]
#                 limitQuery = f"Limit {startWith}, {MaxSize}"
#             # endIf
#         # endIf
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         groupByQuery = "CardCode"
#         SearchQuery = ""
#         fieldsNamesForQuery = "CardCode as GroupCode, CardName as GroupName,"
#         selectGroupField = ""
#         if str(Filter).lower() == 'group':
#             groupByQuery = "GroupCode"
#             fieldsNamesForQuery = "GroupCode, GroupName,"
#             if str(SearchText) != '':
#                 SearchQuery = f"AND (GroupCode like '%%{SearchText}%%')"
#         elif str(Filter).lower() == 'zone':
#             groupByQuery = "U_U_UTL_Zone"
#             fieldsNamesForQuery = "U_U_UTL_Zone as GroupCode, U_U_UTL_Zone as GroupName,"
#             if str(SearchText) != '':
#                 SearchQuery = f"AND (U_U_UTL_Zone like '%%{SearchText}%%')"
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
#         mycursor = mydb.cursor(dictionary=True, buffered=True)
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         receiableData = []
#         sqlQuery = f"""
#             SELECT
#                 {fieldsNamesForQuery}
#                 SUM(TotalDue) AS TotalPending
#             FROM BusinessPartner_receivable
#             WHERE
#                 CronUpdateCount =(SELECT MAX(CronUpdateCount) FROM BusinessPartner_receivable) - 1
#                 AND U_U_UTL_Zone IN('{zonesStr}')
#                 {SearchQuery}
#                 {overDuesQuery}
#             GROUP BY {groupByQuery}
#             {orderby}
#             {limitQuery};
#         """

#         print(sqlQuery)
#         mycursor.execute(sqlQuery)
#         receiableData = mycursor.fetchall()

#         dataContext = []
#         totalSales = 0
#         totalPayments = 0
#         totalPendings = 0
#         # for one bp Receipt and Pending
#         totalPaybal = 0
#         print(">>>>>> No of Objs", len(receiableData))
#         for groupObj in receiableData:
#             GroupCode     = groupObj['GroupCode']
#             GroupName     = groupObj['GroupName']
#             DocTotal      = groupObj['TotalPending']
#             PaidToDateSys = groupObj['TotalPending']
#             TotalPending  = groupObj['TotalPending']

#             bpData = {
#                 "GroupName": GroupName,
#                 "GroupCode": GroupCode,
#                 "TotalSales": round(TotalPending, 2)
#             }
#             dataContext.append(bpData)
#             totalSales = float(totalSales) + float(DocTotal)
#             totalPayments = float(totalPayments) + float(PaidToDateSys)
#             totalPendings = float(totalPendings) + float(TotalPending)


#         TotalSales = totalSales
#         TotalReceivePayment = round(totalPayments, 2)
#         DifferenceAmount = round(float(totalPendings), 2)
#         # DifferenceAmount = round(float(float(TotalSales) - float(allPayment)), 2)

#         return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": TotalSales, "TotalReceivePayment": TotalReceivePayment, "DifferenceAmount": DifferenceAmount})
    
#     except Exception as e:
#         return Response({"message": str(e),"status": 201,"data":[]})



# @api_view(['POST'])
# def filter_receivable_dashboard(request):
#     try:
#         print("filter_receivable_dashboard", request.data)
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         SalesPersonCode = request.data['SalesPersonCode']
#         Filter        = request.data['Filter']
#         FromDate      = str(request.data['FromDate'])
#         ToDate        = str(request.data['ToDate'])
#         DueDaysGroup  = request.data['DueDaysGroup']
#         SearchText    = request.data['SearchText']
#         OrderByName   = str(request.data['OrderByName']).strip()
#         OrderByAmt    = str(request.data['OrderByAmt']).strip()
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         zones = getZoneByEmployee(SalesPersonCode)
#         zonesStr = "','".join(zones)
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         orderby = ""
#         if str(OrderByName).lower() == 'a-z':
#             orderby = "Order By CardName asc"
#         elif str(OrderByName).lower() == 'z-a':
#             orderby = "Order By CardName desc"
#         elif str(OrderByAmt).lower() == 'asc':
#             orderby = "Order By TotalPending asc"
#         elif str(OrderByAmt).lower() == 'desc':
#             orderby = "Order By TotalPending desc"
#         else:
#             orderby = "Order By DocDate asc"
#         # endElse
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         overDuesQuery = ""
#         if DueDaysGroup != "":
#             if DueDaysGroup == "90":
#                 overDuesQuery = f"AND DueDaysGroup > '{DueDaysGroup}'"
#             else:
#                 overDuesQuery = f"AND DueDaysGroup = '{DueDaysGroup}'"
#         # endIf
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         limitQuery = ""
#         if 'PageNo' in request.data:
#             PageNo = int(request.data['PageNo'])
#             MaxSize = request.data['MaxSize']
#             if str(MaxSize).lower() != "all":   
#                 size = int(MaxSize)
#                 endWith = (PageNo * size)
#                 startWith = (endWith - size)
#                 # dataContext = dataContext[startWith:endWith]
#                 limitQuery = f"Limit {startWith}, {MaxSize}"
#             # endIf
#         # endIf
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         groupByQuery = "CardCode"
#         SearchQuery = ""
#         fieldsNamesForQuery = "CardCode as GroupCode, CardName as GroupName,"
#         selectGroupField = ""
#         if str(Filter).lower() == 'group':
#             groupByQuery = "GroupCode"
#             fieldsNamesForQuery = "GroupCode, GroupName,"
#             if str(SearchText) != '':
#                 SearchQuery = f"AND (GroupCode like '%%{SearchText}%%')"
#         elif str(Filter).lower() == 'zone':
#             groupByQuery = "U_U_UTL_Zone"
#             fieldsNamesForQuery = "U_U_UTL_Zone as GroupCode, U_U_UTL_Zone as GroupName,"
#             if str(SearchText) != '':
#                 SearchQuery = f"AND (U_U_UTL_Zone like '%%{SearchText}%%')"
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
#         mycursor = mydb.cursor(dictionary=True, buffered=True)
#         # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#         receiableData = []
#         sqlQuery = f"""
#             SELECT
#                 {fieldsNamesForQuery}
#                 SUM(TotalDue) AS TotalPending
#             FROM BusinessPartner_receivable
#             WHERE
#                 CronUpdateCount =(SELECT MAX(CronUpdateCount) FROM BusinessPartner_receivable) - 1
#                 AND U_U_UTL_Zone IN('{zonesStr}')
#                 {SearchQuery}
#                 {overDuesQuery}
#             GROUP BY {groupByQuery}
#             {orderby}
#             {limitQuery};
#         """

#         print(sqlQuery)
#         mycursor.execute(sqlQuery)
#         receiableData = mycursor.fetchall()

#         dataContext = []
#         totalSales = 0
#         totalPayments = 0
#         totalPendings = 0
#         # for one bp Receipt and Pending
#         totalPaybal = 0
#         print(">>>>>> No of Objs", len(receiableData))
#         for groupObj in receiableData:
#             GroupCode     = groupObj['GroupCode']
#             GroupName     = groupObj['GroupName']
#             DocTotal      = groupObj['TotalPending']
#             PaidToDateSys = groupObj['TotalPending']
#             TotalPending  = groupObj['TotalPending']

#             bpData = {
#                 "GroupName": GroupName,
#                 "GroupCode": GroupCode,
#                 "TotalSales": round(TotalPending, 2)
#             }
#             dataContext.append(bpData)
#             totalSales = float(totalSales) + float(DocTotal)
#             totalPayments = float(totalPayments) + float(PaidToDateSys)
#             totalPendings = float(totalPendings) + float(TotalPending)


#         TotalSales = totalSales
#         TotalReceivePayment = round(totalPayments, 2)
#         DifferenceAmount = round(float(totalPendings), 2)
#         # DifferenceAmount = round(float(float(TotalSales) - float(allPayment)), 2)

#         return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": TotalSales, "TotalReceivePayment": TotalReceivePayment, "DifferenceAmount": DifferenceAmount})
    
#     except Exception as e:
#         return Response({"message": str(e),"status": 201,"data":[]})

    

@api_view(['POST'])
def filter_receivable_dashboard(request):
    try:
        print("filter_receivable_dashboard", request.data)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SalesPersonCode = request.data['SalesPersonCode']
        Filter        = request.data['Filter']
        FromDate      = str(request.data['FromDate'])
        ToDate        = str(request.data['ToDate'])
        DueDaysGroup  = request.data['DueDaysGroup']
        SearchText    = request.data['SearchText']
        OrderByName   = str(request.data['OrderByName']).strip()
        OrderByAmt    = str(request.data['OrderByAmt']).strip()
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        zones = getZoneByEmployee(SalesPersonCode)
        zonesStr = "','".join(zones)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        orderby = "Order By DocDate asc"
        # if str(OrderByName).lower() == 'a-z':
        #     orderby = "Order By CardName asc"
        # elif str(OrderByName).lower() == 'z-a':
        #     orderby = "Order By CardName desc"
        # elif str(OrderByAmt).lower() == 'asc':
        #     orderby = "Order By TotalPending asc"
        # elif str(OrderByAmt).lower() == 'desc':
        #     orderby = "Order By TotalPending desc"
        # else:
        #     orderby = "Order By DocDate asc"
        # endElse
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        overDuesQuery = ""
        if DueDaysGroup != "":
            if DueDaysGroup == "90":
                overDuesQuery = f"AND DueDaysGroup > '{DueDaysGroup}'"
            else:
                overDuesQuery = f"AND DueDaysGroup = '{DueDaysGroup}'"
        # endIf
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        limitQuery = ""
        if 'PageNo' in request.data:
            PageNo = int(request.data['PageNo'])
            MaxSize = request.data['MaxSize']
            if str(MaxSize).lower() != "all":   
                size = int(MaxSize)
                endWith = (PageNo * size)
                startWith = (endWith - size)
                # dataContext = dataContext[startWith:endWith]
                limitQuery = f"Limit {startWith}, {MaxSize}"
            # endIf
        # endIf
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        groupByQuery = "CardCode"
        SearchQuery = ""
        fieldsNamesForQuery = "CardCode as GroupCode, CardName as GroupName,"
        selectGroupField = ""
        if str(Filter).lower() == 'group':
            groupByQuery = "GroupCode"
            fieldsNamesForQuery = "GroupCode, GroupName,"
            if str(SearchText) != '':
                SearchQuery = f"AND (GroupCode like '%%{SearchText}%%')"
            if str(OrderByName).lower() == 'a-z':
                orderby = "Order By GroupName asc"
            elif str(OrderByName).lower() == 'z-a':
                orderby = "Order By GroupName desc"
            elif str(OrderByAmt).lower() == 'asc':
                orderby = "Order By TotalPending asc"
            elif str(OrderByAmt).lower() == 'desc':
                orderby = "Order By TotalPending desc"
        elif str(Filter).lower() == 'zone':
            groupByQuery = "U_U_UTL_Zone"
            fieldsNamesForQuery = "U_U_UTL_Zone as GroupCode, U_U_UTL_Zone as GroupName,"
            if str(SearchText) != '':
                SearchQuery = f"AND (U_U_UTL_Zone like '%%{SearchText}%%')"
                
            if str(OrderByName).lower() == 'a-z':
                orderby = "Order By U_U_UTL_Zone asc"
            elif str(OrderByName).lower() == 'z-a':
                orderby = "Order By U_U_UTL_Zone desc"
            elif str(OrderByAmt).lower() == 'asc':
                orderby = "Order By TotalPending asc"
            elif str(OrderByAmt).lower() == 'desc':
                orderby = "Order By TotalPending desc"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        receiableData = []
        sqlQuery = f"""
            SELECT
                {fieldsNamesForQuery}
                SUM(TotalDue) AS TotalPending
            FROM BusinessPartner_receivable
            WHERE
                CronUpdateCount =(SELECT MAX(CronUpdateCount) FROM BusinessPartner_receivable) - 1
                AND U_U_UTL_Zone IN('{zonesStr}')
                {SearchQuery}
                {overDuesQuery}
            GROUP BY {groupByQuery}
            {orderby}
            {limitQuery};
        """

        print(sqlQuery)
        mycursor.execute(sqlQuery)
        receiableData = mycursor.fetchall()

        dataContext = []
        totalSales = 0
        totalPayments = 0
        totalPendings = 0
        # for one bp Receipt and Pending
        totalPaybal = 0
        print(">>>>>> No of Objs", len(receiableData))
        for groupObj in receiableData:
            GroupCode     = groupObj['GroupCode']
            GroupName     = groupObj['GroupName']
            DocTotal      = groupObj['TotalPending']
            PaidToDateSys = groupObj['TotalPending']
            TotalPending  = groupObj['TotalPending']

            bpData = {
                "GroupName": GroupName,
                "GroupCode": GroupCode,
                "TotalSales": round(TotalPending, 2)
            }
            dataContext.append(bpData)
            totalSales = float(totalSales) + float(DocTotal)
            totalPayments = float(totalPayments) + float(PaidToDateSys)
            totalPendings = float(totalPendings) + float(TotalPending)


        TotalSales = totalSales
        TotalReceivePayment = round(totalPayments, 2)
        DifferenceAmount = round(float(totalPendings), 2)
        # DifferenceAmount = round(float(float(TotalSales) - float(allPayment)), 2)

        return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": TotalSales, "TotalReceivePayment": TotalReceivePayment, "DifferenceAmount": DifferenceAmount})
    
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})





@api_view(['POST'])
def filter_payable_dashboard(request):
    try:
        print("filter_payable_dashboard", request.data)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SalesPersonCode = request.data['SalesPersonCode']
        Filter        = request.data['Filter']
        FromDate      = str(request.data['FromDate'])
        ToDate        = str(request.data['ToDate'])
        DueDaysGroup  = request.data['DueDaysGroup']
        SearchText    = request.data['SearchText']
        OrderByName   = str(request.data['OrderByName']).strip()
        OrderByAmt    = str(request.data['OrderByAmt']).strip()
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        zones = getZoneByEmployee(SalesPersonCode)
        zonesStr = "','".join(zones)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        orderby = ""
        if str(OrderByName).lower() == 'a-z':
            orderby = "Order By CardName asc"
        elif str(OrderByName).lower() == 'z-a':
            orderby = "Order By CardName desc"
        elif str(OrderByAmt).lower() == 'asc':
            orderby = "Order By TotalPending asc"
        elif str(OrderByAmt).lower() == 'desc':
            orderby = "Order By TotalPending desc"
        else:
            orderby = "Order By DocDate asc"
        # endElse
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        overDuesQuery = ""
        if DueDaysGroup != "":
            if DueDaysGroup == "90":
                overDuesQuery = f"AND DueDaysGroup > '{DueDaysGroup}'"
            else:
                overDuesQuery = f"AND DueDaysGroup = '{DueDaysGroup}'"
        # endIf
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        limitQuery = ""
        if 'PageNo' in request.data:
            PageNo = int(request.data['PageNo'])
            MaxSize = request.data['MaxSize']
            if str(MaxSize).lower() != "all":   
                size = int(MaxSize)
                endWith = (PageNo * size)
                startWith = (endWith - size)
                # dataContext = dataContext[startWith:endWith]
                limitQuery = f"Limit {startWith}, {MaxSize}"
            # endIf
        # endIf
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        groupByQuery = "CardCode"
        SearchQuery = ""
        fieldsNamesForQuery = "CardCode as GroupCode, CardName as GroupName,"
        selectGroupField = ""
        if str(Filter).lower() == 'group':
            groupByQuery = "GroupCode"
            fieldsNamesForQuery = "GroupCode, GroupName,"
            if str(SearchText) != '':
                SearchQuery = f"AND (GroupCode like '%%{SearchText}%%')"
        elif str(Filter).lower() == 'zone':
            groupByQuery = "U_U_UTL_Zone"
            fieldsNamesForQuery = "U_U_UTL_Zone as GroupCode, U_U_UTL_Zone as GroupName,"
            if str(SearchText) != '':
                SearchQuery = f"AND (U_U_UTL_Zone like '%%{SearchText}%%')"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        receiableData = []
        sqlQuery = f"""
            SELECT
                {fieldsNamesForQuery}
                SUM(TotalDue) AS TotalPending
            FROM BusinessPartner_payable
            WHERE
                CronUpdateCount =(SELECT MAX(CronUpdateCount) FROM BusinessPartner_payable) - 1
                AND U_U_UTL_Zone IN('{zonesStr}')
                {SearchQuery}
                {overDuesQuery}
            GROUP BY {groupByQuery}
            {orderby}
            {limitQuery};
        """

        print(sqlQuery)
        mycursor.execute(sqlQuery)
        receiableData = mycursor.fetchall()

        dataContext = []
        totalSales = 0
        totalPayments = 0
        totalPendings = 0
        # for one bp Receipt and Pending
        totalPaybal = 0
        print(">>>>>> No of Objs", len(receiableData))
        for groupObj in receiableData:
            GroupCode     = groupObj['GroupCode']
            GroupName     = groupObj['GroupName']
            DocTotal      = groupObj['TotalPending']
            PaidToDateSys = groupObj['TotalPending']
            TotalPending  = groupObj['TotalPending']

            bpData = {
                "GroupName": GroupName,
                "GroupCode": GroupCode,
                "TotalSales": round(TotalPending, 2)
            }
            dataContext.append(bpData)
            totalSales = float(totalSales) + float(DocTotal)
            totalPayments = float(totalPayments) + float(PaidToDateSys)
            totalPendings = float(totalPendings) + float(TotalPending)


        TotalSales = totalSales
        TotalReceivePayment = round(totalPayments, 2)
        DifferenceAmount = round(float(totalPendings), 2)
        # DifferenceAmount = round(float(float(TotalSales) - float(allPayment)), 2)

        return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": TotalSales, "TotalReceivePayment": TotalReceivePayment, "DifferenceAmount": DifferenceAmount})
    
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def receivable_dashboard(request):
    try:
        print("receivable_dashboard", request.data)
        Filter = request.data['Filter']
        Code = request.data['Code']
        SalesType = request.data['Type']
        FromDate = str(request.data['FromDate'])
        ToDate = str(request.data['ToDate'])

        SalesPersonCode = -1
        if 'SalesPersonCode' in request.data:
            SalesPersonCode = request.data['SalesPersonCode']
        zones = getZoneByEmployee(SalesPersonCode)
        print(zones)
        SearchText = ""
        if 'SearchText' in request.data:
            SearchText = request.data['SearchText']
        # endIf
        OrderByName = "" #a-z/z-a
        OrderByAmt = "" #desc
        if 'OrderByName' in request.data:
            OrderByName = str(request.data['OrderByName']).strip()
        # endIf
        if 'OrderByAmt' in request.data:
            OrderByAmt = str(request.data['OrderByAmt']).strip()
        # endIf
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        orderby = ""
        if str(OrderByName).lower() == 'a-z':
            orderby = "Order By CardName asc"
        elif str(OrderByName).lower() == 'z-a':
            orderby = "Order By CardName desc"
        elif str(OrderByAmt).lower() == 'asc':
            orderby = "Order By TotalPending asc"
        elif str(OrderByAmt).lower() == 'desc':
            orderby = "Order By TotalPending desc"
        else:
            orderby = "Order By DocDate asc"
        # endElse
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        DueDaysGroup = ''
        if 'DueDaysGroup' in request.data:
            DueDaysGroup = request.data['DueDaysGroup']
        # endIf
        overDuesQuery = ""
        if DueDaysGroup != "":
            overDuesQuery = f"AND DueDaysGroup = '{DueDaysGroup}'"
        # endIf
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        limitQuery = ""
        if 'PageNo' in request.data:
            PageNo = int(request.data['PageNo'])
            MaxSize = request.data['MaxSize']
            if str(MaxSize).lower() != "all":   
                size = int(MaxSize)
                endWith = (PageNo * size)
                startWith = (endWith - size)
                # dataContext = dataContext[startWith:endWith]
                limitQuery = f"Limit {startWith}, {MaxSize}"
            # endIf
        # endIf
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        cardCodesList = []
        if str(Filter).lower() == 'group':
            cardCodesList = list(BusinessPartner.objects.filter(Q(GroupCode = Code, U_U_UTL_Zone__in = zones) & Q( Q(CardCode__icontains = SearchText) | Q(CardName__icontains = SearchText))).values_list("CardCode", flat=True))
        elif str(Filter).lower() == 'zone':
            cardCodesList = list(BusinessPartner.objects.filter(Q(U_U_UTL_Zone = Code) & Q( Q(CardCode__icontains = SearchText) | Q(CardName__icontains = SearchText))).values_list("CardCode", flat=True))
        else:
            cardCodesList = list(BusinessPartner.objects.filter(Q(U_U_UTL_Zone__in = zones) & Q( Q(CardCode__icontains = SearchText) | Q(CardName__icontains = SearchText))).values_list("CardCode", flat=True))

        cardCodeStr = "','".join(cardCodesList)
        # print("cardCodeStr", cardCodeStr)

        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        receiableData = []
        sqlQuery = f"""
            SELECT *, SUM(`TotalDue`) as TotalPending FROM `BusinessPartner_receivable`
            WHERE
                CardCode IN('{cardCodeStr}')
                AND `CronUpdateCount` = (SELECT MAX(`CronUpdateCount`) FROM BusinessPartner_receivable) - 1
                {overDuesQuery}
            GROUP BY 
                CardCode 
            {orderby}
            {limitQuery};
        """

        print(sqlQuery)
        mycursor.execute(sqlQuery)
        receiableData = mycursor.fetchall()

        dataContext = []
        totalSales = 0
        # for one bp Receipt and Pending
        totalPaybal = 0
        print(">>>>>> No of Objs", len(receiableData))
        for obj in receiableData:
            # print("CardCode", obj['CardCode'])
            CardCode        = obj['CardCode']
            CardName        = obj['CardName']
            PendingTotal    = round(float(obj['TotalPending']), 2)
            ContactPerson   = obj['ContactPerson']
            EmailAddress    = obj['EmailAddress']
            Phone1          = obj['MobileNo']
            GSTIN           = obj['GSTIN']
            BPAddress       = obj['BPAddresses']
            CreditLimit     = obj['CreditLimit']
            CreditLimitDayes = obj['CreditLimitDayes']
            GroupName       = obj['GroupName']

            # ______________________________
            totalPaybal = totalPaybal + PendingTotal

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            
            AvgPayDays = 0
            bpData = {
                "CardName": CardName,
                "CardCode": CardCode,
                "EmailAddress": EmailAddress,
                "Phone1": Phone1,
                "GSTIN": GSTIN,
                "BPAddress": BPAddress,
                "GroupName": GroupName,
                "CreditLimit": CreditLimit,
                "CreditLimitDayes": CreditLimitDayes,
                "TotalSales": (round(float(PendingTotal))),
                "TotalReceivePayment": 0,
                "DifferenceAmount":(round(float(PendingTotal))),
                "AvgPayDays": round(AvgPayDays, 2)
            }
            dataContext.append(bpData)

        TotalSales = totalSales
        TotalReceivePayment = 0
        DifferenceAmount = (round(float(totalPaybal)))

        return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": TotalSales, "TotalReceivePayment": TotalReceivePayment, "DifferenceAmount": DifferenceAmount})
    
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})



@api_view(['POST'])
def payable_dashboard(request):
    try:
        print("payable_dashboard", request.data)
        Filter = request.data['Filter']
        Code = request.data['Code']
        SalesType = request.data['Type']
        FromDate = str(request.data['FromDate'])
        ToDate = str(request.data['ToDate'])

        SalesPersonCode = -1
        if 'SalesPersonCode' in request.data:
            SalesPersonCode = request.data['SalesPersonCode']
        zones = getZoneByEmployee(SalesPersonCode)
        print(zones)
        SearchText = ""
        if 'SearchText' in request.data:
            SearchText = request.data['SearchText']
        # endIf
        OrderByName = "" #a-z/z-a
        OrderByAmt = "" #desc
        if 'OrderByName' in request.data:
            OrderByName = str(request.data['OrderByName']).strip()
        # endIf
        if 'OrderByAmt' in request.data:
            OrderByAmt = str(request.data['OrderByAmt']).strip()
        # endIf
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        orderby = ""
        if str(OrderByName).lower() == 'a-z':
            orderby = "Order By CardName asc"
        elif str(OrderByName).lower() == 'z-a':
            orderby = "Order By CardName desc"
        elif str(OrderByAmt).lower() == 'asc':
            orderby = "Order By TotalPending asc"
        elif str(OrderByAmt).lower() == 'desc':
            orderby = "Order By TotalPending desc"
        else:
            orderby = "Order By DocDate asc"
        # endElse
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        DueDaysGroup = ''
        if 'DueDaysGroup' in request.data:
            DueDaysGroup = request.data['DueDaysGroup']
        # endIf
        overDuesQuery = ""
        if DueDaysGroup != "":
            overDuesQuery = f"AND DueDaysGroup = '{DueDaysGroup}'"
        # endIf
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        limitQuery = ""
        if 'PageNo' in request.data:
            PageNo = int(request.data['PageNo'])
            MaxSize = request.data['MaxSize']
            if str(MaxSize).lower() != "all":   
                size = int(MaxSize)
                endWith = (PageNo * size)
                startWith = (endWith - size)
                # dataContext = dataContext[startWith:endWith]
                limitQuery = f"Limit {startWith}, {MaxSize}"
            # endIf
        # endIf
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        cardCodesList = []
        if str(Filter).lower() == 'group':
            cardCodesList = list(BusinessPartner.objects.filter(Q(GroupCode = Code, U_U_UTL_Zone__in = zones) & Q( Q(CardCode__icontains = SearchText) | Q(CardName__icontains = SearchText))).values_list("CardCode", flat=True))
        elif str(Filter).lower() == 'zone':
            cardCodesList = list(BusinessPartner.objects.filter(Q(U_U_UTL_Zone = Code) & Q( Q(CardCode__icontains = SearchText) | Q(CardName__icontains = SearchText))).values_list("CardCode", flat=True))
        else:
            cardCodesList = list(BusinessPartner.objects.filter(Q(U_U_UTL_Zone__in = zones) & Q( Q(CardCode__icontains = SearchText) | Q(CardName__icontains = SearchText))).values_list("CardCode", flat=True))

        cardCodeStr = "','".join(cardCodesList)
        # print("cardCodeStr", cardCodeStr)

        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        receiableData = []
        sqlQuery = f"""
            SELECT *, SUM(`TotalDue`) as TotalPending FROM `BusinessPartner_payable`
            WHERE
                CardCode IN('{cardCodeStr}')
                AND `CronUpdateCount` = (SELECT MAX(`CronUpdateCount`) FROM BusinessPartner_payable) - 1
                {overDuesQuery}
            GROUP BY 
                CardCode 
            {orderby}
            {limitQuery};
        """

        print(sqlQuery)
        mycursor.execute(sqlQuery)
        receiableData = mycursor.fetchall()

        dataContext = []
        totalSales = 0
        # for one bp Receipt and Pending
        totalPaybal = 0
        print(">>>>>> No of Objs", len(receiableData))
        for obj in receiableData:
            # print("CardCode", obj['CardCode'])
            CardCode        = obj['CardCode']
            CardName        = obj['CardName']
            PendingTotal    = round(float(obj['TotalPending']), 2)
            ContactPerson   = obj['ContactPerson']
            EmailAddress    = obj['EmailAddress']
            Phone1          = obj['MobileNo']
            GSTIN           = obj['GSTIN']
            BPAddress       = obj['BPAddresses']
            CreditLimit     = obj['CreditLimit']
            CreditLimitDayes = obj['CreditLimitDayes']
            GroupName       = obj['GroupName']

            # _______________________________________
            totalPaybal = totalPaybal + PendingTotal

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            
            AvgPayDays = 0
            bpData = {
                "CardName": CardName,
                "CardCode": CardCode,
                "EmailAddress": EmailAddress,
                "Phone1": Phone1,
                "GSTIN": GSTIN,
                "BPAddress": BPAddress,
                "GroupName": GroupName,
                "CreditLimit": CreditLimit,
                "CreditLimitDayes": CreditLimitDayes,
                "TotalSales": (round(float(PendingTotal))),
                "TotalReceivePayment": 0,
                "DifferenceAmount":(round(float(PendingTotal))),
                "AvgPayDays": round(AvgPayDays, 2)
            }
            dataContext.append(bpData)

        TotalSales = totalSales
        TotalReceivePayment = 0
        DifferenceAmount = (round(float(totalPaybal)))

        return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": TotalSales, "TotalReceivePayment": TotalReceivePayment, "DifferenceAmount": DifferenceAmount})
    
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})





# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def due_payment_dashboard_count(request):
    try:
        # print("due_payment_dashboard_count", request.data)
        SalesPersonCode = request.data['SalesPersonCode']
        DueDaysGroup = request.data['DueDaysGroup']
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        dueDaysGroupQuery = "AND `DueDate` >= CURDATE()"
        if str(DueDaysGroup) == '-1': # overdue invoices
            dueDaysGroupQuery = "AND `DueDate` < CURDATE()"
            # print("over days", dueDaysGroupQuery)
        elif DueDaysGroup == "all": # due date in next 7 days and over due
            dueDaysGroupQuery = f"AND `DueDate` <= DATE_ADD(CURDATE(), INTERVAL 7 DAY)"
            # print("all days", dueDaysGroupQuery)
        elif DueDaysGroup != "": # due date in next DueDaysGroup
            dueDaysGroupQuery = f"AND `DueDate` >= CURDATE() AND `DueDate` <= DATE_ADD(CURDATE(), INTERVAL {DueDaysGroup} DAY)"
            # print("days", dueDaysGroupQuery)
        
        
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        zones = getZoneByEmployee(SalesPersonCode)
        zonesStr = "','".join(zones)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        sqlQuery = f"""
            SELECT 
                *, SUM(`TotalDue`) as TotalPending 
            FROM `BusinessPartner_receivable`
            WHERE
                U_U_UTL_Zone IN('{zonesStr}') AND
                `CronUpdateCount` = (SELECT MAX(`CronUpdateCount`) FROM BusinessPartner_receivable) - 1 
                {dueDaysGroupQuery}
        """
        # `DueDate` >= CURDATE() AND DueDate` <= DATE_ADD(CURDATE(), INTERVAL {DueDaysGroup} DAY)
        # print(sqlQuery)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mycursor.execute(sqlQuery)
        duePaymentData = mycursor.fetchall()
        dataContext = []
        totalPaybal = 0
        for obj in duePaymentData:
            print("CardCode", obj['CardCode'])
            totalPaybal    = round(float(obj['TotalPending']), 2)
        # endFor
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        TotalPaybal = (round(float(totalPaybal)))
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        return Response({"message": "Success","status": 200, "data":dataContext, "TotalPaybal": TotalPaybal})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
    

@api_view(['POST'])
def due_payable_payment_dashboard_count(request):
    try:
        print("due_payable_payment_dashboard_count", request.data)
        SalesPersonCode = request.data['SalesPersonCode']
        DueDaysGroup = request.data['DueDaysGroup']
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        dueDaysGroupQuery = "AND `DueDate` >= CURDATE()"
        if str(DueDaysGroup) == '-1': # overdue invoices
            dueDaysGroupQuery = "AND `DueDate` < CURDATE()"
            print("over days", dueDaysGroupQuery)

        elif DueDaysGroup == "all": # due date in next 7 days and over due
            dueDaysGroupQuery = f"AND `DueDate` <= DATE_ADD(CURDATE(), INTERVAL 7 DAY)"
            print("all days", dueDaysGroupQuery)

        elif DueDaysGroup != "": # due date in next DueDaysGroup
            dueDaysGroupQuery = f"AND `DueDate` >= CURDATE() AND `DueDate` <= DATE_ADD(CURDATE(), INTERVAL {DueDaysGroup} DAY)"
            print("days", dueDaysGroupQuery)
        
        
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        zones = getZoneByEmployee(SalesPersonCode)
        zonesStr = "','".join(zones)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        sqlQuery = f"""
            SELECT 
                *, SUM(`TotalDue`) as TotalPending 
            FROM `BusinessPartner_payable`
            WHERE
                U_U_UTL_Zone IN('{zonesStr}') AND
                `CronUpdateCount` = (SELECT MAX(`CronUpdateCount`) FROM BusinessPartner_payable) - 1 
                {dueDaysGroupQuery}
        """
        # `DueDate` >= CURDATE() AND DueDate` <= DATE_ADD(CURDATE(), INTERVAL {DueDaysGroup} DAY)
        print(sqlQuery)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mycursor.execute(sqlQuery)
        duePaymentData = mycursor.fetchall()
        dataContext = []
        totalPaybal = 0
        for obj in duePaymentData:
            print("CardCode", obj['CardCode'])
            totalPaybal    = round(float(obj['TotalPending']), 2)
        # endFor
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        TotalPaybal = (round(float(totalPaybal)))
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        return Response({"message": "Success","status": 200, "data":dataContext, "TotalPaybal": TotalPaybal})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})



# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def due_payment_dashboard(request):
    try:
        try:
            Filter = request.data['Filter']
            Code = request.data['Code']
        except:
            Filter = ""
            Code = ""
        
        print("due_payment_dashboard", request.data)
        Filter = Filter
        Code = Code
        SalesPersonCode = request.data['SalesPersonCode']
        SearchText   = request.data['SearchText']
        OrderByName  = str(request.data['OrderByName']).strip()
        OrderByAmt   = str(request.data['OrderByAmt']).strip()
        DueDaysGroup = request.data['DueDaysGroup']
        PageNo       = int(request.data['PageNo'])
        MaxSize      = request.data['MaxSize']
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        zones    = getZoneByEmployee(SalesPersonCode)
        zonesStr = "','".join(zones)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        orderby = ""
        if str(OrderByName).lower() == 'a-z':
            orderby = "Order By CardName asc"
        elif str(OrderByName).lower() == 'z-a':
            orderby = "Order By CardName desc"
        elif str(OrderByAmt).lower() == 'asc':
            orderby = "Order By TotalPending asc"
        elif str(OrderByAmt).lower() == 'desc':
            orderby = "Order By TotalPending desc"
        else:
            orderby = "Order By DocDate asc"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SearchQuery = ''
        if str(SearchText) != '':
            SearchQuery = f"AND (CardCode like '%%{SearchText}%%' OR CardName like '%%{SearchText}%%')"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        filterBy = f"U_U_UTL_Zone IN('{zonesStr}')"
        if str(Filter).lower() == 'group':
            filterBy = f"U_U_UTL_Zone IN('{zonesStr}') AND GroupCode = '{Code}'"
        elif str(Filter).lower() == 'zone':
            filterBy = f"U_U_UTL_Zone = '{Code}'"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        limitQuery = ""
        if str(MaxSize).lower() != "all":   
            size = int(MaxSize)
            endWith = (PageNo * size)
            startWith = (endWith - size)
            limitQuery = f"Limit {startWith}, {MaxSize}"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        dueDaysGroupQuery = "AND `DueDate` >= CURDATE()"
        if str(DueDaysGroup) == '-1': # overdue invoices
            dueDaysGroupQuery = "AND `DueDate` < CURDATE()"
        elif DueDaysGroup == "all": # due date in next 7 days and over due
            dueDaysGroupQuery = f"AND `DueDate` <= DATE_ADD(CURDATE(), INTERVAL 7 DAY)"
        elif DueDaysGroup != "": # due date in next DueDaysGroup
            dueDaysGroupQuery = f"AND `DueDate` >= CURDATE() AND `DueDate` <= DATE_ADD(CURDATE(), INTERVAL {DueDaysGroup} DAY)"
        # print("all days", dueDaysGroupQuery)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        sqlQuery = f"""
            SELECT 
                *, SUM(`TotalDue`) as TotalPending 
            FROM `BusinessPartner_receivable`
            WHERE
                {filterBy} AND
                `CronUpdateCount` = (SELECT MAX(`CronUpdateCount`) FROM BusinessPartner_receivable) - 1 
                {dueDaysGroupQuery}
                {SearchQuery}
            GROUP BY 
                CardCode
            {orderby}
            {limitQuery};
        """
        print(sqlQuery)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mycursor.execute(sqlQuery)
        duePaymentData = mycursor.fetchall()
        dataContext = []
        totalPaybal = 0
        for obj in duePaymentData:
            print("CardCode", obj['CardCode'])
            CardCode         = obj['CardCode']
            CardName         = obj['CardName']
            PendingTotal     = round(float(obj['TotalPending']), 2)
            # ContactPerson  = obj['ContactPerson']
            EmailAddress     = obj['EmailAddress']
            Phone1           = obj['MobileNo']
            GSTIN            = obj['GSTIN']
            BPAddress        = obj['BPAddresses']
            CreditLimit      = obj['CreditLimit']
            CreditLimitDayes = obj['CreditLimitDayes']
            GroupName        = obj['GroupName']

            totalPaybal     = totalPaybal + PendingTotal
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            AvgPayDays = 0
            bpData = {
                "CardName": CardName,
                "CardCode": CardCode,
                "EmailAddress": EmailAddress,
                "Phone1": Phone1,
                "GSTIN": GSTIN,
                "BPAddress": BPAddress,
                "GroupName": GroupName,
                "CreditLimit": CreditLimit,
                "CreditLimitDayes": CreditLimitDayes,
                "TotalSales": (round(float(PendingTotal))),
                "TotalReceivePayment": 0,
                "DifferenceAmount":(round(float(PendingTotal))),
                "AvgPayDays": round(AvgPayDays, 2)
            }
            dataContext.append(bpData)

        TotalSales = 0
        TotalReceivePayment = 0
        DifferenceAmount = (round(float(totalPaybal)))

        return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": TotalSales, "TotalReceivePayment": TotalReceivePayment, "DifferenceAmount": DifferenceAmount})
    
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def due_payable_payment_dashboard(request):
    try:
        
        Filter = request.data['Filter'] if 'Filter' in request.data else ''
        Code = request.data['Code'] if 'Code' in request.data else ''
        
        print("due_payment_dashboard", request.data)
        Filter = Filter
        Code = Code
        SalesPersonCode = request.data['SalesPersonCode']
        SearchText   = request.data['SearchText']
        OrderByName  = str(request.data['OrderByName']).strip()
        OrderByAmt   = str(request.data['OrderByAmt']).strip()
        DueDaysGroup = request.data['DueDaysGroup']
        PageNo       = int(request.data['PageNo'])
        MaxSize      = request.data['MaxSize']
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        zones    = getZoneByEmployee(SalesPersonCode)
        zonesStr = "','".join(zones)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        orderby = ""
        if str(OrderByName).lower() == 'a-z':
            orderby = "Order By CardName asc"
        elif str(OrderByName).lower() == 'z-a':
            orderby = "Order By CardName desc"
        elif str(OrderByAmt).lower() == 'asc':
            orderby = "Order By TotalPending asc"
        elif str(OrderByAmt).lower() == 'desc':
            orderby = "Order By TotalPending desc"
        else:
            orderby = "Order By DocDate asc"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SearchQuery = ''
        if str(SearchText) != '':
            SearchQuery = f"AND (CardCode like '%%{SearchText}%%' OR CardName like '%%{SearchText}%%')"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        filterBy = f"U_U_UTL_Zone IN('{zonesStr}')"
        if str(Filter).lower() == 'group':
            filterBy = f"U_U_UTL_Zone IN('{zonesStr}') AND GroupCode = '{Code}'"
        elif str(Filter).lower() == 'zone':
            filterBy = f"U_U_UTL_Zone = '{Code}'"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        limitQuery = ""
        if str(MaxSize).lower() != "all":   
            size = int(MaxSize)
            endWith = (PageNo * size)
            startWith = (endWith - size)
            limitQuery = f"Limit {startWith}, {MaxSize}"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        dueDaysGroupQuery = "AND `DueDate` >= CURDATE()"
        if str(DueDaysGroup) == '-1': # overdue invoices
            dueDaysGroupQuery = "AND `DueDate` < CURDATE()"
        
        elif DueDaysGroup == "all": # due date in next 7 days and over due
            dueDaysGroupQuery = f"AND `DueDate` <= DATE_ADD(CURDATE(), INTERVAL 7 DAY)"
            print("all days", dueDaysGroupQuery)

        elif DueDaysGroup != "": # due date in next DueDaysGroup
            dueDaysGroupQuery = f"AND `DueDate` >= CURDATE() AND `DueDate` <= DATE_ADD(CURDATE(), INTERVAL {DueDaysGroup} DAY)"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        sqlQuery = f"""
            SELECT 
                *, SUM(`TotalDue`) as TotalPending 
            FROM `BusinessPartner_payable`
            WHERE
                {filterBy} AND
                `CronUpdateCount` = (SELECT MAX(`CronUpdateCount`) FROM BusinessPartner_payable) - 1 
                {dueDaysGroupQuery}
                {SearchQuery}
            GROUP BY 
                CardCode
            {orderby}
            {limitQuery};
        """
        print(sqlQuery)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mycursor.execute(sqlQuery)
        duePaymentData = mycursor.fetchall()
        dataContext = []
        totalPaybal = 0
        for obj in duePaymentData:
            print("CardCode", obj['CardCode'])
            CardCode        = obj['CardCode']
            CardName        = obj['CardName']
            PendingTotal    = round(float(obj['TotalPending']), 2)
            # ContactPerson   = obj['ContactPerson']
            EmailAddress    = obj['EmailAddress']
            Phone1          = obj['MobileNo']
            GSTIN           = obj['GSTIN']
            BPAddress       = obj['BPAddresses']
            CreditLimit     = obj['CreditLimit']
            CreditLimitDayes = obj['CreditLimitDayes']
            GroupName       = obj['GroupName']

            totalPaybal = totalPaybal + PendingTotal

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            
            AvgPayDays = 0
            bpData = {
                "CardName": CardName,
                "CardCode": CardCode,
                "EmailAddress": EmailAddress,
                "Phone1": Phone1,
                "GSTIN": GSTIN,
                "BPAddress": BPAddress,
                "GroupName": GroupName,
                "CreditLimit": CreditLimit,
                "CreditLimitDayes": CreditLimitDayes,
                "TotalSales": (round(float(PendingTotal))),
                "TotalReceivePayment": 0,
                "DifferenceAmount":(round(float(PendingTotal))),
                "AvgPayDays": round(AvgPayDays, 2)
            }
            dataContext.append(bpData)

        TotalSales = 0
        TotalReceivePayment = 0
        DifferenceAmount = (round(float(totalPaybal)))

        return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": TotalSales, "TotalReceivePayment": TotalReceivePayment, "DifferenceAmount": DifferenceAmount})
    
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def filter_due_payment_dashboard(request):
    try:
        print("filter_receivable_dashboard", request.data)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SalesPersonCode = request.data['SalesPersonCode']
        Filter        = request.data['Filter']
        #FromDate      = str(request.data['FromDate'])
        #ToDate        = str(request.data['ToDate'])
        DueDaysGroup  = request.data['DueDaysGroup']
        SearchText    = request.data['SearchText']
        OrderByName   = str(request.data['OrderByName']).strip()
        OrderByAmt    = str(request.data['OrderByAmt']).strip()
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        zones = getZoneByEmployee(SalesPersonCode)
        zonesStr = "','".join(zones)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        orderby = ""
        if str(OrderByName).lower() == 'a-z':
            orderby = "Order By CardName asc"
        elif str(OrderByName).lower() == 'z-a':
            orderby = "Order By CardName desc"
        elif str(OrderByAmt).lower() == 'asc':
            orderby = "Order By TotalPending asc"
        elif str(OrderByAmt).lower() == 'desc':
            orderby = "Order By TotalPending desc"
        else:
            orderby = "Order By DocDate asc"
        # endElse
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        #overDuesQuery = ""
        #if DueDaysGroup != "":
        #overDuesQuery = f"AND DueDaysGroup = '{DueDaysGroup}'"
        # endIf
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        dueDaysGroupQuery = "AND `DueDate` >= CURDATE()"
        if str(DueDaysGroup) == '-1': # overdue invoices
            dueDaysGroupQuery = "AND `DueDate` < CURDATE()"
        
        elif DueDaysGroup == "all": # due date in next 7 days and over due
            dueDaysGroupQuery = f"AND `DueDate` <= DATE_ADD(CURDATE(), INTERVAL 7 DAY)"
            print("all days", dueDaysGroupQuery)

        elif DueDaysGroup != "": # due date in next DueDaysGroup
            dueDaysGroupQuery = f"AND `DueDate` >= CURDATE() AND `DueDate` <= DATE_ADD(CURDATE(), INTERVAL {DueDaysGroup} DAY)"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        
        limitQuery = ""
        if 'PageNo' in request.data:
            PageNo = int(request.data['PageNo'])
            MaxSize = request.data['MaxSize']
            if str(MaxSize).lower() != "all":   
                size = int(MaxSize)
                endWith = (PageNo * size)
                startWith = (endWith - size)
                # dataContext = dataContext[startWith:endWith]
                limitQuery = f"Limit {startWith}, {MaxSize}"
            # endIf
        # endIf
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        groupByQuery = "CardCode"
        SearchQuery = ""
        fieldsNamesForQuery = "CardCode as GroupCode, CardName as GroupName,"
        selectGroupField = ""
        if str(Filter).lower() == 'group':
            groupByQuery = "GroupCode"
            fieldsNamesForQuery = "GroupCode, GroupName,"
            if str(SearchText) != '':
                SearchQuery = f"AND (GroupCode like '%%{SearchText}%%')"
        elif str(Filter).lower() == 'zone':
            groupByQuery = "U_U_UTL_Zone"
            fieldsNamesForQuery = "U_U_UTL_Zone as GroupCode, U_U_UTL_Zone as GroupName,"
            if str(SearchText) != '':
                SearchQuery = f"AND (U_U_UTL_Zone like '%%{SearchText}%%')"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        receiableData = []
        sqlQuery = f"""
            SELECT
                {fieldsNamesForQuery}
                SUM(TotalDue) AS TotalPending
            FROM BusinessPartner_receivable
            WHERE
                CronUpdateCount =(SELECT MAX(CronUpdateCount) FROM BusinessPartner_receivable) - 1
                AND U_U_UTL_Zone IN('{zonesStr}')
                {dueDaysGroupQuery}
                {SearchQuery}                
            GROUP BY {groupByQuery}
            {orderby}
            {limitQuery};
        """

        print(sqlQuery)
        mycursor.execute(sqlQuery)
        receiableData = mycursor.fetchall()

        dataContext = []
        totalSales = 0
        totalPayments = 0
        totalPendings = 0
        # for one bp Receipt and Pending
        totalPaybal = 0
        print(">>>>>> No of Objs", len(receiableData))
        for groupObj in receiableData:
            GroupCode     = groupObj['GroupCode']
            GroupName     = groupObj['GroupName']
            DocTotal      = groupObj['TotalPending']
            PaidToDateSys = groupObj['TotalPending']
            TotalPending  = groupObj['TotalPending']

            bpData = {
                "GroupName": GroupName,
                "GroupCode": GroupCode,
                "TotalSales": round(TotalPending, 2)
            }
            dataContext.append(bpData)
            totalSales = float(totalSales) + float(DocTotal)
            totalPayments = float(totalPayments) + float(PaidToDateSys)
            totalPendings = float(totalPendings) + float(TotalPending)


        TotalSales = totalSales
        TotalReceivePayment = round(totalPayments, 2)
        DifferenceAmount = round(float(totalPendings), 2)
        # DifferenceAmount = round(float(float(TotalSales) - float(allPayment)), 2)

        return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": TotalSales, "TotalReceivePayment": TotalReceivePayment, "DifferenceAmount": DifferenceAmount})
    
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def filter_due_payable_payment_dashboard(request):
    try:
        print("filter_due_payable_payment_dashboard", request.data)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SalesPersonCode = request.data['SalesPersonCode']
        Filter        = request.data['Filter']
        DueDaysGroup  = request.data['DueDaysGroup']
        SearchText    = request.data['SearchText']
        OrderByName   = str(request.data['OrderByName']).strip()
        OrderByAmt    = str(request.data['OrderByAmt']).strip()
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        zones = getZoneByEmployee(SalesPersonCode)
        zonesStr = "','".join(zones)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        orderby = ""
        if str(OrderByName).lower() == 'a-z':
            orderby = "Order By CardName asc"
        elif str(OrderByName).lower() == 'z-a':
            orderby = "Order By CardName desc"
        elif str(OrderByAmt).lower() == 'asc':
            orderby = "Order By TotalPending asc"
        elif str(OrderByAmt).lower() == 'desc':
            orderby = "Order By TotalPending desc"
        else:
            orderby = "Order By DocDate asc"
        # endElse
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        #overDuesQuery = ""
        #if DueDaysGroup != "":
        #overDuesQuery = f"AND DueDaysGroup = '{DueDaysGroup}'"
        # endIf
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        dueDaysGroupQuery = "AND `DueDate` >= CURDATE()"
        if str(DueDaysGroup) == '-1': # overdue invoices
            dueDaysGroupQuery = "AND `DueDate` < CURDATE()"
        
        elif DueDaysGroup == "all": # due date in next 7 days and over due
            dueDaysGroupQuery = f"AND `DueDate` <= DATE_ADD(CURDATE(), INTERVAL 7 DAY)"
            print("all days", dueDaysGroupQuery)

        elif DueDaysGroup != "": # due date in next DueDaysGroup
            dueDaysGroupQuery = f"AND `DueDate` >= CURDATE() AND `DueDate` <= DATE_ADD(CURDATE(), INTERVAL {DueDaysGroup} DAY)"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        
        limitQuery = ""
        if 'PageNo' in request.data:
            PageNo = int(request.data['PageNo'])
            MaxSize = request.data['MaxSize']
            if str(MaxSize).lower() != "all":   
                size = int(MaxSize)
                endWith = (PageNo * size)
                startWith = (endWith - size)
                # dataContext = dataContext[startWith:endWith]
                limitQuery = f"Limit {startWith}, {MaxSize}"
            # endIf
        # endIf
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        groupByQuery = "CardCode"
        SearchQuery = ""
        fieldsNamesForQuery = "CardCode as GroupCode, CardName as GroupName,"
        selectGroupField = ""
        if str(Filter).lower() == 'group':
            groupByQuery = "GroupCode"
            fieldsNamesForQuery = "GroupCode, GroupName,"
            if str(SearchText) != '':
                SearchQuery = f"AND (GroupCode like '%%{SearchText}%%')"
        elif str(Filter).lower() == 'zone':
            groupByQuery = "U_U_UTL_Zone"
            fieldsNamesForQuery = "U_U_UTL_Zone as GroupCode, U_U_UTL_Zone as GroupName,"
            if str(SearchText) != '':
                SearchQuery = f"AND (U_U_UTL_Zone like '%%{SearchText}%%')"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        receiableData = []
        sqlQuery = f"""
            SELECT
                {fieldsNamesForQuery}
                SUM(TotalDue) AS TotalPending
            FROM BusinessPartner_payable
            WHERE
                CronUpdateCount =(SELECT MAX(CronUpdateCount) FROM BusinessPartner_payable) - 1
                AND U_U_UTL_Zone IN('{zonesStr}')
                {dueDaysGroupQuery}
                {SearchQuery}                
            GROUP BY {groupByQuery}
            {orderby}
            {limitQuery};
        """

        print(sqlQuery)
        mycursor.execute(sqlQuery)
        receiableData = mycursor.fetchall()

        dataContext = []
        totalSales = 0
        totalPayments = 0
        totalPendings = 0
        # for one bp Receipt and Pending
        totalPaybal = 0
        print(">>>>>> No of Objs", len(receiableData))
        for groupObj in receiableData:
            GroupCode     = groupObj['GroupCode']
            GroupName     = groupObj['GroupName']
            DocTotal      = groupObj['TotalPending']
            PaidToDateSys = groupObj['TotalPending']
            TotalPending  = groupObj['TotalPending']

            bpData = {
                "GroupName": GroupName,
                "GroupCode": GroupCode,
                "TotalSales": round(TotalPending, 2)
            }
            dataContext.append(bpData)
            totalSales = float(totalSales) + float(DocTotal)
            totalPayments = float(totalPayments) + float(PaidToDateSys)
            totalPendings = float(totalPendings) + float(TotalPending)


        TotalSales = totalSales
        TotalReceivePayment = round(totalPayments, 2)
        DifferenceAmount = round(float(totalPendings), 2)
        # DifferenceAmount = round(float(float(TotalSales) - float(allPayment)), 2)

        return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": TotalSales, "TotalReceivePayment": TotalReceivePayment, "DifferenceAmount": DifferenceAmount})
    
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>   
# bp list with total purchase
@api_view(['POST'])
def bp_ledger(request):
    try:
        print("bp_ledger",request.data)
        CardCode = request.data['CardCode']
        SalesType = request.data['Type'] # Gross/Net
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        
        dataContext = []
        docEntrys = []
        totalSales = 0
        totalSalesByBp = 0
        allPayment = 0

        if BusinessPartner.objects.filter(CardCode = CardCode).exists():
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            bpobj = BusinessPartner.objects.filter(CardCode = CardCode).first()
            PayTermsGrpCode = bpobj.PayTermsGrpCode
            CreditLimit = bpobj.CreditLimit
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            MobileNo = ""
            if BPEmployee.objects.filter(CardCode = CardCode, FirstName = bpobj.ContactPerson).exists():
                bpEmp = BPEmployee.objects.filter(CardCode = CardCode, FirstName = bpobj.ContactPerson).first()
                MobileNo = bpEmp.MobilePhone 
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            ptgcObj = PaymentTermsTypes.objects.filter(GroupNumber = PayTermsGrpCode).first()
            creditLimitDayes = ptgcObj.PaymentTermsGroupName
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            GSTIN = ""
            BPAddress = ""
            if BPBranch.objects.filter(BPCode = CardCode).exists():
                bpBranch = BPBranch.objects.filter(BPCode = CardCode).first()
                GSTIN = str(bpBranch.GSTIN)
                BPAddress = f"{bpBranch.Street} {bpBranch.City} {bpBranch.ZipCode}"
            GroupName = ""
            if BusinessPartnerGroups.objects.filter(Code = bpobj.GroupCode).exists():
                bpGroup = BusinessPartnerGroups.objects.filter(Code = bpobj.GroupCode).first()
                GroupName = bpGroup.Name

            BPData = [{
                "CardName": bpobj.CardName,
                "CardCode": bpobj.CardCode,
                "EmailAddress": bpobj.EmailAddress,
                "ContactPerson": bpobj.ContactPerson,
                "Phone1": MobileNo, #bpobj.Phone1,
                "GSTIN": GSTIN,
                "BPAddress": BPAddress,
                "GroupName": GroupName,
                "CreditLimit": CreditLimit,
                "CreditLimitDayes": creditLimitDayes,
            }]
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

            orderList = []
            if str(FromDate) != "":
                orderList = Invoice.objects.filter(CancelStatus="csNo", CardCode = CardCode, DocDate__gte = FromDate, DocDate__lte = ToDate).values("id","DocTotal", "CreateDate", "VatSum", "DocEntry", "DocumentStatus", "DocDate", "DiscountPercent", "PaidToDateSys", "DocNum").order_by('-DocDate')
            else:
                orderList = Invoice.objects.filter(CancelStatus="csNo", CardCode = CardCode).values("id","DocTotal", "CreateDate", "VatSum", "DocEntry", "DocumentStatus", "DocDate", "DiscountPercent", "PaidToDateSys", "DocNum").order_by('-DocDate')
            
            # print("Length of objects orderList: ", len(orderList))
            if len(orderList) != 0:
                for order in orderList:
                    allPaymentsList = []
                    docEntrys.append(order['DocEntry'])
                    DocTotal = order['DocTotal']
                    VatSum = order['VatSum']
                    #print(SalesType, DocTotal, VatSum)
                    DocumentStatus = order['DocumentStatus']
                    PaidToDateSys = order['PaidToDateSys']
                    if str(VatSum) == "":
                        #print("if vat empty:", VatSum)
                        VatSum = 0
                        
                    InvId = order['id']
                    DiscountPercent = float(order['DiscountPercent'])
                    if str(SalesType).lower() == "net":
                        BaseTotal = 0
                        itemObjs = DocumentLines.objects.filter(InvoiceID = InvId).values("id","LineTotal")
                        for itObjs in itemObjs:
                            LineTotal = float(itObjs['LineTotal'])
                            BaseTotal = BaseTotal + LineTotal
                        disAmt = 0
                        print('netAmt befour dicount',order['DocEntry'], BaseTotal)
                        if BaseTotal != 0:
                            if float(DiscountPercent) != 0.0:
                                disAmt = (BaseTotal * DiscountPercent) / 100
                        DocTotal = round(float(BaseTotal - disAmt), 2)
                        print('netAmt after dicount',order['DocEntry'], DocTotal)

                    if str(FromDate) != "":
                        allPaymentsList = IncomingPaymentInvoices.objects.filter(InvoiceDocEntry = order['DocEntry'], DocDate__gte = FromDate, DocDate__lte = ToDate).values_list('SumApplied', flat=True)
                    else:
                       allPaymentsList = IncomingPaymentInvoices.objects.filter(InvoiceDocEntry = order['DocEntry']).values_list('SumApplied', flat=True)
                    
                    for item in allPaymentsList:
                        allPayment += float(item)

                    PaymentStatus = "Unpaid"                    
                    if DocumentStatus == "bost_Close":
                        PaymentStatus = "Paid"
                    # elif len(allPaymentsList) != 0:
                    elif float(PaidToDateSys) > 0:
                        PaymentStatus = "Partially Paid"
                    else:
                        PaymentStatus = "Unpaid"
                        
                    bpData = {
                        "OrderId": order['DocEntry'],
                        "DocEntry": order['DocNum'],
                        "OrderAmount": DocTotal,
                        "CreateDate": order['DocDate'],
                        "PaymentStatus": PaymentStatus
                    }                    
                    dataContext.append(bpData)
                    totalSalesByBp = totalSalesByBp + float(DocTotal)
            else:
                pass
                #print('no invoice')
        else:
            return Response({"message": "Invalid CardCode","status": 201, "data":[], "TotalSales": 0})
        
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        fromToDate = ""
        if str(FromDate) != "":
            fromToDate = f"AND inv.DocDate >= '{FromDate}' AND inv.DocDate <= '{ToDate}'"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        TotalCreditNote = 0
        allCreditNote = 0
        bpCreditNote = 0
        sqlAllCreditNote = f"""
        SELECT
            bp.CardCode as CardCode,
            bp.CardName as CardName, 
            IFNULL(SUM(A.DocTotal), 0) AS 'DocTotal',
            IFNULL(SUM(A.NetTotal), 0) AS 'NetTotal',
            IFNULL(SUM(A.PaidToDateSys), 0) AS `PaidToDateSys`,
            IFNULL(SUM(A.DocTotal - A.PaidToDateSys), 0) AS `PendingTotal`
        FROM BusinessPartner_businesspartner bp
        LEFT JOIN BusinessPartner_businesspartnergroups bpgroup ON bpgroup.Code = bp.GroupCode
        INNER JOIN (
            SELECT
                inv.CardCode,
                inv.id,
                inv.DocTotal,
                inv.PaidToDateSys,
                IFNULL(SUM(INVLine.LineTotal), 0) AS LineTotal,
                IFNULL(
                    SUM(CASE
                        WHEN inv.DiscountPercent != 0.0 THEN INVLine.LineTotal - (INVLine.LineTotal * inv.DiscountPercent / 100)
                        ELSE INVLine.LineTotal
                    END), 0
                ) AS NetTotal
            FROM Invoice_creditnotes inv
            LEFT JOIN Invoice_creditnotesdocumentlines INVLine ON INVLine.CreditNotesId = inv.id
            WHERE 
                inv.CancelStatus = 'csNo'
                {fromToDate}
            GROUP BY inv.CardCode, inv.id
        ) A ON bp.CardCode = A.CardCode
        WHERE
            bp.CardCode = '{CardCode}';
        """
        print(sqlAllCreditNote)
        mycursor.execute(sqlAllCreditNote)
        allCreditNoteData = mycursor.fetchall()        
        if len(allCreditNoteData) > 0:
            allCreditNote = allCreditNoteData[0]['NetTotal']
            if str(SalesType).lower() == "gross":
                allCreditNote = allCreditNoteData[0]['DocTotal']

        TotalSales = round(totalSalesByBp, 2)
        TotalReceivePayment = round(allPayment, 2)
        DifferenceAmount = round(float(float(totalSalesByBp) - float(allPayment)), 2)
        TotalCreditNote = round(allCreditNote, 2)

        if 'PageNo' in request.data:
            PageNo = int(request.data['PageNo'])
            MaxSize = request.data['MaxSize']
            if MaxSize != "All":
                size = int(MaxSize)
                endWith = (PageNo * size)
                startWith = (endWith - size)
                dataContext = dataContext[startWith:endWith]

        return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": TotalSales, "TotalReceivePayment": TotalReceivePayment, "DifferenceAmount": DifferenceAmount, "BPData": BPData, "TotalCreditNote": TotalCreditNote})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# bp list with total purchase
@api_view(['POST'])
def bp_purchase_invoices(request):
    try:
        CardCode    = request.data['CardCode']
        SalesType   = request.data['Type'] # Gross/Net
        FromDate    = request.data['FromDate']
        ToDate      = request.data['ToDate']
        
        dataContext = []
        docEntrys   = []
        allPayment  = 0
        totalSalesByBp = 0

        if BusinessPartner.objects.filter(CardCode = CardCode).exists():
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            bpobj = BusinessPartner.objects.filter(CardCode = CardCode).first()
            LinkedBusinessPartner = bpobj.LinkedBusinessPartner
            PayTermsGrpCode = bpobj.PayTermsGrpCode
            CreditLimit = bpobj.CreditLimit
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            MobileNo = ""
            if BPEmployee.objects.filter(CardCode = CardCode, FirstName = bpobj.ContactPerson).exists():
                bpEmp = BPEmployee.objects.filter(CardCode = CardCode, FirstName = bpobj.ContactPerson).first()
                MobileNo = bpEmp.MobilePhone 
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            ptgcObj = PaymentTermsTypes.objects.filter(GroupNumber = PayTermsGrpCode).first()
            creditLimitDayes = ptgcObj.PaymentTermsGroupName

            GSTIN = ""
            BPAddress = ""
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            if BPBranch.objects.filter(BPCode = CardCode).exists():
                bpBranch = BPBranch.objects.filter(BPCode = CardCode).first()
                GSTIN = str(bpBranch.GSTIN)
                BPAddress = f"{bpBranch.Street} {bpBranch.City} {bpBranch.ZipCode}"
            GroupName = ""
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            if BusinessPartnerGroups.objects.filter(Code = bpobj.GroupCode).exists():
                bpGroup = BusinessPartnerGroups.objects.filter(Code = bpobj.GroupCode).first()
                GroupName = bpGroup.Name

            BPData = [{
                "CardName": bpobj.CardName,
                "CardCode": bpobj.CardCode,
                "EmailAddress": bpobj.EmailAddress,
                "ContactPerson": bpobj.ContactPerson,
                "Phone1": MobileNo, #bpobj.Phone1,
                "GSTIN": GSTIN,
                "BPAddress": BPAddress,
                "GroupName": GroupName,
                "CreditLimit": CreditLimit,
                "CreditLimitDayes": creditLimitDayes,
            }]
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

            apInvoicesList = []
            if str(FromDate) != "":
                apInvoicesList = PurchaseInvoices.objects.filter(CancelStatus="csNo", CardCode = LinkedBusinessPartner, DocDate__gte = FromDate, DocDate__lte = ToDate).values("id","DocTotal", "CreateDate", "VatSum", "DocEntry", "DocumentStatus", "DocDate", "DiscountPercent").order_by('-DocDate')
            else:
                apInvoicesList = PurchaseInvoices.objects.filter(CancelStatus="csNo", CardCode = LinkedBusinessPartner).values("id","DocTotal", "CreateDate", "VatSum", "DocEntry", "DocumentStatus", "DocDate", "DiscountPercent").order_by('-DocDate')

            #print("Length of objects apInvoicesList: ", len(apInvoicesList))
            if len(apInvoicesList) != 0:
                for order in apInvoicesList:
                    allPaymentsList = []
                    docEntrys.append(order['DocEntry'])
                    DocTotal = order['DocTotal']
                    VatSum = order['VatSum']
                    DocumentStatus = order['DocumentStatus']
                    x = "Unpaid"                    
                    if str(VatSum) == "":
                        VatSum = 0

                    InvId = order['id']
                    DiscountPercent = float(order['DiscountPercent'])
                    if str(SalesType).lower() == "net":
                        BaseTotal = 0
                        itemObjs = DocumentLines.objects.filter(InvoiceID = InvId).values("id","LineTotal")
                        for itObjs in itemObjs:
                            LineTotal = float(itObjs['LineTotal'])
                            BaseTotal = BaseTotal + LineTotal
                        disAmt = 0
                        print('netAmt befour dicount',order['DocEntry'], BaseTotal)
                        if BaseTotal != 0:
                            if float(DiscountPercent) != 0.0:
                                disAmt = (BaseTotal * DiscountPercent) / 100
                        DocTotal = round(float(BaseTotal - disAmt), 2)
                        print('netAmt after dicount',order['DocEntry'], DocTotal)

                    if str(FromDate) != "":
                        allPaymentsList = VendorPaymentsInvoices.objects.filter(InvoiceDocEntry = order['DocEntry'], DocDate__gte = FromDate, DocDate__lte = ToDate).values_list('SumApplied', flat=True)
                    else:
                       allPaymentsList = VendorPaymentsInvoices.objects.filter(InvoiceDocEntry = order['DocEntry']).values_list('SumApplied', flat=True)
                    
                    for item in allPaymentsList:
                        allPayment += float(item)

                    if DocumentStatus == "bost_Close":
                        PaymentStatus = "Paid"
                    elif len(allPaymentsList) != 0:
                        PaymentStatus = "Partially Paid"
                    else:
                        PaymentStatus = "Unpaid"
                        
                    bpData = {
                        "OrderId": order['id'],
                        "DocEntry": order['DocEntry'],
                        "OrderAmount": order['DocTotal'],
                        "CreateDate": order['DocDate'],
                        "PaymentStatus": PaymentStatus
                    }                    
                    dataContext.append(bpData)
                    totalSalesByBp = totalSalesByBp + float(DocTotal)
                # end 
        else:
            return Response({"message": "Invalid CardCode","status": 201, "data":[], "TotalSales": 0})

        allCreditNoteList = []
        if str(FromDate) != "":
            allCreditNoteList = PurchaseCreditNotes.objects.filter(CancelStatus="csNo",CardCode = LinkedBusinessPartner, DocDate__gte = FromDate, DocDate__lte = ToDate).values_list('DocTotal', flat=True)
        else:
            allCreditNoteList = PurchaseCreditNotes.objects.filter(CancelStatus="csNo",CardCode = LinkedBusinessPartner).values_list('DocTotal', flat=True)
        
        allCreditNote = 0
        for item2 in allCreditNoteList:
            allCreditNote += float(item2)

        TotalSales = round(totalSalesByBp, 2)
        TotalReceivePayment = round(allPayment, 2)
        DifferenceAmount = round(float(float(totalSalesByBp) - float(allPayment)), 2)
        TotalCreditNote = round(allCreditNote, 2)

        if 'PageNo' in request.data:
            PageNo = int(request.data['PageNo'])
            MaxSize = request.data['MaxSize']
            if MaxSize != "All":
                size = int(MaxSize)
                endWith = (PageNo * size)
                startWith = (endWith - size)
                dataContext = dataContext[startWith:endWith]

        return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": TotalSales, "TotalReceivePayment": TotalReceivePayment, "DifferenceAmount": DifferenceAmount, "BPData": BPData, "TotalCreditNote": TotalCreditNote})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

# bp list with total purchase
@api_view(['POST'])
def bp_receivable(request):
    try:
        CardCode    = request.data['CardCode']
        SalesType   = request.data['Type'] # Gross/Net
        FromDate    = request.data['FromDate']
        ToDate      = request.data['ToDate']
        
        dataContext = []
        totalPendingsByBp = 0
        allCreditNote = 0
        allbpJELine = 0
        dataList = []
        dataListTotal = 0

        OrderByName = "" #a-z/z-a
        OrderByAmt = "" #desc
        if 'OrderByName' in request.data:
            OrderByName = str(request.data['OrderByName']).strip()
        if 'OrderByAmt' in request.data:
            OrderByAmt = str(request.data['OrderByAmt']).strip()
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        orderby = ""
        if str(OrderByName).lower() == 'a-z':
            orderby = "Order By CardName asc"
        elif str(OrderByName).lower() == 'z-a':
            orderby = "Order By CardName desc"
        elif str(OrderByAmt).lower() == 'asc':
            orderby = "Order By TotalDue asc"
        elif str(OrderByAmt).lower() == 'desc':
            orderby = "Order By TotalDue desc"
        else:
            orderby = "Order By DocDate asc"

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        DueDaysGroup = ''
        if 'DueDaysGroup' in request.data:
            DueDaysGroup = request.data['DueDaysGroup']
        # endif
        overDuesQuery = ""
        if DueDaysGroup != "":
            overDuesQuery = f"AND DueDaysGroup = '{DueDaysGroup}'"
    
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        
        # for one bp Receipt and Pending
        if BusinessPartner.objects.filter(CardCode = CardCode).exists():
            # # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            bpobj = BusinessPartner.objects.filter(CardCode = CardCode).first()

            sqlSelectReceiable = f"""
                SELECT * FROM `BusinessPartner_receivable`
                WHERE
                    CardCode = '{CardCode}'
                    AND `CronUpdateCount` = (SELECT MAX(`CronUpdateCount`) FROM BusinessPartner_receivable) - 1
                    {overDuesQuery}
                {orderby}
            """
            # {limitQuery};

            ContactPerson    = ""
            EmailAddress     = ""
            MobileNo         = ""
            GSTIN            = ""
            BPAddress        = ""
            CreditLimit      = ""
            CreditLimitDayes = ""
            GroupName        = ""
                
            print(sqlSelectReceiable)
            mycursor.execute(sqlSelectReceiable)
            orderList = mycursor.fetchall()      
            if len(orderList) != 0:
                for order in orderList:
                    DocEntry      = order['DocEntry']
                    DocNum        = order['DocNum']
                    TransId       = order['TransId']
                    TransType     = order['TransType']
                    PendingTotal  = round(float(order['TotalDue']), 2)
                    DueDaysGroup  = order['DueDaysGroup']
                    DocDate       = order['DocDate']
                    DocDueDate    = order['DueDate']

                    ContactPerson = order['ContactPerson']
                    EmailAddress  = order['EmailAddress']
                    MobileNo      = order['MobileNo']
                    GSTIN         = order['GSTIN']
                    BPAddress     = order['BPAddresses']
                    CreditLimit   = order['CreditLimit']
                    CreditLimitDayes = order['CreditLimitDayes']
                    GroupName     = order['GroupName']

                    OverDueDays     = order['OverDueDays']
                    
                    PaymentStatus = "Unpaid"

                    print("DocEntry", DocEntry, "TransType", TransType)
                    if str(TransType) == 'Invoice':
                        
                        PaymentStatus = "Unpaid"                        
                        bpData = {
                            "OrderId": DocEntry,
                            "DocEntry": DocNum,
                            "DocDueDate": DocDueDate,
                            "OrderAmount": 0,
                            "OverDueDays": OverDueDays,
                            "CreateDate": DocDate,
                            "PaymentStatus": PaymentStatus,
                            "TotalReceivePayment": 0,
                            "DifferenceAmount":round(float(PendingTotal), 2)
                        }                    
                        dataContext.append(bpData)
                        totalPendingsByBp = totalPendingsByBp + float(PendingTotal)

                    elif str(TransType) == 'JE':
                        tempData = {
                            'id': DocEntry,
                            'DocNum': DocNum,
                            'DocTotal': PendingTotal,
                            'DocDate': DocDate,
                            'DocType': "ttJournalEntry"
                        }
                        dataList.append(tempData)
                        dataListTotal = dataListTotal + PendingTotal
                    elif str(TransType) == 'A/R Credit Memo':
                        tempData = {
                            'id': DocEntry,
                            'DocNum': DocNum,
                            'DocTotal': (PendingTotal),
                            'DocDate': DocDate,
                            'DocType': "ttARCredItnote"
                        }
                        dataList.append(tempData)
                        dataListTotal = dataListTotal + PendingTotal
                    elif str(TransType) == 'Incoming':
                        tempData = {
                            'id': DocEntry,
                            'DocNum': DocNum,
                            'DocTotal': PendingTotal,
                            'DocDate': DocDate,
                            'DocType': "ttReceipt"
                        }
                        dataList.append(tempData)
                        dataListTotal = dataListTotal + PendingTotal
                    elif str(TransType) == 'outgoing':
                        
                        tempData = {
                            'id': DocEntry,
                            'DocNum': DocNum,
                            'DocTotal': PendingTotal,
                            'DocDate': DocDate,
                            'DocType': "ttVendorPayment"
                        }
                        dataList.append(tempData)
                        dataListTotal = dataListTotal + PendingTotal
                    else:
                        print('no match found')
                    # endelif
                # end for
            # endif

            AvgPayDays = 0

            BPData = [{
                "CardName": bpobj.CardName,
                "CardCode": bpobj.CardCode,
                "EmailAddress": EmailAddress,
                "ContactPerson": ContactPerson,
                "Phone1": MobileNo, 
                "GSTIN": GSTIN,
                "BPAddress": BPAddress,
                "GroupName": GroupName,
                "CreditLimit": CreditLimit,
                "CreditLimitDayes": CreditLimitDayes,
                "AvgPayDays": AvgPayDays
            }]
        else:
            return Response({"message": "Invalid CardCode","status": 201, "data":[], "TotalSales": 0})

        TotalSales = 0
        TotalReceivePayment = 0
        DifferenceAmount = round(float(totalPendingsByBp), 2)

        print("TotalSales", TotalSales, "allCreditNote", allCreditNote, "allbpJELine", allbpJELine)
        if 'PageNo' in request.data:
            PageNo = int(request.data['PageNo'])
            MaxSize = request.data['MaxSize']
            if MaxSize != "All":
                size = int(MaxSize)
                endWith = (PageNo * size)
                startWith = (endWith - size)
                dataContext = dataContext[startWith:endWith]

        return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": TotalSales, "TotalReceivePayment": TotalReceivePayment, "DifferenceAmount": DifferenceAmount, "BPData": BPData, "DataListTotal": dataListTotal, "DataList": dataList})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# bp list with total purchase
@api_view(['POST'])
def bp_payable(request):
    try:
        CardCode = request.data['CardCode']
        SalesType = request.data['Type'] # Gross/Net
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        
        dataContext = []
        totalPendingsByBp = 0
        allCreditNote = 0
        allbpJELine = 0
        BPData = []
        dataList = []
        dataListTotal = 0

        OrderByName = "" #a-z/z-a
        OrderByAmt = "" #desc
        if 'OrderByName' in request.data:
            OrderByName = str(request.data['OrderByName']).strip()
        if 'OrderByAmt' in request.data:
            OrderByAmt = str(request.data['OrderByAmt']).strip()
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        orderby = ""
        if str(OrderByName).lower() == 'a-z':
            orderby = "Order By CardName asc"
        elif str(OrderByName).lower() == 'z-a':
            orderby = "Order By CardName desc"
        elif str(OrderByAmt).lower() == 'asc':
            orderby = "Order By TotalDue asc"
        elif str(OrderByAmt).lower() == 'desc':
            orderby = "Order By TotalDue desc"
        else:
            orderby = "Order By DocDate asc"

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        DueDaysGroup = ''
        if 'DueDaysGroup' in request.data:
            DueDaysGroup = request.data['DueDaysGroup']
        # endif
        overDuesQuery = ""
        if DueDaysGroup != "":
            overDuesQuery = f"AND DueDaysGroup = '{DueDaysGroup}'"
    
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        
        # for one bp Receipt and Pending
        if BusinessPartner.objects.filter(CardCode = CardCode).exists():
            # # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            bpobj = BusinessPartner.objects.filter(CardCode = CardCode).first()

            sqlSelectPayable = f"""
                SELECT * FROM `BusinessPartner_payable`
                WHERE
                    CardCode = '{CardCode}'
                    AND `CronUpdateCount` = (SELECT MAX(`CronUpdateCount`) FROM BusinessPartner_payable) - 1
                    {overDuesQuery}
                {orderby}
            """
            # {limitQuery};

            ContactPerson    = ""
            EmailAddress     = ""
            MobileNo         = ""
            GSTIN            = ""
            BPAddress        = ""
            CreditLimit      = ""
            CreditLimitDayes = ""
            GroupName        = ""
                
            print(sqlSelectPayable)
            mycursor.execute(sqlSelectPayable)
            orderList = mycursor.fetchall()      
            if len(orderList) != 0:
                for order in orderList:
                    DocEntry      = order['DocEntry']
                    DocNum        = order['DocNum']
                    TransId       = order['TransId']
                    TransType     = order['TransType']
                    PendingTotal  = round(float(order['TotalDue']), 2)
                    DueDaysGroup  = order['DueDaysGroup']
                    DocDate       = order['DocDate']
                    DocDueDate    = order['DueDate']

                    ContactPerson = order['ContactPerson']
                    EmailAddress  = order['EmailAddress']
                    MobileNo      = order['MobileNo']
                    GSTIN         = order['GSTIN']
                    BPAddress     = order['BPAddresses']
                    CreditLimit   = order['CreditLimit']
                    CreditLimitDayes = order['CreditLimitDayes']
                    GroupName     = order['GroupName']

                    OverDueDays     = order['OverDueDays']
                    
                    PaymentStatus = "Unpaid"

                    print("DocEntry", DocEntry, "TransType", TransType)
                    if str(TransType) == 'Invoice':
                        
                        PaymentStatus = "Unpaid"                        
                        bpData = {
                            "OrderId": DocEntry,
                            "DocEntry": DocNum,
                            "DocDueDate": DocDueDate,
                            "OrderAmount": 0,
                            "OverDueDays": OverDueDays,
                            "CreateDate": DocDate,
                            "PaymentStatus": PaymentStatus,
                            "TotalReceivePayment": 0,
                            "DifferenceAmount":round(float(PendingTotal), 2)
                        }                    
                        dataContext.append(bpData)
                        totalPendingsByBp = totalPendingsByBp + float(PendingTotal)

                    elif str(TransType) == 'JE':
                        tempData = {
                            'id': DocEntry,
                            'DocNum': DocNum,
                            'DocTotal': PendingTotal,
                            'DocDate': DocDate,
                            'DocType': "ttJournalEntry"
                        }
                        dataList.append(tempData)
                        dataListTotal = dataListTotal + PendingTotal
                    elif str(TransType) == 'A/R Credit Memo':
                        tempData = {
                            'id': DocEntry,
                            'DocNum': DocNum,
                            'DocTotal': (PendingTotal),
                            'DocDate': DocDate,
                            'DocType': "ttARCredItnote"
                        }
                        dataList.append(tempData)
                        dataListTotal = dataListTotal + PendingTotal
                    elif str(TransType) == 'Incoming':
                        tempData = {
                            'id': DocEntry,
                            'DocNum': DocNum,
                            'DocTotal': PendingTotal,
                            'DocDate': DocDate,
                            'DocType': "ttReceipt"
                        }
                        dataList.append(tempData)
                        dataListTotal = dataListTotal + PendingTotal
                    elif str(TransType) == 'outgoing':
                        
                        tempData = {
                            'id': DocEntry,
                            'DocNum': DocNum,
                            'DocTotal': PendingTotal,
                            'DocDate': DocDate,
                            'DocType': "ttVendorPayment"
                        }
                        dataList.append(tempData)
                        dataListTotal = dataListTotal + PendingTotal
                    else:
                        print('no match found')
                    # endelif
                # end for
            # endif

            AvgPayDays = 0

            BPData = [{
                "CardName": bpobj.CardName,
                "CardCode": bpobj.CardCode,
                "EmailAddress": EmailAddress,
                "ContactPerson": ContactPerson,
                "Phone1": MobileNo, 
                "GSTIN": GSTIN,
                "BPAddress": BPAddress,
                "GroupName": GroupName,
                "CreditLimit": CreditLimit,
                "CreditLimitDayes": CreditLimitDayes,
                "AvgPayDays": AvgPayDays
            }]
        else:
            return Response({"message": "Invalid CardCode","status": 201, "data":[], "TotalSales": 0})

        TotalSales = 0
        TotalReceivePayment = 0
        DifferenceAmount = round(float(totalPendingsByBp), 2)

        print("TotalSales", TotalSales, "allCreditNote", allCreditNote, "allbpJELine", allbpJELine)
        if 'PageNo' in request.data:
            PageNo = int(request.data['PageNo'])
            MaxSize = request.data['MaxSize']
            if MaxSize != "All":
                size = int(MaxSize)
                endWith = (PageNo * size)
                startWith = (endWith - size)
                dataContext = dataContext[startWith:endWith]

        return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": TotalSales, "TotalReceivePayment": TotalReceivePayment, "DifferenceAmount": DifferenceAmount, "BPData": BPData, "DataListTotal": dataListTotal, "DataList": dataList})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# bp list with total purchase
@api_view(['POST'])
def bp_due_payment(request):
    try:
        CardCode = request.data['CardCode']
        OrderByName  = str(request.data['OrderByName']).strip()
        OrderByAmt   = str(request.data['OrderByAmt']).strip()
        DueDaysGroup = request.data['DueDaysGroup']
        PageNo       = request.data['PageNo']
        MaxSize      = request.data['MaxSize']
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        dueDaysGroupQuery = "AND `DueDate` >= CURDATE()"
        if str(DueDaysGroup) == '-1': # overdue invoices
            dueDaysGroupQuery = "AND `DueDate` < CURDATE()"
        elif DueDaysGroup != "": # due date in next DueDaysGroup
            dueDaysGroupQuery = f"AND `DueDate` >= CURDATE() AND `DueDate` <= DATE_ADD(CURDATE(), INTERVAL {DueDaysGroup} DAY)"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        dataContext = []
        totalPendingsByBp = 0
        dataList = []
        dataListTotal = 0
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        orderby = ""
        if str(OrderByName).lower() == 'a-z':
            orderby = "Order By CardName asc"
        elif str(OrderByName).lower() == 'z-a':
            orderby = "Order By CardName desc"
        elif str(OrderByAmt).lower() == 'asc':
            orderby = "Order By TotalDue asc"
        elif str(OrderByAmt).lower() == 'desc':
            orderby = "Order By TotalDue desc"
        else:
            orderby = "Order By DocDate asc"    
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        
        # for one bp Receipt and Pending
        if BusinessPartner.objects.filter(CardCode = CardCode).exists():
            # # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            bpobj = BusinessPartner.objects.filter(CardCode = CardCode).first()

            sqlSelectReceiable = f"""
                SELECT *, `TotalDue` as TotalPending FROM `BusinessPartner_receivable`
                WHERE
                    CardCode = '{CardCode}' AND
                    `CronUpdateCount` = (SELECT MAX(`CronUpdateCount`) FROM BusinessPartner_receivable) - 1 
                    {dueDaysGroupQuery}
                {orderby}
            """
            ContactPerson    = ""
            EmailAddress     = ""
            MobileNo         = ""
            GSTIN            = ""
            BPAddress        = ""
            CreditLimit      = ""
            CreditLimitDayes = ""
            GroupName        = ""
                
            print(sqlSelectReceiable)
            mycursor.execute(sqlSelectReceiable)
            orderList = mycursor.fetchall()      
            if len(orderList) != 0:
                for order in orderList:
                    DocEntry      = order['DocEntry']
                    DocNum        = order['DocNum']
                    TransId       = order['TransId']
                    TransType     = order['TransType']
                    PendingTotal  = round(float(order['TotalDue']), 2)
                    DueDaysGroup  = order['DueDaysGroup']
                    DocDate       = order['DocDate']
                    DocDueDate    = order['DueDate']

                    ContactPerson = order['ContactPerson']
                    EmailAddress  = order['EmailAddress']
                    MobileNo      = order['MobileNo']
                    GSTIN         = order['GSTIN']
                    BPAddress     = order['BPAddresses']
                    CreditLimit   = order['CreditLimit']
                    CreditLimitDayes = order['CreditLimitDayes']
                    GroupName     = order['GroupName']

                    OverDueDays     = order['OverDueDays']
                    
                    PaymentStatus = "Unpaid"

                    print("DocEntry", DocEntry, "TransType", TransType)
                    if str(TransType) == 'Invoice':
                        
                        PaymentStatus = "Unpaid"                        
                        bpData = {
                            "OrderId": DocEntry,
                            "DocEntry": DocNum,
                            "DocDueDate": DocDueDate,
                            "OrderAmount": 0,
                            "OverDueDays": OverDueDays,
                            "CreateDate": DocDate,
                            "PaymentStatus": PaymentStatus,
                            "TotalReceivePayment": 0,
                            "DifferenceAmount":round(float(PendingTotal), 2)
                        }                    
                        dataContext.append(bpData)
                        totalPendingsByBp = totalPendingsByBp + float(PendingTotal)

                    elif str(TransType) == 'JE':
                        tempData = {
                            'id': DocEntry,
                            'DocNum': DocNum,
                            'DocTotal': PendingTotal,
                            'DocDate': DocDate,
                            'DocType': "ttJournalEntry"
                        }
                        dataList.append(tempData)
                        dataListTotal = dataListTotal + PendingTotal
                    elif str(TransType) == 'A/R Credit Memo':
                        tempData = {
                            'id': DocEntry,
                            'DocNum': DocNum,
                            'DocTotal': (PendingTotal),
                            'DocDate': DocDate,
                            'DocType': "ttARCredItnote"
                        }
                        dataList.append(tempData)
                        dataListTotal = dataListTotal + PendingTotal
                    elif str(TransType) == 'Incoming':
                        tempData = {
                            'id': DocEntry,
                            'DocNum': DocNum,
                            'DocTotal': PendingTotal,
                            'DocDate': DocDate,
                            'DocType': "ttReceipt"
                        }
                        dataList.append(tempData)
                        dataListTotal = dataListTotal + PendingTotal
                    elif str(TransType) == 'outgoing':
                        
                        tempData = {
                            'id': DocEntry,
                            'DocNum': DocNum,
                            'DocTotal': PendingTotal,
                            'DocDate': DocDate,
                            'DocType': "ttVendorPayment"
                        }
                        dataList.append(tempData)
                        dataListTotal = dataListTotal + PendingTotal
                    else:
                        print('no match found')
                    # endelif
                # end for
            # endif

            AvgPayDays = 0

            BPData = [{
                "CardName": bpobj.CardName,
                "CardCode": bpobj.CardCode,
                "EmailAddress": EmailAddress,
                "ContactPerson": ContactPerson,
                "Phone1": MobileNo, 
                "GSTIN": GSTIN,
                "BPAddress": BPAddress,
                "GroupName": GroupName,
                "CreditLimit": CreditLimit,
                "CreditLimitDayes": CreditLimitDayes,
                "AvgPayDays": AvgPayDays
            }]
        else:
            return Response({"message": "Invalid CardCode","status": 201, "data":[], "TotalSales": 0})

        TotalSales = 0
        TotalReceivePayment = 0
        DifferenceAmount = round(float(totalPendingsByBp), 2)

        if 'PageNo' in request.data:
            PageNo = int(request.data['PageNo'])
            MaxSize = request.data['MaxSize']
            if MaxSize != "All":
                size = int(MaxSize)
                endWith = (PageNo * size)
                startWith = (endWith - size)
                dataContext = dataContext[startWith:endWith]

        return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": TotalSales, "TotalReceivePayment": TotalReceivePayment, "DifferenceAmount": DifferenceAmount, "BPData": BPData, "DataListTotal": dataListTotal, "DataList": dataList})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# bp list with total purchase
@api_view(['POST'])
def bp_payable_due_payment(request):
    try:
        CardCode = request.data['CardCode']
        OrderByName  = str(request.data['OrderByName']).strip()
        OrderByAmt   = str(request.data['OrderByAmt']).strip()
        DueDaysGroup = request.data['DueDaysGroup']
        PageNo       = request.data['PageNo']
        MaxSize      = request.data['MaxSize']
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        dueDaysGroupQuery = "AND `DueDate` >= CURDATE()"
        if str(DueDaysGroup) == '-1': # overdue invoices
            dueDaysGroupQuery = "AND `DueDate` < CURDATE()"
        elif DueDaysGroup != "": # due date in next DueDaysGroup
            dueDaysGroupQuery = f"AND `DueDate` >= CURDATE() AND `DueDate` <= DATE_ADD(CURDATE(), INTERVAL {DueDaysGroup} DAY)"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        dataContext = []
        totalPendingsByBp = 0
        dataList = []
        dataListTotal = 0
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        orderby = ""
        if str(OrderByName).lower() == 'a-z':
            orderby = "Order By CardName asc"
        elif str(OrderByName).lower() == 'z-a':
            orderby = "Order By CardName desc"
        elif str(OrderByAmt).lower() == 'asc':
            orderby = "Order By TotalDue asc"
        elif str(OrderByAmt).lower() == 'desc':
            orderby = "Order By TotalDue desc"
        else:
            orderby = "Order By DocDate asc"    
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        
        # for one bp Receipt and Pending
        if BusinessPartner.objects.filter(CardCode = CardCode).exists():
            # # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            bpobj = BusinessPartner.objects.filter(CardCode = CardCode).first()

            sqlSelectReceiable = f"""
                SELECT *, `TotalDue` as TotalPending FROM `BusinessPartner_payable`
                WHERE
                    CardCode = '{CardCode}' AND
                    `CronUpdateCount` = (SELECT MAX(`CronUpdateCount`) FROM BusinessPartner_payable) - 1 
                    {dueDaysGroupQuery}
                {orderby}
            """
            ContactPerson    = ""
            EmailAddress     = ""
            MobileNo         = ""
            GSTIN            = ""
            BPAddress        = ""
            CreditLimit      = ""
            CreditLimitDayes = ""
            GroupName        = ""
                
            print(sqlSelectReceiable)
            mycursor.execute(sqlSelectReceiable)
            orderList = mycursor.fetchall()      
            if len(orderList) != 0:
                for order in orderList:
                    DocEntry      = order['DocEntry']
                    DocNum        = order['DocNum']
                    TransId       = order['TransId']
                    TransType     = order['TransType']
                    PendingTotal  = round(float(order['TotalDue']), 2)
                    DueDaysGroup  = order['DueDaysGroup']
                    DocDate       = order['DocDate']
                    DocDueDate    = order['DueDate']

                    ContactPerson = order['ContactPerson']
                    EmailAddress  = order['EmailAddress']
                    MobileNo      = order['MobileNo']
                    GSTIN         = order['GSTIN']
                    BPAddress     = order['BPAddresses']
                    CreditLimit   = order['CreditLimit']
                    CreditLimitDayes = order['CreditLimitDayes']
                    GroupName     = order['GroupName']

                    OverDueDays     = order['OverDueDays']
                    
                    PaymentStatus = "Unpaid"

                    print("DocEntry", DocEntry, "TransType", TransType)
                    if str(TransType) == 'Invoice':
                        
                        PaymentStatus = "Unpaid"                        
                        bpData = {
                            "OrderId": DocEntry,
                            "DocEntry": DocNum,
                            "DocDueDate": DocDueDate,
                            "OrderAmount": 0,
                            "OverDueDays": OverDueDays,
                            "CreateDate": DocDate,
                            "PaymentStatus": PaymentStatus,
                            "TotalReceivePayment": 0,
                            "DifferenceAmount":round(float(PendingTotal), 2)
                        }                    
                        dataContext.append(bpData)
                        totalPendingsByBp = totalPendingsByBp + float(PendingTotal)

                    elif str(TransType) == 'JE':
                        tempData = {
                            'id': DocEntry,
                            'DocNum': DocNum,
                            'DocTotal': PendingTotal,
                            'DocDate': DocDate,
                            'DocType': "ttJournalEntry"
                        }
                        dataList.append(tempData)
                        dataListTotal = dataListTotal + PendingTotal
                    elif str(TransType) == 'A/R Credit Memo':
                        tempData = {
                            'id': DocEntry,
                            'DocNum': DocNum,
                            'DocTotal': (PendingTotal),
                            'DocDate': DocDate,
                            'DocType': "ttARCredItnote"
                        }
                        dataList.append(tempData)
                        dataListTotal = dataListTotal + PendingTotal
                    elif str(TransType) == 'Incoming':
                        tempData = {
                            'id': DocEntry,
                            'DocNum': DocNum,
                            'DocTotal': PendingTotal,
                            'DocDate': DocDate,
                            'DocType': "ttReceipt"
                        }
                        dataList.append(tempData)
                        dataListTotal = dataListTotal + PendingTotal
                    elif str(TransType) == 'outgoing':
                        
                        tempData = {
                            'id': DocEntry,
                            'DocNum': DocNum,
                            'DocTotal': PendingTotal,
                            'DocDate': DocDate,
                            'DocType': "ttVendorPayment"
                        }
                        dataList.append(tempData)
                        dataListTotal = dataListTotal + PendingTotal
                    else:
                        tempData = {
                            'id': DocEntry,
                            'DocNum': DocNum,
                            'DocTotal': PendingTotal,
                            'DocDate': DocDate,
                            'DocType': TransType
                        }
                        dataList.append(tempData)
                        dataListTotal = dataListTotal + PendingTotal
                        print('no match found')
                    # endelif
                # end for
            # endif

            AvgPayDays = 0

            BPData = [{
                "CardName": bpobj.CardName,
                "CardCode": bpobj.CardCode,
                "EmailAddress": EmailAddress,
                "ContactPerson": ContactPerson,
                "Phone1": MobileNo, 
                "GSTIN": GSTIN,
                "BPAddress": BPAddress,
                "GroupName": GroupName,
                "CreditLimit": CreditLimit,
                "CreditLimitDayes": CreditLimitDayes,
                "AvgPayDays": AvgPayDays
            }]
        else:
            return Response({"message": "Invalid CardCode","status": 201, "data":[], "TotalSales": 0})

        TotalSales = 0
        TotalReceivePayment = 0
        DifferenceAmount = round(float(totalPendingsByBp), 2)

        if 'PageNo' in request.data:
            PageNo = int(request.data['PageNo'])
            MaxSize = request.data['MaxSize']
            if MaxSize != "All":
                size = int(MaxSize)
                endWith = (PageNo * size)
                startWith = (endWith - size)
                dataContext = dataContext[startWith:endWith]

        return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": TotalSales, "TotalReceivePayment": TotalReceivePayment, "DifferenceAmount": DifferenceAmount, "BPData": BPData, "DataListTotal": dataListTotal, "DataList": dataList})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# bp list with total payment receipt
@api_view(['POST'])
def receipt_dashboard(request):
    try:
        Filter = request.data['Filter']
        Code = request.data['Code']
        SalesType = request.data['Type']
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SalesPersonCode = -1
        if 'SalesPersonCode' in request.data:
            SalesPersonCode = request.data['SalesPersonCode']
        zones = getZoneByEmployee(SalesPersonCode)
        zonesStr = "','".join(zones)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SearchText = ""
        if 'SearchText' in request.data:
            SearchText = request.data['SearchText']
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        OrderByName = "" #a-z/z-a
        OrderByAmt = "" #desc
        if 'OrderByName' in request.data:
            OrderByName = str(request.data['OrderByName']).strip().lower()
        if 'OrderByAmt' in request.data:
            OrderByAmt = str(request.data['OrderByAmt']).strip().lower()

        orderby = "ORDER BY `BP`.`CardName` ASC"
        if str(OrderByName) == 'a-z':
            orderby = "ORDER BY `BP`.`CardName` ASC"
        elif str(OrderByName) == 'z-a':
            orderby = "ORDER BY `BP`.`CardName` DESC"
        elif str(OrderByAmt) == 'asc':
            orderby = f"ORDER BY TransferSum ASC"
        elif str(OrderByAmt) == 'desc':
            orderby = f"ORDER BY TransferSum DESC"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        dataContext = []
        docEntrys = []
        totalSales = 0
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SearchQuery = ''
        if str(SearchText) != '':
            SearchQuery = f"AND (BP.CardCode like '%%{SearchText}%%' OR BP.CardName like '%%{SearchText}%%')"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        fromToDate = ""
        if str(FromDate) != "":
            fromToDate = f"AND INVPay.DocDate >= '{FromDate}' AND INVPay.DocDate <= '{ToDate}'"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        filterBy = f"AND BP.U_U_UTL_Zone IN('{zonesStr}')"
        if str(Filter).lower() == 'group':
            filterBy = f"AND BP.U_U_UTL_Zone IN('{zonesStr}') AND BP.GroupCode = '{Code}'"
        elif str(Filter).lower() == 'zone':
            filterBy = f"AND BP.U_U_UTL_Zone = '{Code}'"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        sqlReceipt = f"""
            SELECT
                BP.CardCode,
                BP.CardName,
                IFNULL(SUM(INVPay.TransferSum), 0) AS `TransferSum`
            FROM BusinessPartner_businesspartner BP
                LEFT JOIN Invoice_incomingpayments INVPay ON INVPay.CardCode = BP.CardCode
            WHERE 
                INVPay.JournalRemarks != 'Canceled'
                {filterBy}
                {fromToDate}
                {SearchQuery}
            GROUP BY BP.CardCode 
            {orderby}
        """
                # AND BP.U_U_UTL_Zone IN('{zonesStr}')
        print(sqlReceipt)
        mycursor.execute(sqlReceipt)
        receipData = mycursor.fetchall()
        if len(receipData) > 0:
            for line in receipData:
                totalSalesByBp = line['TransferSum']
                CardCode = line['CardCode']
                CardName = line['CardName']
                bpData = {
                    "CardName": CardName,
                    "CardCode": CardCode,
                    "TotalSales": round(totalSalesByBp, 2),
                    "TotalReceivePayment":round(totalSalesByBp, 2),
                    "PaymentStatus": "Paid",
                    "DifferenceAmount": 0
                }
                dataContext.append(bpData)

                totalSales = float(totalSales) + float(totalSalesByBp)

        if 'PageNo' in request.data:
            PageNo = int(request.data['PageNo'])
            MaxSize = request.data['MaxSize']
            if MaxSize != "All":
                size = int(MaxSize)
                endWith = (PageNo * size)
                startWith = (endWith - size)
                dataContext = dataContext[startWith:endWith]
        
        TotalSales = totalSales
        TotalReceivePayment = round(totalSales, 2)
        #DifferenceAmount = round(float(float(TotalSales) - float(allPayment)), 2)

        return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": TotalSales, "TotalReceivePayment": TotalReceivePayment, "DifferenceAmount":0})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# bp list with total payment receipt
@api_view(['POST'])
def bp_receipt(request):
    try:
        CardCode = request.data['CardCode']
        SalesType = request.data['Type'] # Gross/Net
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        
        dataContext = []
        docEntrys = []
        totalSales = 0
        totalSalesByBp = 0
        # allPayment = 0
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        bpobj = BusinessPartner.objects.filter(CardCode = CardCode).first()
        PayTermsGrpCode = bpobj.PayTermsGrpCode
        CreditLimit = bpobj.CreditLimit
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        MobileNo = ""
        if BPEmployee.objects.filter(CardCode = CardCode, FirstName = bpobj.ContactPerson).exists():
            bpEmp = BPEmployee.objects.filter(CardCode = CardCode, FirstName = bpobj.ContactPerson).first()
            MobileNo = bpEmp.MobilePhone 
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        ptgcObj = PaymentTermsTypes.objects.filter(GroupNumber = PayTermsGrpCode).first()
        creditLimitDayes = ptgcObj.PaymentTermsGroupName
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        GroupCode = bpobj.GroupCode
        GroupName = ""
        if BusinessPartnerGroups.objects.filter(Code = GroupCode).exists():
            bpGroup = BusinessPartnerGroups.objects.filter(Code = GroupCode).first()
            GroupName = bpGroup.Name

        GSTIN = ""
        BPAddress = ""
        if BPBranch.objects.filter(BPCode = CardCode).exists():
            bpBranch = BPBranch.objects.filter(BPCode = CardCode).first()
            GSTIN = str(bpBranch.GSTIN)
            BPAddress = f"{bpBranch.Street} {bpBranch.City} {bpBranch.ZipCode}"

        BPDataa = [{
            "CardName": bpobj.CardName,
            "CardCode": bpobj.CardCode,
            "EmailAddress": bpobj.EmailAddress,
            "ContactPerson": bpobj.ContactPerson,
            "Phone1": MobileNo, #bpobj.Phone1,
            "GSTIN": GSTIN,
            "BPAddress": BPAddress,
            "GroupName": GroupName,
            "CreditLimit": CreditLimit,
            "CreditLimitDayes": creditLimitDayes,
        }]

        if BusinessPartner.objects.filter(CardCode = CardCode).exists():
            orderList = []
            if str(FromDate) != "":
                orderList = IncomingPayments.objects.filter(CardCode = CardCode, DocDate__gte = FromDate, DocDate__lte = ToDate).exclude(JournalRemarks = 'Canceled').values("id","DocDate", "TransferSum", "DocEntry", "Comments", "DocNum").order_by('-DocDate')
            else:
                orderList = IncomingPayments.objects.filter(CardCode = CardCode).exclude(JournalRemarks = 'Canceled').values("id","DocDate", "TransferSum", "DocEntry", "Comments", "DocNum").order_by('-DocDate')
            
            print('no of order list', len(orderList))
            if 'PageNo' in request.data:
                PageNo = int(request.data['PageNo'])
                MaxSize = request.data['MaxSize']
                if MaxSize != "All":
                    size = int(MaxSize)
                    endWith = (PageNo * size)
                    startWith = (endWith - size)
                    orderList = orderList[startWith:endWith]
            print('no of order list', len(orderList))
            for order in orderList:
                
                docEntrys.append(order['DocEntry'])
                DocTotal = order['TransferSum']
                
                incomingPaymentInvoices = []
                # if IncomingPaymentInvoices.objects.filter(IncomingPaymentsId = order['id']).exists():
                #     invoicesPayments =IncomingPaymentInvoices.objects.filter(IncomingPaymentsId = order['id'])
                #     for obj in invoicesPayments:
                #         InvoiceId = 0
                #         if Invoice.objects.filter(DocEntry = obj.InvoiceDocEntry).exists():
                #             invObj = Invoice.objects.get(DocEntry = obj.InvoiceDocEntry)
                #             InvoiceId = invObj.id

                #         print("InvoiceId", InvoiceId)
                #         tempContaxt = {
                #             "InvoiceId": InvoiceId,
                #             "DocEntry": obj.InvoiceDocEntry,
                #             "ReceiptId": obj.id,
                #             "PaymentAmt": obj.SumApplied,
                #             "CreateDate": obj.DocDate
                #         }
                #         incomingPaymentInvoices.append(tempContaxt)
                            
                bpData = {
                    "OrderId": order['DocEntry'],
                    "DocNum": order['DocNum'],
                    "OrderAmount": DocTotal,
                    "PaymentStatus": "",
                    "CreateDate": order['DocDate'],
                    "Comments": order['Comments'],
                    "IncomingPaymentInvoices": incomingPaymentInvoices
                }                    
                dataContext.append(bpData)
                totalSalesByBp = totalSalesByBp + float(DocTotal)
        else:
            return Response({"message": "Invalid CardCode","status": 201, "data":[], "TotalSales": 0})


        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        fromToDate = ""
        if str(FromDate) != "":
            fromToDate = f"AND INVPay.DocDate >= '{FromDate}' AND INVPay.DocDate <= '{ToDate}'"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        sqlReceipt = f"""
           SELECT
                BP.CardCode,
                BP.CardName,
                IFNULL(SUM(INVPay.TransferSum), 0) AS `TotalReceivePayment`
            FROM BusinessPartner_businesspartner BP
                LEFT JOIN Invoice_incomingpayments INVPay ON INVPay.CardCode = BP.CardCode
            WHERE 
                INVPay.JournalRemarks != 'Canceled'
                AND BP.CardCode = '{CardCode}'
                {fromToDate};
        """

        print(sqlReceipt)
        mycursor.execute(sqlReceipt)
        TotalReceivePayment = 0
        receipData = mycursor.fetchall()
        if len(receipData) > 0:
            TotalReceivePayment = receipData[0]['TotalReceivePayment']

        TotalSales = 0
        # TotalReceivePayment = round(totalSalesByBp, 2)
        #DifferenceAmount = round(float(float(totalSalesByBp) - float(allPayment)), 2)
                
        return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": TotalSales, "TotalReceivePayment": TotalReceivePayment, "BPData":BPDataa})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#BusinessPartner All selected field data API
@api_view(["POST"])
def all_data(request):
    try:
        SalesPersonCode = request.data['SalesPersonCode']
        result = []
        if Employee.objects.filter(SalesEmployeeCode = SalesPersonCode).exists():
            zones = getZoneByEmployee(SalesPersonCode)
            allEmp = getAllReportingToIds(SalesPersonCode)
            businesspartners_obj = BusinessPartner.objects.filter( Q(U_U_UTL_Zone__in = zones) & Q(SalesPersonCode__in = allEmp) | Q(CreatedBy__in = allEmp)).exclude(Link = 'Commission Agent').order_by("CardName")
            result = BPSelectFieldSerializer(businesspartners_obj, many=True).data
        else:
            return Response({"message": "Invalid SalesPersonCode?","status": 201,"data":[]})
        return Response({"message": "Success","status": 200,"data":result})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#BusinessPartner All selected field data API
@api_view(["POST"])
def all_data_pagination(request):
    try:
        PageNo = int(request.data['PageNo'])
        MaxSize = request.data['MaxSize']
        SalesPersonCode = int(request.data['SalesPersonCode'])
        CardType = request.data['CardType'] if 'CardType' in request.data else '' #cCustomer, cSupplier 
        
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        limitQuery = ""
        if 'PageNo' in request.data:
            PageNo = int(request.data['PageNo'])
            MaxSize = request.data['MaxSize']
            if MaxSize != "All":
                size = int(MaxSize)
                endWith = (PageNo * size)
                startWith = (endWith - size)
                # dataContext = dataContext[startWith:endWith]
                limitQuery = f"Limit {startWith}, {MaxSize}"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # if Zones pass then data will be zones wise
        # if 'Zones' in request.data:
        #     InputZones = request.data['Zones']
        #     if str(InputZones).strip() != "":
        #         zones = [InputZones]

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SearchQuery = ""
        if 'SearchText' in request.data:
            SearchText = request.data['SearchText']
            if str(SearchText) != '':
                SearchQuery = f"AND (bp.CardCode like '%%{SearchText}%%' OR bp.CardName like '%%{SearchText}%%')"

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        OrderByName = "" #a-z/z-a
        if 'OrderByName' in request.data:
            OrderByName = str(request.data['OrderByName']).strip().lower()
        
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        CardTypeFilter = ""
        if CardType != "":
            CardTypeFilter = f"AND bp.CardType = '{CardType}'"
        
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        orderby = "ORDER BY bp.CardName ASC"
        if str(OrderByName) == 'a-z':
            orderby = "ORDER BY bp.CardName ASC"
        elif str(OrderByName) == 'z-a':
            orderby = "ORDER BY bp.CardName DESC"

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        if Employee.objects.filter(SalesEmployeeCode = SalesPersonCode).exists():
            zones = getZoneByEmployee(SalesPersonCode)
            print(zones)
            zonesStr = "','".join(zones)
            # emp_obj = Employee.objects.get(SalesEmployeeCode = SalesPersonCode)
            # if emp_obj.role == 'Director':
            #     SalesPersonCode = -1

            mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
            mycursor = mydb.cursor(dictionary=True, buffered=True)
            result = []
            sqlQuery = f"""
                SELECT 
                    bp.id,
                    bp.CardName,
                    bp.CardCode,
                    bp.CardType,
                    bp.EmailAddress as EmailAddress,
                    emp.MobilePhone as Phone1,
                    bp_branch.GSTIN as GSTIN,
                    bp.CreditLimit as CreditLimit,
                    CONCAT(bp_branch.Street, " ", bp_branch.City, " ", bp_branch.ZipCode) as BPAddress
                FROM BusinessPartner_businesspartner as bp
                LEFT JOIN BusinessPartner_bpbranch as bp_branch ON bp_branch.BPID = bp.id AND bp_branch.RowNum = 1
                LEFT JOIN BusinessPartner_bpemployee as emp ON emp.U_BPID = bp.id
                WHERE 
                    bp.U_U_UTL_Zone IN('{zonesStr}')
                    {CardTypeFilter}
                    {SearchQuery}
                {orderby}
                {limitQuery};
            """

            print(sqlQuery)
            mycursor.execute(sqlQuery)
            result = mycursor.fetchall()

            return Response({"message": "Success","status": 200,"data":result})
        else:
            return Response({"message": "Invalid SalesPersonCode?","status": 201,"data":[]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# BusinessPartner Overview Dashboard
@api_view(['POST'])
def bp_overview(request):
    try:
        print(request.data)
        CardCode = request.data['CardCode']
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        contaxt = {}

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        if BusinessPartner.objects.filter(CardCode = CardCode).exists():  

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            BpObj = BusinessPartner.objects.filter(CardCode = CardCode).first()
            LinkedBusinessPartner = BpObj.LinkedBusinessPartner
            PayTermsGrpCode = BpObj.PayTermsGrpCode
            CreditLimit = BpObj.CreditLimit
            ptgcObj = PaymentTermsTypes.objects.filter(GroupNumber = PayTermsGrpCode).first()
            creditLimitDayes = ptgcObj.PaymentTermsGroupName
            GroupCode = BpObj.GroupCode
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            GroupName = ""
            if BusinessPartnerGroups.objects.filter(Code = GroupCode).exists():
                bpGroup = BusinessPartnerGroups.objects.filter(Code = GroupCode).first()
                GroupName = bpGroup.Name
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # ----------- Respones Header details-----------
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            LastSalesDate = ""
            LastRecipetDate = ""
            BpInvoiceList = []
            if str(FromDate) != "":
                LastSalesDate = Invoice.objects.filter(CancelStatus="csNo", CardCode = CardCode, DocDate__gte = FromDate, DocDate__lte = ToDate).order_by('-DocDate').values_list('DocDate', flat=True).first()
                LastRecipetDate = IncomingPayments.objects.filter(CardCode = CardCode, DocDate__gte = FromDate, DocDate__lte = ToDate).exclude(JournalRemarks = 'Canceled').order_by('-DocDate').values_list('DocDate', flat=True).first()
                BpInvoiceList = Invoice.objects.filter(CancelStatus="csNo", CardCode = CardCode, DocDate__gte = FromDate, DocDate__lte = ToDate).values_list('DocTotal', flat=True)
            else:
                LastSalesDate = Invoice.objects.filter(CancelStatus="csNo", CardCode = CardCode).order_by('-DocDate').values_list('DocDate', flat=True).first()
                LastRecipetDate = IncomingPayments.objects.filter(CardCode = CardCode).exclude(JournalRemarks = 'Canceled').order_by('-DocDate').values_list('DocDate', flat=True).first()
                BpInvoiceList = Invoice.objects.filter(CancelStatus="csNo", CardCode = CardCode).values_list('DocTotal', flat=True)

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            InvoiceCount = BpInvoiceList.count()
            TotalInvoiceAmt = 0
            for amt in BpInvoiceList:
                TotalInvoiceAmt = (TotalInvoiceAmt + float(amt))
            AvgInvoiceAmount = 0
            if int(InvoiceCount) > 0:
                AvgInvoiceAmount = (TotalInvoiceAmt / InvoiceCount)

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # ----------- Total Sales-----------
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            bpTotalSales = 0
            SalesList = []
            orderList = []
            if str(FromDate) != "":
                orderList = Invoice.objects.filter(CancelStatus="csNo", CardCode = CardCode, DocDate__gte = FromDate, DocDate__lte = ToDate).values("id","DocTotal", "DocDueDate", "DocDate", "VatSum", "DocEntry").order_by('DocDate')
            else:
                orderList = Invoice.objects.filter(CancelStatus="csNo", CardCode = CardCode).values("id","DocTotal", "DocDueDate", "DocDate", "VatSum", "DocEntry").order_by('DocDate')

            for ord in orderList:
                bpTotalSales = bpTotalSales + float(ord['DocTotal'])
                #"InvoiceId": ord['id'] s/b change,
                invContaxt = {
                    "OrderId": ord['id'],
                    "DocEntry": ord['DocEntry'],
                    "CreateDate": ord['DocDate'],
                    "DocTotal": round(float(ord['DocTotal']), 2),
                    "Month": get_mm_yy(ord['DocDate'])
                }
                SalesList.append(invContaxt)
            
            MonthGroupSalesList = groupby(SalesList, ['DocTotal', 'Month'], "Month", "DocTotal")

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # ----------- Total Receipts-----------
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            bpTotalReceipt = 0
            ReceiptList = []
            incomingPayList = []
            if str(FromDate) != "":
                incomingPayList = IncomingPayments.objects.filter(CardCode = CardCode, DocDate__gte = FromDate, DocDate__lte = ToDate).exclude(JournalRemarks = 'Canceled').values("id","TransferSum", "DocDate", "DocEntry")
            else:
                incomingPayList = IncomingPayments.objects.filter(CardCode = CardCode).exclude(JournalRemarks = 'Canceled').values("id","TransferSum", "DocDate", "DocEntry")
                
            for pmt in incomingPayList:
                bpTotalReceipt = bpTotalReceipt + float(pmt['TransferSum'])
                invContaxt = {
                    "ReceiptId": pmt['id'],
                    "DocEntry": pmt['DocEntry'],
                    "CreateDate": pmt['DocDate'],
                    "DocTotal": round(float(pmt['TransferSum']), 2),
                    "Month": get_mm_yy(pmt['DocDate'])
                }
                ReceiptList.append(invContaxt)                 
            
            
            MonthGroupReceiptList = groupby(ReceiptList, ['DocTotal', 'Month'], "Month", "DocTotal")
            
            # # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # # ----------- Total Receivables-----------
            # # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            bpTotalReceivable = 0
            ReceivableList = []
            OverList = []
            UnderList = []
            invoiceList = []
            TotalReceiableAmt = 0
            totalSalesByBp = 0
            allCreditNote = 0


            bpJELineTotal = 0
            sqlSelectReceiable = f"""
                SELECT * FROM `BusinessPartner_receivable`
                WHERE
                    CardCode = '{CardCode}'
                    AND `CronUpdateCount` = (SELECT MAX(`CronUpdateCount`) FROM BusinessPartner_receivable) - 1
            """

            print(sqlSelectReceiable)
            mycursor.execute(sqlSelectReceiable)
            orderList = mycursor.fetchall()      
            if len(orderList) != 0:
                for order in orderList:
                    DocEntry      = order['DocEntry']
                    TransId       = order['TransId']
                    TransType     = order['TransType']
                    PendingTotal  = float(order['TotalDue'])
                    DueDaysGroup  = order['DueDaysGroup']
                    DocDate       = order['DocDate']
                    DocDueDate    = order['DueDate']
                    PaymentStatus = "Unpaid"

                    print("DocEntry", DocEntry, "TransType", TransType)
                    if str(TransType) == 'Invoice':
                        PaymentStatus = "Unpaid"                        
                        overDueDays = 0

                        invContaxt = {
                            "InvoiceId":DocEntry,
                            "DocEntry": DocEntry,
                            "CreateDate": DocDate,
                            "DocDueDate": DocDueDate,
                            "DocTotal": round(float(PendingTotal), 2),
                            "OverDueDays": DueDaysGroup,
                            "OverDueGroup": DueDaysGroup,
                            "Month": get_mm_yy(DocDate)
                        }
                        ReceivableList.append(invContaxt)
                        TotalReceiableAmt = TotalReceiableAmt + float(PendingTotal)
                                        
                        OverList.append(invContaxt)
                    else:
                        bpJELineTotal = bpJELineTotal + PendingTotal
                # endfor
            # end if

                
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            #                            CreditNotes        
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            allCreditNoteList = []
            if str(FromDate) != "":
                allCreditNoteList = CreditNotes.objects.filter( CancelStatus="csNo", CardCode = CardCode, DocDate__gte = FromDate, DocDate__lte = ToDate ).values('id', 'DocNum', 'DocTotal', 'DocDate', 'PaidToDateSys')
            else:
                allCreditNoteList = CreditNotes.objects.filter( CancelStatus="csNo", CardCode = CardCode ).values('id', 'DocNum', 'DocTotal', 'DocDate', 'PaidToDateSys')
            
            bpCreditNote = 0
            for item2 in allCreditNoteList:
                # DocTotal = abs(float(item2['DocTotal']) - float(item2['PaidToDateSys']))
                DocTotal = abs(float(item2['DocTotal']))
                # print("CreditNoteDocTotal", DocTotal)
                bpCreditNote += float(DocTotal)
            allCreditNote += bpCreditNote

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            #                           Vender Purchases Invoices
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # >>>>>>>>>> Invoices >>>>>>>>>>>
            print("LinkedBusinessPartner", LinkedBusinessPartner)
            bpTotalPurchases = 0
            purchaseList = []
            purchaseInvoicesList = []
            if str(FromDate) != "":
                purchaseInvoicesList = PurchaseInvoices.objects.filter(CancelStatus="csNo", CardCode = LinkedBusinessPartner, DocDate__gte = FromDate, DocDate__lte = ToDate).values("id","DocTotal", "DocDueDate", "DocDate", "VatSum", "DocEntry").order_by('-id')
            else:
                purchaseInvoicesList = PurchaseInvoices.objects.filter(CancelStatus="csNo", CardCode = LinkedBusinessPartner).values("id","DocTotal", "DocDueDate", "DocDate", "VatSum", "DocEntry").order_by('-id')

            for apInv in purchaseInvoicesList:
                bpTotalPurchases = bpTotalPurchases + float(apInv['DocTotal'])
                invContaxt = {
                    "OrderId": apInv['id'],
                    "DocEntry": apInv['DocEntry'],
                    "CreateDate": apInv['DocDate'],
                    "DocTotal": float(apInv['DocTotal']),
                    "Month": get_mm_yy(apInv['DocDate'])
                }
                purchaseList.append(invContaxt)

            MonthGroupPurchaseList = groupby(purchaseList, ['DocTotal', 'Month'], "Month", "DocTotal")
            
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            #                       Vender Payments
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            bpTotalPurchasesReceipt = 0
            PurchaseReceiptList = []
            incomingPayList = []
            if str(FromDate) != "":
                incomingPayList = VendorPayments.objects.filter(CardCode = LinkedBusinessPartner, DocDate__gte = FromDate, DocDate__lte = ToDate).values("id","TransferSum", "DocDate", "DocEntry")
            else:
                incomingPayList = VendorPayments.objects.filter(CardCode = LinkedBusinessPartner).values("id","TransferSum", "DocDate", "DocEntry")
                
            for pmt in incomingPayList:
                bpTotalPurchasesReceipt = bpTotalPurchasesReceipt + float(pmt['TransferSum'])
                invContaxt = {
                    "ReceiptId": pmt['id'],
                    "DocEntry": pmt['DocEntry'],
                    "CreateDate": pmt['DocDate'],
                    "DocTotal": float(pmt['TransferSum']),
                    "Month": get_mm_yy(pmt['DocDate'])
                }
                PurchaseReceiptList.append(invContaxt) 

            MonthGroupPurchaseReceiptList = groupby(PurchaseReceiptList, ['DocTotal', 'Month'], "Month", "DocTotal")

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            #                       Vender CreditNots
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            allPurchaseCreditNoteList = []
            if str(FromDate) != "":
                allPurchaseCreditNoteList = PurchaseCreditNotes.objects.filter(CardCode = LinkedBusinessPartner, DocDate__gte = FromDate, DocDate__lte = ToDate).values_list('DocTotal', flat=True)
            else:
                allPurchaseCreditNoteList = PurchaseCreditNotes.objects.filter(CardCode = LinkedBusinessPartner).values_list('DocTotal', flat=True)
            
            allPurchaseCreditNote = 0
            for item2 in allPurchaseCreditNoteList:
                allPurchaseCreditNote += float(item2)

            # bpTotalReceivable = bpTotalSales - bpTotalReceipt
            bpTotalReceivable = TotalReceiableAmt


            MonthGroupReceivableList = groupby(ReceivableList, ['DocTotal', 'Month'], "Month", "DocTotal")
            MonthGroupOverList = groupby(OverList, ['DocTotal', 'Month'], "Month", "DocTotal")
            MonthGroupUnderList = groupby(UnderList, ['DocTotal', 'Month'], "Month", "DocTotal")
            
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>    

            # Ods = Order.objects.filter(CardCode=request.data["CardCode"],DocumentStatus = 'bost_Open', CancelStatus="csNo")
            # allord = pending_order(Ods)        
            # pd_ods = pd.DataFrame(allord, columns=['OrderID', 'OrderDocEntry', 'CardCode', 'CardName', 'PendingAmount', 'PendingQty'])
            # df = pd_ods.groupby(['CardCode', 'CardName'], as_index=False)['PendingAmount'].sum()
            
            # Total = pd_ods['PendingAmount'].sum()

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # Total Credit Notes
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            TotalPendings = 0
            sqlPendings = f"""SELECT bp.CardCode as CardCode, bp.CardName as CardName, A.id, A.DocEntry, IFNULL(SUM(A.DocTotal), 0) AS 'DocTotal', IFNULL(SUM(A.TotalOpenAmount), 0) AS 'TotalOpenAmount', IFNULL(SUM(A.TotalRemainingOpenQuantity), 0) AS 'TotalRemainingOpenQuantity' FROM BusinessPartner_businesspartner bp INNER JOIN ( SELECT ord.id, ord.CardCode, ord.DocEntry, ord.DocTotal, IFNULL(SUM(ORDLine.UnitPrice * ORDLine.RemainingOpenQuantity), 0) AS TotalOpenAmount, IFNULL(SUM(ORDLine.RemainingOpenQuantity), 0) AS TotalRemainingOpenQuantity FROM Order_order ord LEFT JOIN Order_documentlines ORDLine ON ORDLine.OrderID = ord.id WHERE ord.CancelStatus = 'csNo' AND ord.DocumentStatus = 'bost_Open' AND RemainingOpenQuantity > 0 GROUP BY ord.CardCode, ord.id ) A ON bp.CardCode = A.CardCode WHERE bp.CardCode = '{CardCode}' HAVING TotalRemainingOpenQuantity > 0 """
            print(sqlPendings)
            mycursor.execute(sqlPendings)
            allPendingsData = mycursor.fetchall()        
            if len(allPendingsData) > 0:
                TotalPendings = allPendingsData[0]['TotalOpenAmount']
            
            contaxt = {
                "CardCode": str(BpObj.CardCode),
                "LinkedBusinessPartner": LinkedBusinessPartner,
                "CardName": str(BpObj.CardName),
                "CreditLimit": CreditLimit,
                "CreditLimitLeft": creditLimitDayes,
                "GroupName": GroupName,
                "LastSalesDate": str(LastSalesDate),
                "LastRecipetDate": str(LastRecipetDate),
                "InvoiceCount": str(InvoiceCount), 
                "AvgInvoiceAmount": round(AvgInvoiceAmount, 2),

                # salesorder
                "TotalSales": round(bpTotalSales, 2),
                "SalesList": [], #SalesList
                "MonthGroupSalesList": MonthGroupSalesList,

                # invoices
                # "TotalReceivable": abs(round(float(float(bpTotalReceivable) - float(bpCreditNote) + float(bpJELineTotal)), 2)),
                "TotalReceivable": round(bpTotalReceivable, 2),
                "ReceivableList": [], #ReceivableList
                "OverList": OverList,
                "UnderList": UnderList,
                "MonthGroupReceivableList": MonthGroupReceivableList,
                "MonthGroupOverList": MonthGroupOverList,
                "MonthGroupUnderList": MonthGroupUnderList,
                "TotalJECreditNote":round(bpJELineTotal, 2),
                
                # payment collection
                "TotalReceipt": round(bpTotalReceipt, 2),
                "ReceiptList": [], #ReceiptList
                "MonthGroupReceiptList": MonthGroupReceiptList,
                "AvgPayDays": 0,
                "PendingAmount":round(TotalPendings, 2),
                "TotalCreditNote":bpCreditNote,
                
                # >>>>>>>>>>>>>>>>>>>>>> Purchase 
                # Invoices
                "TotalPurchases":round(bpTotalPurchases, 2),
                "PurchaseList":[],
                "MonthGroupPurchaseList":MonthGroupPurchaseList,
                # Payments
                "TotalPurchasesReceipt":bpTotalPurchasesReceipt,
                "PurchaseReceiptList":[],
                "MonthGroupPurchaseReceiptList":MonthGroupPurchaseReceiptList,
                # CreditNote
                "PurchaseCreditNote":allPurchaseCreditNote

            }
            return Response({"message": "Success","status": 200,"data":[contaxt]})
        else:
            return Response({"message": "Invalid CardCode?","status": 201,"data":[]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# bp debit credit
@api_view(['POST'])
def bp_debit_credit(request):
    try:
        CardCode = request.data['CardCode']
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        
        dataContext = []
        docEntrys = []
        totalSales = 0
        totalSalesByBp = 0

        if BusinessPartner.objects.filter(CardCode = CardCode).exists():
            orderList = []
            if str(FromDate) != "":
                orderList = Invoice.objects.filter(CancelStatus="csNo", CardCode = CardCode, DocDate__gte = FromDate, DocDate__lte = ToDate).values("id", "CardCode", "DocTotal", "CreationDate", "DocEntry").order_by('-id')
            else:
                orderList = Invoice.objects.filter(CancelStatus="csNo", CardCode = CardCode).values("id", "CardCode", "DocTotal", "CreationDate", "DocEntry").order_by('-id')
            
            if len(orderList) != 0:
                for order in orderList:
                    docEntrys.append(order['DocEntry'])
                    
                    bpData = {
                        "CardCode": order['CardCode'],
                        "Type": "Sales",
                        "OrderId": order['DocEntry'],
                        "Amount": order['DocTotal'],
                        "CreateDate": order['CreationDate']
                    }                    
                    dataContext.append(bpData)
                    totalSalesByBp = totalSalesByBp + float(order['DocTotal'])
            else:
                pass
                #print('no invoice')
        else:
            return Response({"message": "Invalid CardCode","status": 201, "data":[], "TotalSales": 0})

        allPaymentsList = []
        if str(FromDate) != "":
            allPaymentsList = IncomingPayments.objects.filter(CardCode = CardCode, TransferDate__gte = FromDate, TransferDate__lte = ToDate).exclude(JournalRemarks = 'Canceled').values('CardCode', 'DocEntry', 'TransferDate', 'TransferSum')
        else:
            allPaymentsList = IncomingPayments.objects.filter(CardCode = CardCode).exclude(JournalRemarks = 'Canceled').values('CardCode', 'DocEntry', 'TransferDate', 'TransferSum')
        
        allPayment = 0
        for item in allPaymentsList:
            allPayment += float(item['TransferSum'])
            pmData = {
                    "CardCode": item['CardCode'],
                    "Type": "Receipt",
                    "OrderId": item['DocEntry'],
                    "Amount": item['TransferSum'],
                    "CreateDate": item['TransferDate']
                }                    
            dataContext.append(pmData)
            #totalSalesByBp = totalSalesByBp + float(order['DocTotal'])

        TotalSales = round(totalSalesByBp, 2)
        TotalReceivePayment = round(allPayment, 2)
        DifferenceAmount = round(float(float(totalSalesByBp) - float(allPayment)), 2)
        #print(dataContext)
        dataContext_date = sorted(dataContext, key=lambda d: d['CreateDate'])
        #print('------dataContext_sort----')
        ##print(dataContext_type)
        dataContext_arr=[]
        blnc=0
        for ss in dataContext_date:
            #print(ss)
            if ss['Type']=='Sales':
                blnc = blnc + float(ss['Amount'])
            else:    
                blnc = blnc - float(ss['Amount'])
            ss['Balance'] = blnc
            dataContext_arr.append(ss)

        return Response({"message": "Success","status": 200, "data":dataContext_arr, "TotalSales": TotalSales, "TotalReceivePayment": TotalReceivePayment, "Closing": DifferenceAmount})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# update Category Items and Uom
@api_view(['GET'])
def syncBP(request):
    try:
        # Import and sync BusinessPartner
        businessPartnerBP ="BusinessPartner/BP.py"
        exec(compile(open(businessPartnerBP, "rb").read(), businessPartnerBP, 'exec'), {})

        return Response({"message":"Successful","status":200, "data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"Model": "Items" ,"data":[]})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def monthly_sales_chart(request):
    try:
        print(request.data)
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        SalesPersonCode = request.data['SalesPersonCode']
        zones = getZoneByEmployee(SalesPersonCode)
        zonesStr = "','".join(zones)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        fromToDate = ""
        if str(FromDate) != "":
            fromToDate = f"AND inv.DocDate >= '{FromDate}' AND inv.DocDate <= '{ToDate}'"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        finaldataSet = getMonthlyReportFromate(FromDate)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        sqlReceipt = f"""
            SELECT
                inv.DocDate as DocDate,
                MONTH(inv.DocDate) as Month,
                YEAR(inv.DocDate) as Year,
                IFNULL(SUM(inv.DocTotal), 0) AS `DocTotal`,
                IFNULL(SUM(inv.PaidToDateSys), 0) AS `PaidToDateSys`,
                IFNULL( SUM( inv.DocTotal - inv.PaidToDateSys ), 0 ) AS `PendingTotal`
            FROM BusinessPartner_businesspartner bp
            LEFT JOIN BusinessPartner_businesspartnergroups bpgroup ON bpgroup.Code = bp.GroupCode
            LEFT JOIN Invoice_invoice inv ON bp.CardCode = inv.CardCode
            WHERE
                inv.CancelStatus = 'csNo'
                AND bp.U_U_UTL_Zone IN('{zonesStr}')
                {fromToDate}
            GROUP BY MONTH(inv.DocDate)
        """
        print(sqlReceipt)
        mycursor.execute(sqlReceipt)
        monthlySalesData = mycursor.fetchall()
        if len(monthlySalesData) != 0:
            for data in monthlySalesData:
                # DocDate  = data['DocDate']
                Month    = data['Month']
                Year     = data['Year']
                DocTotal = data['DocTotal']
                finaldataSet[Month-4]['MonthlySales'] = round(float(DocTotal), 2)
                finaldataSet[Month-4]['Year'] = Year

        return Response({"message":"Successful","status":200, "data":finaldataSet})
    except Exception as e:
        return Response({"message":str(e),"status":201,"Model": "Items" ,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def monthly_purchase_chart(request):
    try:
        print(request.data)
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        SalesPersonCode = request.data['SalesPersonCode']
        zones = getZoneByEmployee(SalesPersonCode)
        zonesStr = "','".join(zones)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        fromToDate = ""
        if str(FromDate) != "":
            fromToDate = f"AND inv.DocDate >= '{FromDate}' AND inv.DocDate <= '{ToDate}'"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        finaldataSet = getMonthlyReportFromate(FromDate)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        sqlReceipt = f"""
            SELECT
                inv.DocDate as DocDate,
                MONTH(inv.DocDate) as Month,
                YEAR(inv.DocDate) as Year,
                IFNULL(SUM(inv.DocTotal), 0) AS `DocTotal`,
                IFNULL(SUM(inv.PaidToDateSys), 0) AS `PaidToDateSys`,
                IFNULL( SUM( inv.DocTotal - inv.PaidToDateSys ), 0 ) AS `PendingTotal`
            FROM BusinessPartner_businesspartner bp
            LEFT JOIN BusinessPartner_businesspartnergroups bpgroup ON bpgroup.Code = bp.GroupCode
            LEFT JOIN PurchaseInvoices_purchaseinvoices inv ON bp.CardCode = inv.CardCode
            WHERE
                inv.CancelStatus = 'csNo'
                AND bp.U_U_UTL_Zone IN('{zonesStr}')
                {fromToDate}
            GROUP BY MONTH(inv.DocDate)
        """
        print(sqlReceipt)
        mycursor.execute(sqlReceipt)
        monthlySalesData = mycursor.fetchall()
        if len(monthlySalesData) != 0:
            for data in monthlySalesData:
                # DocDate  = data['DocDate']
                Month    = data['Month']
                Year     = data['Year']
                DocTotal = data['DocTotal']
                finaldataSet[Month-4]['MonthlySales'] = round(float(DocTotal), 2)
                finaldataSet[Month-4]['Year'] = Year

        return Response({"message":"Successful","status":200, "data":finaldataSet})
    except Exception as e:
        return Response({"message":str(e),"status":201,"Model": "Items" ,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def monthly_receivable_chart(request):
    try:
        print(request.data)
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        SalesPersonCode = request.data['SalesPersonCode']
        zones = getZoneByEmployee(SalesPersonCode)
        zonesStr = "','".join(zones)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        fromToDate = ""
        if str(FromDate) != "":
            fromToDate = f"AND inv.DocDate >= '{FromDate}' AND inv.DocDate <= '{ToDate}'"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        finaldataSet = getMonthlyReportFromate(FromDate)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        sqlReceipt = f"""
            SELECT
                inv.DocDate as DocDate,
                MONTH(inv.DocDate) as Month,
                YEAR(inv.DocDate) as Year,
                IFNULL(SUM(inv.`TotalDue`), 0) AS `DocTotal`
            FROM BusinessPartner_businesspartner bp
            LEFT JOIN BusinessPartner_receivable inv ON bp.CardCode = inv.CardCode
            WHERE
                bp.U_U_UTL_Zone IN('{zonesStr}')
                AND `CronUpdateCount` = (SELECT MAX(`CronUpdateCount`) FROM BusinessPartner_receivable) - 1
                {fromToDate}
            GROUP BY MONTH(inv.DocDate)
        """
        print(sqlReceipt)
        mycursor.execute(sqlReceipt)
        monthlySalesData = mycursor.fetchall()
        if len(monthlySalesData) != 0:
            for data in monthlySalesData:
                # DocDate  = data['DocDate']
                Month    = data['Month']
                Year     = data['Year']
                DocTotal = data['DocTotal']
                finaldataSet[Month-4]['MonthlySales'] = round(float(DocTotal), 2)
                finaldataSet[Month-4]['Year'] = Year

        return Response({"message":"Successful","status":200, "data":finaldataSet})
    except Exception as e:
        return Response({"message":str(e),"status":201,"Model": "Items" ,"data":[]})
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def monthly_payable_chart(request):
    try:
        print(request.data)
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        SalesPersonCode = request.data['SalesPersonCode']
        zones = getZoneByEmployee(SalesPersonCode)
        zonesStr = "','".join(zones)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        fromToDate = ""
        if str(FromDate) != "":
            fromToDate = f"AND inv.DocDate >= '{FromDate}' AND inv.DocDate <= '{ToDate}'"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        finaldataSet = getMonthlyReportFromate(FromDate)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        sqlReceipt = f"""
            SELECT
                inv.DocDate as DocDate,
                MONTH(inv.DocDate) as Month,
                YEAR(inv.DocDate) as Year,
                IFNULL(SUM(inv.`TotalDue`), 0) AS `DocTotal`
            FROM BusinessPartner_businesspartner bp
            LEFT JOIN BusinessPartner_payable inv ON bp.CardCode = inv.CardCode
            WHERE
                bp.U_U_UTL_Zone IN('{zonesStr}')
                AND `CronUpdateCount` = (SELECT MAX(`CronUpdateCount`) FROM BusinessPartner_payable) - 1
                {fromToDate}
            GROUP BY MONTH(inv.DocDate)
        """
        print(sqlReceipt)
        mycursor.execute(sqlReceipt)
        monthlySalesData = mycursor.fetchall()
        if len(monthlySalesData) != 0:
            for data in monthlySalesData:
                # DocDate  = data['DocDate']
                Month    = data['Month']
                Year     = data['Year']
                DocTotal = data['DocTotal']
                finaldataSet[Month-4]['MonthlySales'] = round(float(DocTotal), 2)
                finaldataSet[Month-4]['Year'] = Year

        return Response({"message":"Successful","status":200, "data":finaldataSet})
    except Exception as e:
        return Response({"message":str(e),"status":201,"Model": "Items" ,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def monthly_receivable_group_chart(request):
    try:
        print(request.data)
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        SalesPersonCode = request.data['SalesPersonCode']
        zones = getZoneByEmployee(SalesPersonCode)
        zonesStr = "','".join(zones)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        fromToDate = ""
        if str(FromDate) != "":
            fromToDate = f"AND DocDate >= '{FromDate}' AND DocDate <= '{ToDate}'"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        sqlReceivable = f"""
            SELECT 
                id,
                ROUND(SUM(TotalDue), 2) as TotalDue,
                CASE
                    WHEN OverDueDays BETWEEN 0 AND 30 THEN '0-30'
                    WHEN OverDueDays BETWEEN 31 AND 45 THEN '31-45'
                    WHEN OverDueDays BETWEEN 46 AND 60 THEN '46-60'
                    WHEN OverDueDays BETWEEN 61 AND 90 THEN '61-90'
                    ELSE '>90'
                END AS OverDueDaysGroup,
                CASE
                    WHEN OverDueDays BETWEEN 0 AND 30 THEN '30'
                    WHEN OverDueDays BETWEEN 31 AND 45 THEN '45'
                    WHEN OverDueDays BETWEEN 46 AND 60 THEN '60'
                    WHEN OverDueDays BETWEEN 61 AND 90 THEN '90'
                    ELSE '90+'
                END AS OverDueDaysGroup2
            FROM BusinessPartner_receivable
            WHERE 
                U_U_UTL_Zone IN('{zonesStr}')
                AND `CronUpdateCount` = (SELECT MAX(`CronUpdateCount`) FROM BusinessPartner_receivable) - 1
                {fromToDate}
            GROUP BY OverDueDaysGroup
            ORDER BY OverDueDaysGroup2 ASC;
        """
        print(sqlReceivable)
        mycursor.execute(sqlReceivable)
        monthlySalesData = mycursor.fetchall()
        return Response({"message":"Successful","status":200, "data":monthlySalesData})
    except Exception as e:
        return Response({"message":str(e),"status":201,"Model": "Items" ,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def monthly_payable_group_chart(request):
    try:
        print(request.data)
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        SalesPersonCode = request.data['SalesPersonCode']
        zones = getZoneByEmployee(SalesPersonCode)
        zonesStr = "','".join(zones)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        fromToDate = ""
        if str(FromDate) != "":
            fromToDate = f"AND DocDate >= '{FromDate}' AND DocDate <= '{ToDate}'"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        sqlReceivable = f"""
            SELECT 
                id,
                ROUND(SUM(TotalDue), 2) as TotalDue,
                CASE
                    WHEN OverDueDays BETWEEN 0 AND 30 THEN '0-30'
                    WHEN OverDueDays BETWEEN 31 AND 45 THEN '31-45'
                    WHEN OverDueDays BETWEEN 46 AND 60 THEN '46-60'
                    WHEN OverDueDays BETWEEN 61 AND 90 THEN '61-90'
                    ELSE '>90'
                END AS OverDueDaysGroup,
                CASE
                    WHEN OverDueDays BETWEEN 0 AND 30 THEN '30'
                    WHEN OverDueDays BETWEEN 31 AND 45 THEN '45'
                    WHEN OverDueDays BETWEEN 46 AND 60 THEN '60'
                    WHEN OverDueDays BETWEEN 61 AND 90 THEN '90'
                    ELSE '90+'
                END AS OverDueDaysGroup2
            FROM BusinessPartner_payable
            WHERE 
                U_U_UTL_Zone IN('{zonesStr}')
                AND `CronUpdateCount` = (SELECT MAX(`CronUpdateCount`) FROM BusinessPartner_payable) - 1
                {fromToDate}
            GROUP BY OverDueDaysGroup
            ORDER BY OverDueDaysGroup2 ASC;
        """
        print(sqlReceivable)
        mycursor.execute(sqlReceivable)
        monthlySalesData = mycursor.fetchall()
        return Response({"message":"Successful","status":200, "data":monthlySalesData})
    except Exception as e:
        return Response({"message":str(e),"status":201,"Model": "Items" ,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# created on 01-02-24
@api_view(['POST'])
def monthly_receivable_group_chart_filter(request):
    try:
        print("come graph")
        print(request.data)

        Filter = request.data['Filter']
        Code = request.data['Code']

        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        SalesPersonCode = request.data['SalesPersonCode']
        zones = getZoneByEmployee(SalesPersonCode)
        zonesStr = "','".join(zones)
        
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        filterBy = f"U_U_UTL_Zone IN('{zonesStr}')"
        if str(Filter).lower() == 'group':
            filterBy = f"U_U_UTL_Zone IN('{zonesStr}') AND GroupCode = '{Code}'"
        elif str(Filter).lower() == 'zone':
            filterBy = f"U_U_UTL_Zone = '{Code}'"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        fromToDate = ""
        if str(FromDate) != "":
            fromToDate = f"AND DocDate >= '{FromDate}' AND DocDate <= '{ToDate}'"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        sqlReceivable = f"""
            SELECT 
                id,
                ROUND(SUM(TotalDue), 2) as TotalDue,
                CASE
                    WHEN OverDueDays BETWEEN 0 AND 30 THEN '0-30'
                    WHEN OverDueDays BETWEEN 31 AND 45 THEN '31-45'
                    WHEN OverDueDays BETWEEN 46 AND 60 THEN '46-60'
                    WHEN OverDueDays BETWEEN 61 AND 90 THEN '61-90'
                    ELSE '>90'
                END AS OverDueDaysGroup,
                CASE
                    WHEN OverDueDays BETWEEN 0 AND 30 THEN '30'
                    WHEN OverDueDays BETWEEN 31 AND 45 THEN '45'
                    WHEN OverDueDays BETWEEN 46 AND 60 THEN '60'
                    WHEN OverDueDays BETWEEN 61 AND 90 THEN '90'
                    ELSE '90+'
                END AS OverDueDaysGroup2
            FROM BusinessPartner_receivable
            WHERE 
                {filterBy}
                AND `CronUpdateCount` = (SELECT MAX(`CronUpdateCount`) FROM BusinessPartner_receivable) - 1
                {fromToDate}
            GROUP BY OverDueDaysGroup
            ORDER BY OverDueDaysGroup2 ASC;
        """
        print(sqlReceivable)
        mycursor.execute(sqlReceivable)
        monthlySalesData = mycursor.fetchall()
        #print(data_arr)
        for obj in monthlySalesData:
            print(obj['OverDueDaysGroup2'])

            if obj['OverDueDaysGroup2'] == "30":
                data_arr[0] = obj
            elif obj['OverDueDaysGroup2'] == "45":
                data_arr[1] = obj
            elif obj['OverDueDaysGroup2'] == "60":
                data_arr[2] = obj
            elif obj['OverDueDaysGroup2'] == "90":
                data_arr[3] = obj
            elif obj['OverDueDaysGroup2'] == "90+":
                data_arr[4] = obj
            else:
                print("not match obj")

        #return Response({"message":"Successful","status":200, "data":monthlySalesData})
        return Response({"message":"Successful","status":200, "data":data_arr})
    except Exception as e:
        return Response({"message":str(e),"status":201,"Model": "Items" ,"data":[]})
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# created on 01-02-24
@api_view(['POST'])
def monthly_payable_group_chart_filter(request):
    try:
        print("come graph")
        print(request.data)

        Filter = request.data['Filter']
        Code = request.data['Code']

        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        SalesPersonCode = request.data['SalesPersonCode']
        zones = getZoneByEmployee(SalesPersonCode)
        zonesStr = "','".join(zones)
        
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        filterBy = f"U_U_UTL_Zone IN('{zonesStr}')"
        if str(Filter).lower() == 'group':
            filterBy = f"U_U_UTL_Zone IN('{zonesStr}') AND GroupCode = '{Code}'"
        elif str(Filter).lower() == 'zone':
            filterBy = f"U_U_UTL_Zone = '{Code}'"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        fromToDate = ""
        if str(FromDate) != "":
            fromToDate = f"AND DocDate >= '{FromDate}' AND DocDate <= '{ToDate}'"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        sqlReceivable = f"""
            SELECT 
                id,
                ROUND(SUM(TotalDue), 2) as TotalDue,
                CASE
                    WHEN OverDueDays BETWEEN 0 AND 30 THEN '0-30'
                    WHEN OverDueDays BETWEEN 31 AND 45 THEN '31-45'
                    WHEN OverDueDays BETWEEN 46 AND 60 THEN '46-60'
                    WHEN OverDueDays BETWEEN 61 AND 90 THEN '61-90'
                    ELSE '>90'
                END AS OverDueDaysGroup,
                CASE
                    WHEN OverDueDays BETWEEN 0 AND 30 THEN '30'
                    WHEN OverDueDays BETWEEN 31 AND 45 THEN '45'
                    WHEN OverDueDays BETWEEN 46 AND 60 THEN '60'
                    WHEN OverDueDays BETWEEN 61 AND 90 THEN '90'
                    ELSE '90+'
                END AS OverDueDaysGroup2
            FROM BusinessPartner_payable
            WHERE 
                {filterBy}
                AND `CronUpdateCount` = (SELECT MAX(`CronUpdateCount`) FROM BusinessPartner_payable) - 1
                {fromToDate}
            GROUP BY OverDueDaysGroup
            ORDER BY OverDueDaysGroup2 ASC;
        """
        print(sqlReceivable)
        mycursor.execute(sqlReceivable)
        monthlySalesData = mycursor.fetchall()
        #print(data_arr)
        for obj in monthlySalesData:
            print(obj['OverDueDaysGroup2'])

            if obj['OverDueDaysGroup2'] == "30":
                data_arr[0] = obj
            elif obj['OverDueDaysGroup2'] == "45":
                data_arr[1] = obj
            elif obj['OverDueDaysGroup2'] == "60":
                data_arr[2] = obj
            elif obj['OverDueDaysGroup2'] == "90":
                data_arr[3] = obj
            elif obj['OverDueDaysGroup2'] == "90+":
                data_arr[4] = obj
            else:
                print("not match obj")

        #return Response({"message":"Successful","status":200, "data":monthlySalesData})
        return Response({"message":"Successful","status":200, "data":data_arr})
    except Exception as e:
        return Response({"message":str(e),"status":201,"Model": "Items" ,"data":[]})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def monthly_pending_chart(request):
    try:
        print(request.data)
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        SalesPersonCode = request.data['SalesPersonCode']
        zones = getZoneByEmployee(SalesPersonCode)
        zonesStr = "','".join(zones)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        fromToDate = ""
        if str(FromDate) != "":
            fromToDate = f"AND inv.DocDate >= '{FromDate}' AND inv.DocDate <= '{ToDate}'"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        finaldataSet = getMonthlyReportFromate(FromDate)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        sqlReceipt = f"""
            SELECT
                inv.DocDate as DocDate,
                MONTH(inv.DocDate) as Month,
                YEAR(inv.DocDate) as Year,
                IFNULL(SUM(inv.DocTotal), 0) AS `DocTotal`
            FROM BusinessPartner_businesspartner bp
            LEFT JOIN BusinessPartner_businesspartnergroups bpgroup ON bpgroup.Code = bp.GroupCode
            LEFT JOIN Order_order inv ON bp.CardCode = inv.CardCode
            WHERE
                inv.CancelStatus = 'csNo'
                AND bp.U_U_UTL_Zone IN('{zonesStr}')
                {fromToDate}
            GROUP BY MONTH(inv.DocDate)
        """
        print(sqlReceipt)
        mycursor.execute(sqlReceipt)
        monthlySalesData = mycursor.fetchall()
        if len(monthlySalesData) != 0:
            for data in monthlySalesData:
                # DocDate  = data['DocDate']
                Month    = data['Month']
                Year     = data['Year']
                DocTotal = data['DocTotal']
                finaldataSet[Month-4]['MonthlySales'] = round(float(DocTotal), 2)
                finaldataSet[Month-4]['Year'] = Year

        return Response({"message":"Successful","status":200, "data":finaldataSet})
    except Exception as e:
        return Response({"message":str(e),"status":201,"Model": "Items" ,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def monthly_pending_purchase_chart(request):
    try:
        print(request.data)
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        SalesPersonCode = request.data['SalesPersonCode']
        zones = getZoneByEmployee(SalesPersonCode)
        zonesStr = "','".join(zones)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        fromToDate = ""
        if str(FromDate) != "":
            fromToDate = f"AND inv.DocDate >= '{FromDate}' AND inv.DocDate <= '{ToDate}'"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        finaldataSet = getMonthlyReportFromate(FromDate)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        sqlReceipt = f"""
            SELECT
                inv.DocDate as DocDate,
                MONTH(inv.DocDate) as Month,
                YEAR(inv.DocDate) as Year,
                IFNULL(SUM(inv.DocTotal), 0) AS `DocTotal`
            FROM BusinessPartner_businesspartner bp
            LEFT JOIN BusinessPartner_businesspartnergroups bpgroup ON bpgroup.Code = bp.GroupCode
            LEFT JOIN PurchaseOrders_purchaseorders inv ON bp.CardCode = inv.CardCode
            WHERE
                inv.CancelStatus = 'csNo'
                AND bp.U_U_UTL_Zone IN('{zonesStr}')
                {fromToDate}
            GROUP BY MONTH(inv.DocDate)
        """
        print(sqlReceipt)
        mycursor.execute(sqlReceipt)
        monthlySalesData = mycursor.fetchall()
        if len(monthlySalesData) != 0:
            for data in monthlySalesData:
                # DocDate  = data['DocDate']
                Month    = data['Month']
                Year     = data['Year']
                DocTotal = data['DocTotal']
                finaldataSet[Month-4]['MonthlySales'] = round(float(DocTotal), 2)
                finaldataSet[Month-4]['Year'] = Year

        return Response({"message":"Successful","status":200, "data":finaldataSet})
    except Exception as e:
        return Response({"message":str(e),"status":201,"Model": "Items" ,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def monthly_receipts_chart(request):
    try:
        print(request.data)
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        SalesPersonCode = request.data['SalesPersonCode']
        zones = getZoneByEmployee(SalesPersonCode)
        zonesStr = "','".join(zones)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        fromToDate = ""
        if str(FromDate) != "":
            fromToDate = f"AND INVPay.DocDate >= '{FromDate}' AND INVPay.DocDate <= '{ToDate}'"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        finaldataSet = getMonthlyReportFromate(FromDate)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        sqlReceipt = f"""
            SELECT
                INVPay.DocDate as DocDate,
                MONTH(INVPay.DocDate) as Month,
                YEAR(INVPay.DocDate) as Year,
                IFNULL(SUM(INVPay.TransferSum), 0) AS `TransferSum`
            FROM BusinessPartner_businesspartner BP
                LEFT JOIN Invoice_incomingpayments INVPay ON INVPay.CardCode = BP.CardCode
            WHERE 
                INVPay.JournalRemarks != 'Canceled'
                AND BP.U_U_UTL_Zone IN('{zonesStr}')
                {fromToDate}
            GROUP BY MONTH(INVPay.DocDate)
        """
        print(sqlReceipt)
        mycursor.execute(sqlReceipt)
        monthlySalesData = mycursor.fetchall()
        if len(monthlySalesData) != 0:
            for data in monthlySalesData:
                # DocDate  = data['DocDate']
                Month    = data['Month']
                Year     = data['Year']
                TransferSum = data['TransferSum']
                finaldataSet[Month-4]['MonthlySales'] = round(float(TransferSum), 2)
                finaldataSet[Month-4]['Year'] = Year

        return Response({"message":"Successful","status":200, "data":finaldataSet})
    except Exception as e:
        return Response({"message":str(e),"status":201,"Model": "Items" ,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def monthly_purchase_receipts_chart(request):
    try:
        print(request.data)
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        SalesPersonCode = request.data['SalesPersonCode']
        zones = getZoneByEmployee(SalesPersonCode)
        zonesStr = "','".join(zones)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        fromToDate = ""
        if str(FromDate) != "":
            fromToDate = f"AND INVPay.DocDate >= '{FromDate}' AND INVPay.DocDate <= '{ToDate}'"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        finaldataSet = getMonthlyReportFromate(FromDate)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        sqlReceipt = f"""
            SELECT
                INVPay.DocDate as DocDate,
                MONTH(INVPay.DocDate) as Month,
                YEAR(INVPay.DocDate) as Year,
                IFNULL(SUM(INVPay.TransferSum), 0) AS `TransferSum`
            FROM BusinessPartner_businesspartner BP
                LEFT JOIN PurchaseInvoices_vendorpayments INVPay ON INVPay.CardCode = BP.CardCode
            WHERE 
                INVPay.JournalRemarks != 'Canceled'
                AND BP.U_U_UTL_Zone IN('{zonesStr}')
                {fromToDate}
            GROUP BY MONTH(INVPay.DocDate)
        """
        print(sqlReceipt)
        mycursor.execute(sqlReceipt)
        monthlySalesData = mycursor.fetchall()
        if len(monthlySalesData) != 0:
            for data in monthlySalesData:
                # DocDate  = data['DocDate']
                Month    = data['Month']
                Year     = data['Year']
                TransferSum = data['TransferSum']
                finaldataSet[Month-4]['MonthlySales'] = round(float(TransferSum), 2)
                finaldataSet[Month-4]['Year'] = Year

        return Response({"message":"Successful","status":200, "data":finaldataSet})
    except Exception as e:
        return Response({"message":str(e),"status":201,"Model": "Items" ,"data":[]})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# function to getMonthlyReportFromate
def getMonthlyReportFromate(date):
    dateArr = date.split('-')
    monSales = [
            {
                "MonthlySales": 0,
                "FinanYr": str(dateArr[0]),
                "Month": str("Apr"),
                "Year": int(dateArr[0])
            },
            {
                "MonthlySales": 0,
                "FinanYr": str(dateArr[0]),
                "Month": str("May"),
                "Year": int(dateArr[0])
            },
            {
                "MonthlySales": 0,
                "FinanYr": str(dateArr[0]),
                "Month": str("Jun"),
                "Year": int(dateArr[0])
            },
            {
                "MonthlySales": 0,
                "FinanYr": str(dateArr[0]),
                "Month": str("Jul"),
                "Year": int(dateArr[0])
            },
            {
                "MonthlySales": 0,
                "FinanYr": str(dateArr[0]),
                "Month": str("Aug"),
                "Year": int(dateArr[0])
            },
            {
                "MonthlySales": 0,
                "FinanYr": str(dateArr[0]),
                "Month": str("Sep"),
                "Year": int(dateArr[0])
            },
            {
                "MonthlySales": 0,
                "FinanYr": str(dateArr[0]),
                "Month": str("Oct"),
                "Year": int(dateArr[0])
            },
            {
                "MonthlySales": 0,
                "FinanYr": str(dateArr[0]),
                "Month": str("Nov"),
                "Year": int(dateArr[0])
            },
            {
                "MonthlySales": 0,
                "FinanYr": str(dateArr[0]),
                "Month": str("Dec"),
                "Year": int(dateArr[0])
            },
            {
                "MonthlySales": 0,
                "FinanYr": str(dateArr[0]),
                "Month": str("Jan"),
                "Year": int(dateArr[0])+1
            },
            {
                "MonthlySales": 0,
                "FinanYr": str(dateArr[0]),
                "Month": str("Feb"),
                "Year": int(dateArr[0])+1
            },
            {
                "MonthlySales": 0,
                "FinanYr": str(dateArr[0]),
                "Month": str("Mar"),
                "Year": int(dateArr[0])+1
            },     
        ]
    return monSales
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
import calendar
def first_last_dates_of_month(year, month_number):
    # Ensure the month_number is between 1 and 12
    if month_number < 1 or month_number > 12:
        raise ValueError("Month number must be between 1 and 12")

    # Find the last day of the given month
    last_day = calendar.monthrange(year, month_number)[1]

    # First day of the month
    first_date = f"{year}-{month_number:02d}-01"
    
    # Last day of the month
    last_date = f"{year}-{month_number:02d}-{last_day}"

    return first_date, last_date

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# function to getMonthlyReportFromate
def getMonthlyChart(year):
    monthsList = [
        {
            "month": 4,
            "year": year,
        },
        {
            "month": 5,
            "year": year,
        },
        {
            "month": 6,
            "year": year,
        },
        {
            "month": 7,
            "year": year,
        },
        {
            "month": 8,
            "year": year,
        },
        {
            "month": 9,
            "year": year,
        },
        {
            "month": 10,
            "year": year,
        },
        {
            "month": 11,
            "year": year,
        },
        {
            "month": 12,
            "year": year,
        },
        {
            "month": 1,
            "year": int(year) + 1,
        },
        {
            "month": 2,
            "year": int(year) + 1,
        },
        {
            "month": 3,
            "year": int(year) + 1,
        }
    ]
    return monthsList
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
data_arr = [
	{
		"id": 1,
		"TotalDue": 0,
		"OverDueDaysGroup": "0-30",
		"OverDueDaysGroup2": "30"
	},
	{
		"id": 2,
		"TotalDue": 0,
		"OverDueDaysGroup": "31-45",
		"OverDueDaysGroup2": "45"
	},
	{
		"id": 3,
		"TotalDue": 0,
		"OverDueDaysGroup": "46-60",
		"OverDueDaysGroup2": "60"
	},
	{
		"id": 4,
		"TotalDue": 0,
		"OverDueDaysGroup": "61-90",
		"OverDueDaysGroup2": "90"
	},
	{
		"id": 5,
		"TotalDue": 0,
		"OverDueDaysGroup": ">90",
		"OverDueDaysGroup2": "90+"
	}
]

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def verify_distributor(request):
    try:
        print("request data  :", request.data)
        mobile = request.data['mobile']
        if BusinessPartner.objects.filter(Phone1=mobile, CardType = 'cSupplier').exists():
            bp_obj = BusinessPartner.objects.filter(Phone1=mobile, CardType = 'cSupplier').first()
            bp_ser = BusinessPartnerSerializer(bp_obj)
            return Response({"message":"Successful","status":200,"data":[bp_ser.data], "errors":""})
        else:
            return Response({"message":"Not Found","status":400,"data":[], "errors":"Distributor does not exists"})
    except Exception as e:
        return Response({"message":"Unsuccess","status":500,"data":[], "errors":str(e)})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>