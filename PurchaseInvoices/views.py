from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from BusinessPartner.models import BPBranch, BPEmployee, BusinessPartnerGroups
from BusinessPartner.serializers import BPEmployeeSerializer

from Employee.serializers import EmployeeSerializer
from PaymentTermsTypes.models import PaymentTermsTypes
from PaymentTermsTypes.serializers import PaymentTermsTypesSerializer
from BusinessPartner.models import BusinessPartner
from Invoice.models import CreditNotes
from BusinessPartner.serializers import BPAddressesSerializer
from BusinessPartner.models import BPAddresses
from Company.models import Branch
from global_methods import employeeViewAccess, getAllReportingToIds, getZoneByEmployee
from .models import *
from Employee.models import Employee

from django.db.models import Q

import requests, json

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import *
from rest_framework.parsers import JSONParser

from pytz import timezone
from datetime import datetime as dt

import datetime

from django.db.models import Q
# import setting file
from django.conf import settings
import mysql.connector

from urllib.parse import unquote

date = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d')
yearmonth = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m')
time = dt.now(timezone("Asia/Kolkata")).strftime('%H:%M %p')


# Create your views here.  
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Invoice All API
@api_view(["POST"])
def all_filter(request):
    try:
        SalesPersonCode = request.data['SalesPersonCode']
        if Employee.objects.filter(SalesEmployeeCode = SalesPersonCode).exists():
            empList = getAllReportingToIds(SalesPersonCode)
            quot_obj = PurchaseInvoices.objects.filter(SalesPersonCode__in=empList).order_by("-id")
            # allqt = InvoiceShow(quot_obj)
            allqt = showInvoice(quot_obj)
            return Response({"message": "Success","status": 200,"data":allqt})
        else:
            return Response({"message": "Invalid SalesPersonCode","status": 201,"data":[]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Invoice All API
@api_view(["POST"])
def all_filter_pagination(request):
    try:
        SalesPersonCode = request.data['SalesPersonCode']
        PageNo = int(request.data['PageNo'])
        MaxSize = request.data['MaxSize']
        TotalInvoice = 0
        if Employee.objects.filter(SalesEmployeeCode = SalesPersonCode).exists():
            empList = getAllReportingToIds(SalesPersonCode)
            quot_obj = PurchaseInvoices.objects.filter(SalesPersonCode__in=empList).order_by("-id")
            TotalInvoice = len(quot_obj)
            if MaxSize != "All":
                size = int(MaxSize)
                endWith = (PageNo * size)
                startWith = (endWith - size)
                quot_obj = quot_obj[startWith:endWith]
            allqt = showInvoice(quot_obj)
            return Response({"message": "Success","status": 200,"data":allqt, "TotalInvoice": TotalInvoice})
        else:
            return Response({"message": "Invalid SalesPersonCode","status": 201,"data":[]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Invoice All API
@api_view(["GET"])
def all(request):
    try:
        invoice_obj = PurchaseInvoices.objects.all().order_by("-id")
        result = showInvoice(invoice_obj)
        return Response({"message": "Success","status": 200,"data":result})
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Invoice One API
@api_view(["POST"])
def one(request):
    try:
        id=request.data['id'] 
        invoice_obj = PurchaseInvoices.objects.filter(DocEntry = id)
        # invoice_obj = PurchaseInvoices.objects.filter(pk=id)
        result = showInvoice(invoice_obj)
        return Response({"message": "Success","status": 200,"data":result})
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})
    

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Invoice delete
@api_view(['POST'])
def delete(request):
    fetchid=request.data['id']
    try:
        fetchdata=PurchaseInvoices.objects.filter(pk=fetchid).delete()
        return Response({"message":"successful","status":"200","data":[]})        
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})
     
     
# to get invoice contact person details and salesEmployeeDetails
def showInvoice(objs):
    allInvoice = [];
    for obj in objs:
        cpcType = obj.ContactPersonCode
        salesType = obj.SalesPersonCode
        invId = obj.id
        DocumentStatus = obj.DocumentStatus
        DiscountPercent = obj.DiscountPercent
        CardCode = obj.CardCode
        cpcjson = PurchaseInvoicesSerializer(obj)
        finalCPCData = json.loads(json.dumps(cpcjson.data))
        BaseEntry = 0
        paymentType = obj.PaymentGroupCode
       
        ################################addedd################################
        BPLID = obj.BPLID
        if Branch.objects.filter(BPLId=BPLID).exists():
            branch_obj = Branch.objects.filter(BPLId=BPLID).first()
            finalCPCData["BPLName"] = branch_obj.BPLName
            finalCPCData["Address"] = branch_obj.Address
            finalCPCData["State"] = branch_obj.State
            finalCPCData["TaxIdNum"] = branch_obj.TaxIdNum
            finalCPCData["Branch_GSTIN"] = branch_obj.FederalTaxID
        else:
            finalCPCData["BPLName"] = ""
            finalCPCData["Address"] = ""
            finalCPCData["State"] = ""
            finalCPCData["TaxIdNum"] = ""
            finalCPCData["Branch_GSTIN"] = ""
        ################################addedd################################
        bp_code = obj.CardCode
        if BusinessPartner.objects.filter(CardCode=bp_code).exists():
            bp_obj = BusinessPartner.objects.filter(CardCode=bp_code).first()
            finalCPCData["EmailAddress"] = bp_obj.EmailAddress
        else:
            finalCPCData["EmailAddress"] = ""
        ############################added#####################################
        
        ################################addedd################################
        if BPAddresses.objects.filter(BPCode=bp_code).exists():
            bp_obj = BPAddresses.objects.filter(BPCode=bp_code)
            bpAddrson = BPAddressesSerializer(bp_obj, many=True)
            finalCPCData["BPAddresses"] = bpAddrson.data
        else:
            finalCPCData["BPAddresses"] = []
        ############################added#####################################

        ################################addedd################################
        if BPEmployee.objects.filter(InternalCode = cpcType).exists():
            cpcTypeObj = BPEmployee.objects.filter(InternalCode = cpcType).values("id","FirstName","E_Mail", "MobilePhone")  #updated by millan on 15-09-2022
            cpcTypejson = BPEmployeeSerializer(cpcTypeObj, many = True)
            finalCPCData['ContactPersonCode']=json.loads(json.dumps(cpcTypejson.data))
        else:
            finalCPCData['ContactPersonCode'] = []
        ################################addedd################################
            
        ################################addedd################################
        if Employee.objects.filter(SalesEmployeeCode = salesType).exists():
            salesTypeObj = Employee.objects.filter(SalesEmployeeCode = salesType).values("id", "SalesEmployeeCode", "SalesEmployeeName", "Email", "Mobile")
            salesTypejson = EmployeeSerializer(salesTypeObj, many=True)
            finalCPCData['SalesPersonCode'] = json.loads(json.dumps(salesTypejson.data))
        else:
            finalCPCData['SalesPersonCode'] = []
        ################################addedd################################
            
        ################################addedd################################
        if AddressExtension.objects.filter(InvoiceID = invId).exists():
            addrObj = AddressExtension.objects.filter(InvoiceID = invId)
            addrjson = AddressExtensionSerializer(addrObj, many=True)
            finalCPCData['AddressExtension'] = json.loads(json.dumps(addrjson.data))
        else:
            finalCPCData['AddressExtension'] = []
        ################################addedd################################
            
        ################################addedd################################
        BaseTotal = 0
        if DocumentLines.objects.filter(InvoiceID=invId).exists():
            linesobj = DocumentLines.objects.filter(InvoiceID=invId)
            lines_json = DocumentLinesSerializer(linesobj, many=True)
            BaseEntry = linesobj[0].BaseEntry
            finalCPCData['DocumentLines'] = json.loads(json.dumps(lines_json.data))
            for itObjs in linesobj:
                LineTotal = float(itObjs.LineTotal)
                BaseTotal = BaseTotal + LineTotal
        else:
            finalCPCData['DocumentLines'] = []
        ################################addedd################################
            
        ################################addedd################################
        if PaymentTermsTypes.objects.filter(GroupNumber = paymentType).exists():
            paymentTypeObj = PaymentTermsTypes.objects.filter(GroupNumber = paymentType)
            paymentjson = PaymentTermsTypesSerializer(paymentTypeObj, many = True)
            finalCPCData['PayTermsGrpCode'] = json.loads(json.dumps(paymentjson.data))
        else:
            finalCPCData['PayTermsGrpCode'] = []
        ################################addedd################################
            
        ################################addedd################################
        NetTotal = 0
        disAmt = 0
        if BaseTotal != 0:
            if str(DiscountPercent) != 0.0:
                print(BaseTotal,  DiscountPercent)
                disAmt = (float(BaseTotal) * float(DiscountPercent)) / 100
        NetTotal = round(float(BaseTotal - disAmt), 2)
        finalCPCData['NetTotal'] = NetTotal
        ################################addedd################################
            
        ################################addedd################################
        PaymentStatus = "Unpaid"
        if DocumentStatus == "bost_Close":
            PaymentStatus = "Paid"
        elif VendorPaymentsInvoices.objects.filter(InvoiceDocEntry = invId).exists():
            PaymentStatus = "Partially Paid"
        finalCPCData['PaymentStatus'] = PaymentStatus
        ################################addedd################################
            
        ################################addedd################################
        allInvoice.append(finalCPCData)
    return allInvoice

# To get CreditNote contact
def showCreditNote(objs):
    allInvoice = [];
    for obj in objs:
        cpcType = obj.ContactPersonCode
        salesType = obj.SalesPersonCode
        creditNoteId = obj.id
        DocumentStatus = obj.DocumentStatus
        DiscountPercent = obj.DiscountPercent
        CardCode = obj.CardCode
        cpcjson = PurchaseCreditNotesSerializer(obj)
        finalCPCData = json.loads(json.dumps(cpcjson.data))
        BaseEntry = 0
        paymentType = obj.PaymentGroupCode
       
        ##################################
        # ########### Branch #############
        # ################################
        BPLID = obj.BPLID
        if Branch.objects.filter(BPLId=BPLID).exists():
            branch_obj = Branch.objects.filter(BPLId=BPLID).first()
            finalCPCData["BPLName"] = branch_obj.BPLName
            finalCPCData["Address"] = branch_obj.Address
            finalCPCData["State"] = branch_obj.State
            finalCPCData["TaxIdNum"] = branch_obj.TaxIdNum
            finalCPCData["Branch_GSTIN"] = branch_obj.FederalTaxID
        else:
            finalCPCData["BPLName"] = ""
            finalCPCData["Address"] = ""
            finalCPCData["State"] = ""
            finalCPCData["TaxIdNum"] = ""
            finalCPCData["Branch_GSTIN"] = ""
        ################################addedd################################

        ################################addedd################################
        bp_code = obj.CardCode
        if BusinessPartner.objects.filter(CardCode=bp_code).exists():
            bp_obj = BusinessPartner.objects.filter(CardCode=bp_code).first()
            finalCPCData["EmailAddress"] = bp_obj.EmailAddress
        else:
            finalCPCData["EmailAddress"] = ""
            
        ################################addedd################################
        if BPAddresses.objects.filter(BPCode=bp_code).exists():
            bp_obj = BPAddresses.objects.filter(BPCode=bp_code)
            bpAddrson = BPAddressesSerializer(bp_obj, many=True)
            finalCPCData["BPAddresses"] = bpAddrson.data
        else:
            finalCPCData["BPAddresses"] = []
        ############################added#####################################

        ######################################################################

        if BPEmployee.objects.filter(InternalCode = cpcType).exists():
            cpcTypeObj = BPEmployee.objects.filter(InternalCode = cpcType).values("id","FirstName","E_Mail", "MobilePhone")  #updated by millan on 15-09-2022
            cpcTypejson = BPEmployeeSerializer(cpcTypeObj, many = True)
            finalCPCData['ContactPersonCode']=json.loads(json.dumps(cpcTypejson.data))
        else:
            finalCPCData['ContactPersonCode'] = []
            
        if Employee.objects.filter(SalesEmployeeCode = salesType).exists():
            salesTypeObj = Employee.objects.filter(SalesEmployeeCode = salesType).values("id", "SalesEmployeeCode", "SalesEmployeeName", "Email", "Mobile")
            salesTypejson = EmployeeSerializer(salesTypeObj, many=True)
            finalCPCData['SalesPersonCode'] = json.loads(json.dumps(salesTypejson.data))
        else:
            finalCPCData['SalesPersonCode'] = []
            
        if CreditNotesAddressExtension.objects.filter(CreditNotesId = creditNoteId).exists():
            addrObj = CreditNotesAddressExtension.objects.filter(CreditNotesId = creditNoteId)
            addrjson = CreditNotesAddressExtensionSerializer(addrObj, many=True)
            finalCPCData['AddressExtension'] = json.loads(json.dumps(addrjson.data))
        else:
            finalCPCData['AddressExtension'] = []
        
        BaseTotal = 0
        if CreditNotesDocumentLines.objects.filter(CreditNotesId=creditNoteId).exists():
            linesobj = CreditNotesDocumentLines.objects.filter(CreditNotesId=creditNoteId)
            lines_json = CreditNotesDocumentLinesSerializer(linesobj, many=True)
            # BaseEntry = linesobj[0].BaseEntry
            finalCPCData['DocumentLines'] = json.loads(json.dumps(lines_json.data))
            for itObjs in linesobj:
                LineTotal = float(itObjs.LineTotal)
                BaseTotal = BaseTotal + LineTotal
        else:
            finalCPCData['DocumentLines'] = []
            
        if PaymentTermsTypes.objects.filter(GroupNumber = paymentType).exists():
            paymentTypeObj = PaymentTermsTypes.objects.filter(GroupNumber = paymentType)
            paymentjson = PaymentTermsTypesSerializer(paymentTypeObj, many = True)
            finalCPCData['PayTermsGrpCode'] = json.loads(json.dumps(paymentjson.data))
        else:
            finalCPCData['PayTermsGrpCode'] = []

        NetTotal = 0
        disAmt = 0
        if BaseTotal != 0:
            if str(DiscountPercent) != 0.0:
                print(BaseTotal,  DiscountPercent)
                disAmt = (float(BaseTotal) * float(DiscountPercent)) / 100
        NetTotal = round(float(BaseTotal - disAmt), 2)
        finalCPCData['NetTotal'] = NetTotal

        allInvoice.append(finalCPCData)
    return allInvoice

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# #######################################################################################################################
# #######################################################################################################################
# #######################################################################################################################
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def one_receipt(request):
    try:
        ReceiptId   = request.data['ReceiptId']
        paymentObj  = VendorPayments.objects.filter(DocEntry = ReceiptId)
        # paymentObj = VendorPayments.objects.filter(pk=ReceiptId)
        result = showIncomingPayments(paymentObj)
        return Response({"message":"successful","status":"200","data":result})    
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>    
@api_view(['POST'])
def bp_wise_receipt(request):
    try:
        CardCode = request.data['CardCode']
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        if BusinessPartner.objects.filter(CardCode = CardCode).exists():
            paymentObj = VendorPayments.objects.filter(CardCode = CardCode)
            
            if 'PageNo' in request.data:
                PageNo = int(request.data['PageNo'])
                MaxSize = request.data['MaxSize']
                if MaxSize != "All":
                    size = int(MaxSize)
                    endWith = (PageNo * size)
                    startWith = (endWith - size)
                    paymentObj = paymentObj[startWith:endWith]

            result = showIncomingPayments(paymentObj)
            return Response({"message":"successful","status":"200","data":result})
        else:
            return Response({"message":"Invalid bp Code?","status":"201","data":[]})      
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>    
@api_view(['POST'])
def ap_incoming_payments(request):
    try:
        InvoiceId=request.data['id']
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        if PurchaseInvoices.objects.filter(pk=InvoiceId).exists():
            invObj = PurchaseInvoices.objects.filter(pk=InvoiceId).first()
            incomingPayObj = []
            result = []
            if str(FromDate) !="":
                
                incomingPayIds = VendorPaymentsInvoices.objects.filter(InvoiceDocEntry = invObj.DocEntry, DocDate__gte = FromDate, DocDate__lte = ToDate).values_list('VendorPaymentsId', flat=True)
                incomingPayObj = VendorPayments.objects.filter(pk__in = incomingPayIds)
                result = showIncomingPayments(incomingPayObj)
            else:
                incomingPayIds = VendorPaymentsInvoices.objects.filter(InvoiceDocEntry = invObj.DocEntry).values_list('VendorPaymentsId', flat=True)
                incomingPayObj = VendorPayments.objects.filter(pk__in = incomingPayIds)
                result = showIncomingPayments(incomingPayObj)
                
            # incomingPayJson = IncomingPaymentsSerializer(incomingPayObj, many=True)
            return Response({"message":"successful","status":"200","data":result})
        else:
            return Response({"message":"Invalid Invoice Id?","status":"201","data":[]})      
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def all_ap_incoming_payments(request):
    try:
        SalesEmployeeCode = request.data['SalesEmployeeCode']
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        allEmp = getAllReportingToIds(SalesEmployeeCode)
        docEntrys = list(PurchaseInvoices.objects.filter(SalesPersonCode__in = allEmp).values_list('DocEntry', flat=True))
        if 'PageNo' in request.data:
            PageNo = int(request.data['PageNo'])
            MaxSize = request.data['MaxSize']
            if MaxSize != "All":
                size = int(MaxSize)
                endWith = (PageNo * size)
                startWith = (endWith - size)
                docEntrys = docEntrys[startWith:endWith]

        totalSalesList = 0
        allPaymentsList = 0

        if str(FromDate) != "":
            totalSalesList = list(PurchaseInvoices.objects.filter(SalesPersonCode__in = allEmp, DocDate__gte = FromDate, DocDate__lte = ToDate).values_list('DocTotal', flat=True))
            allPaymentsList = VendorPaymentsInvoices.objects.filter(InvoiceDocEntry__in = docEntrys, DocDate__gte = FromDate, DocDate__lte = ToDate).values_list('SumApplied', flat=True)
            
        else:
            totalSalesList = list(PurchaseInvoices.objects.filter(SalesPersonCode__in = allEmp).values_list('DocTotal', flat=True))
            allPaymentsList = VendorPaymentsInvoices.objects.filter(InvoiceDocEntry__in = docEntrys).values_list('SumApplied', flat=True)
            
        totalSales = 0
        allPayment = 0

        for item in totalSalesList:
            totalSales += float(item)

        for item in allPaymentsList:
            allPayment += float(item)

        # incomingPayJson = IncomallPaymentingPaymentsSerializer(incomingPayObj, many=True)
        context = {
            "TotalSales": totalSales,
            "TotalReceivePayment": allPayment,
            "DifferenceAmount": float(float(totalSales) - float(allPayment))
        }
        return Response({"message":"successful","status":"200","data":[context]})
        # else:
        #     return Response({"message":"Invalid Invoice Id?","status":"201","data":[]})      
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# bp list with total purchase
@api_view(['POST'])
def bp_ap_credit_notes(request):
    try:
        CardCode = request.data['CardCode']
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        
        dataContext = []
        docEntrys = []
        totalSalesByBp = 0
        allPaymentsList = 0

        BPData = []
        if BusinessPartner.objects.filter(CardCode = CardCode).exists():
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            bpobj = BusinessPartner.objects.filter(CardCode = CardCode).first()
            LinkedBusinessPartner = bpobj.LinkedBusinessPartner
            PayTermsGrpCode = bpobj.PayTermsGrpCode
            CreditLimit = bpobj.CreditLimit
            ptgcObj = PaymentTermsTypes.objects.filter(GroupNumber = PayTermsGrpCode).first()
            creditLimitDayes = ptgcObj.PaymentTermsGroupName
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
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

            creditNoteList = []
            if str(FromDate) != "":
                creditNoteList = PurchaseCreditNotes.objects.filter(CardCode = LinkedBusinessPartner, DocDate__gte = FromDate, DocDate__lte = ToDate)
            else:
                creditNoteList = PurchaseCreditNotes.objects.filter(CardCode = LinkedBusinessPartner)

            if len(creditNoteList) != 0:
                if 'PageNo' in request.data:
                    PageNo = int(request.data['PageNo'])
                    MaxSize = request.data['MaxSize']
                    if MaxSize != "All":
                        size = int(MaxSize)
                        endWith = (PageNo * size)
                        startWith = (endWith - size)
                        creditNoteList = creditNoteList[startWith:endWith]
                    
                for creditNote in creditNoteList:
                    docEntrys.append(creditNote.InvoiceDocEntry)
                    DocTotal = float(creditNote.DocTotal)

                    allPaymentsList = allPaymentsList + DocTotal

                    bpData = {
                        "OrderId": creditNote.id,
                        "DocEntry": creditNote.DocEntry,
                        "OrderAmount": DocTotal,
                        "CreateDate": creditNote.DocDate,
                        "Comments": unquote(creditNote.Comments)
                    }                    
                    dataContext.append(bpData)
                    totalSalesByBp = totalSalesByBp + float(DocTotal)

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            bpContext = {
                "CardName": bpobj.CardName,
                "CardCode": bpobj.CardCode,
                "EmailAddress": bpobj.EmailAddress,
                "Phone1": bpobj.Phone1,
                "GSTIN": GSTIN,
                "BPAddress": BPAddress,
                "GroupName": GroupName,
                "CreditLimit": CreditLimit,
                "CreditLimitDayes": creditLimitDayes
            }
            BPData.append(bpContext)
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        else:
            return Response({"message": "Invalid CardCode","status": 201, "data":[], "TotalSales": 0})

        TotalSales = round(totalSalesByBp, 2)
        TotalReceivePayment = round(allPaymentsList, 2)
        DifferenceAmount = round(float(float(totalSalesByBp) - float(allPaymentsList)), 2)

        return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": TotalSales, "TotalReceivePayment": TotalReceivePayment, "DifferenceAmount": DifferenceAmount, "BPData": BPData})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def ap_credit_notes(request):
    try:
        InvoiceId=request.data['id']
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        if PurchaseInvoices.objects.filter(pk=InvoiceId).exists():
            invObj = PurchaseInvoices.objects.filter(pk=InvoiceId).first()
            incomingPayObj = []
            if str(FromDate) != "":
                incomingPayObj = PurchaseCreditNotes.objects.filter(InvoiceDocEntry = invObj.DocEntry, DocDate__gte = FromDate, DocDate__lte = ToDate)
            else:
                incomingPayObj = PurchaseCreditNotes.objects.filter(InvoiceDocEntry = invObj.DocEntry)

            incomingPayJson = PurchaseCreditNotesSerializer(incomingPayObj, many=True)
            return Response({"message":"successful","status":"200","data":incomingPayJson.data})
        else:
            return Response({"message":"Invalid Invoice Id?","status":"201","data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def ap_credit_notes_one(request):
    try:
        id = request.data['id']
        credit_objs = PurchaseCreditNotes.objects.filter(DocEntry = id)
        # credit_objs = PurchaseCreditNotes.objects.filter(pk=id)
        CreditNoteList = showCreditNote(credit_objs)
        return Response({"message":"successful","status":"200","data":CreditNoteList})
        # if PurchaseCreditNotes.objects.filter(pk=id).exists():
        #     credit_objs = PurchaseCreditNotes.objects.filter(pk=id)
        #     CreditNoteList = showCreditNote(credit_objs)
        #     return Response({"message":"successful","status":"200","data":CreditNoteList})
        # else:
        #     return Response({"message":"Invalid Credit Note Id?","status":"201","data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def showIncomingPayments(objs):
    allIncomingPayments = []
    for obj in objs:
        paymentObj = VendorPaymentsSerializer(obj, many=False)
        finalIncomingPayment = json.loads(json.dumps(paymentObj.data))
        ################################addedd################################
        BPLID = obj.BPLID
        if Branch.objects.filter(BPLId=BPLID).exists():
            branch_obj = Branch.objects.filter(BPLId=BPLID).first()
            finalIncomingPayment["BPLName"] = branch_obj.BPLName
            finalIncomingPayment["Address"] = unquote(branch_obj.Address)
            finalIncomingPayment["State"] = branch_obj.State
            finalIncomingPayment["TaxIdNum"] = branch_obj.TaxIdNum
        else:
            finalIncomingPayment["BPLName"] = ""
            finalIncomingPayment["Address"] = ""
            finalIncomingPayment["State"] = ""
            finalIncomingPayment["TaxIdNum"] = ""
        ################################addedd################################
        if VendorPaymentsInvoices.objects.filter(VendorPaymentsId = obj.id).exists():
            invObjs = VendorPaymentsInvoices.objects.filter(VendorPaymentsId = obj.id)
            invJson = VendorPaymentsInvoicesSerializer(invObjs, many=True)
            finalIncomingPayment['IncomingPaymentInvoices'] = invJson.data
        else:
            finalIncomingPayment['IncomingPaymentInvoices'] = []
        allIncomingPayments.append(finalIncomingPayment)

    return allIncomingPayments
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# bp list with total purchase
@api_view(['POST'])
def purchase_ledger_dashboard_count(request):
    try:
        print("purchase_ledger_dashboard_count", request.data)
        SalesPersonCode = request.data['SalesPersonCode']
        Filter      = request.data['Filter']
        Code        = request.data['Code']
        SalesType   = request.data['Type']
        FromDate    = request.data['FromDate']
        ToDate      = request.data['ToDate']
        SearchText  = request.data['SearchText']
        DueDaysGroup = request.data['DueDaysGroup']
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        if Code!="":
            zonesStr = str(Code)
        else:
            zones = getZoneByEmployee(SalesPersonCode)
            zonesStr = "','".join(zones)
        # zones = getZoneByEmployee(SalesPersonCode)
        # zonesStr = "','".join(zones)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        overDuesQuery = ""
        if DueDaysGroup != "":
            overDuesQuery = f"AND DueDaysGroup = {DueDaysGroup}"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # groupByQuery = "GroupCode"
        SearchQuery = ""
        fieldsNamesForQuery = "bp.CardCode as GroupCode, bp.CardName as GroupName,"
        if str(Filter).lower() == 'group':
            # groupByQuery = "GroupCode"
            fieldsNamesForQuery = "bpgroup.Code as GroupCode, bpgroup.Name as GroupName,"
            if str(SearchText) != '':
                SearchQuery = f"AND (bpgroup.Code like '%%{SearchText}%%')"
        elif str(Filter).lower() == 'zone':
            # groupByQuery = "GroupCode"
            fieldsNamesForQuery = "bp.U_U_UTL_Zone as GroupCode, bp.U_U_UTL_Zone as GroupName,"
            if str(SearchText) != '':
                SearchQuery = f"AND (bp.U_U_UTL_Zone like '%%{SearchText}%%')"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        fromToDate = ""
        receiptfromToDate = ""
        ordfromToDate = ""
        if str(FromDate) != "":
            fromToDate = f"AND inv.DocDate >= '{FromDate}' AND inv.DocDate <= '{ToDate}'"
            receiptfromToDate = f"AND INVPay.DocDate >= '{FromDate}' AND INVPay.DocDate <= '{ToDate}'"
            ordfromToDate = f"AND ord.DocDate >= '{FromDate}' AND ord.DocDate <= '{ToDate}'"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        sqlQuery = ""
        if str(SalesType).lower() == "gross":
            sqlQuery = f"""
                SELECT
                    {fieldsNamesForQuery}
                    IFNULL(SUM(inv.DocTotal), 0) AS `DocTotal`,
                    IFNULL(SUM(inv.PaidToDateSys), 0) AS `PaidToDateSys`,
                    IFNULL(SUM(inv.DocTotal - inv.PaidToDateSys), 0) AS `PendingTotal`
                FROM BusinessPartner_businesspartner bp
                INNER JOIN BusinessPartner_businesspartnergroups bpgroup ON bpgroup.Code = bp.GroupCode
                LEFT JOIN PurchaseInvoices_purchaseinvoices inv ON bp.CardCode = inv.CardCode
                WHERE 
                    inv.CancelStatus = 'csNo'
                    AND bp.U_U_UTL_Zone IN('{zonesStr}')
                    {SearchQuery}
                    {fromToDate}
            """
        else:
            sqlQuery = f"""
                SELECT
                    {fieldsNamesForQuery}
                    IFNULL(SUM(A.DocTotal), 0) AS 'DocTotal',
                    IFNULL(SUM(A.NetTotal), 0) AS 'NetTotal',
                    IFNULL(SUM(A.PaidToDateSys), 0) AS `PaidToDateSys`,
                    IFNULL(SUM(A.DocTotal - A.PaidToDateSys), 0) AS `PendingTotal`
                FROM BusinessPartner_businesspartner bp
                INNER JOIN BusinessPartner_businesspartnergroups bpgroup ON bpgroup.Code = bp.GroupCode
                INNER JOIN (
                    SELECT
                        inv.CardCode,
                        inv.id,
                        inv.DocTotal,
                        inv.PaidToDateSys,
                        IFNULL(SUM(INVLine.LineTotal), 0) AS LineTotal,
                        IFNULL( SUM(CASE WHEN inv.DiscountPercent != 0.0 THEN INVLine.LineTotal - (INVLine.LineTotal * inv.DiscountPercent / 100) ELSE INVLine.LineTotal END), 0 ) AS NetTotal
                    FROM PurchaseInvoices_purchaseinvoices inv
                    LEFT JOIN PurchaseInvoices_documentlines INVLine ON INVLine.InvoiceID = inv.id
                    WHERE 
                        inv.CancelStatus = 'csNo'
                        {fromToDate}
                    GROUP BY inv.CardCode, inv.id
                ) A ON bp.CardCode = A.CardCode
                WHERE 
                    bp.U_U_UTL_Zone IN('{zonesStr}')
                    {SearchQuery}
            """

        print(sqlQuery)
        mycursor.execute(sqlQuery)
        groupData = mycursor.fetchall()
        TotalSales = 0
        TotalReceivePayment = 0
        PendingTotal = 0
        if len(groupData) > 0:
            TotalSales = groupData[0]['DocTotal']
            # TotalReceivePayment = groupData[0]['PaidToDateSys']
            PendingTotal = groupData[0]['PendingTotal']
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
                CardCodeArr = list(BusinessPartner.objects.filter(CardType = 'cSupplier', GroupCode = Code, U_U_UTL_Zone__in = zones).values_list("CardCode", flat=True))
            elif str(Filter).lower() == 'zone':
                CardCodeArr = list(BusinessPartner.objects.filter(CardType = 'cSupplier', U_U_UTL_Zone = Code).values_list("CardCode", flat=True))
            else:
                CardCodeArr = list(BusinessPartner.objects.filter(CardType = 'cSupplier', U_U_UTL_Zone__in = zones).values_list("CardCode", flat=True))

        CardCodeStr = "','".join(CardCodeArr)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # Total Receipt
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        TotalCreditNote = 0
        sqlAllReceipts = f"""
        SELECT
            bp.CardCode,
            bp.CardName,
            IFNULL(SUM(INVPay.TransferSum), 0) AS `TransferSum`
        FROM BusinessPartner_businesspartner bp
            LEFT JOIN PurchaseInvoices_vendorpayments INVPay ON INVPay.CardCode = bp.CardCode
        WHERE
            INVPay.JournalRemarks != 'Canceled'
            AND bp.U_U_UTL_Zone IN('{zonesStr}')
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
        sqlAllCreditNote = f"""SELECT bp.CardCode AS CardCode, bp.CardName AS CardName, IFNULL(SUM(A.DocTotal), 0) AS 'DocTotal', IFNULL(SUM(A.NetTotal), 0) AS 'NetTotal', IFNULL(SUM(A.PaidToDateSys),  0) AS `PaidToDateSys`, IFNULL( SUM(A.DocTotal - A.PaidToDateSys), 0 ) AS `PendingTotal` FROM BusinessPartner_businesspartner bp INNER JOIN BusinessPartner_businesspartnergroups bpgroup ON bpgroup.Code = bp.GroupCode INNER JOIN( SELECT inv.CardCode, inv.id, inv.DocTotal, inv.PaidToDateSys, IFNULL(SUM(INVLine.LineTotal), 0) AS LineTotal, IFNULL( SUM( CASE WHEN inv.DiscountPercent != 0.0 THEN INVLine.LineTotal - ( INVLine.LineTotal * inv.DiscountPercent / 100 ) ELSE INVLine.LineTotal END ), 0) AS NetTotal FROM PurchaseInvoices_purchasecreditnotes inv LEFT JOIN PurchaseInvoices_creditnotesdocumentlines INVLine ON INVLine.CreditNotesId = inv.id WHERE inv.CancelStatus = 'csNo' {fromToDate} GROUP BY inv.CardCode, inv.id ) A ON bp.CardCode = A.CardCode WHERE bp.U_U_UTL_Zone IN('{zonesStr}') """
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
                FROM PurchaseOrders_purchaseorders ord
                LEFT JOIN PurchaseOrders_documentlines ORDLine ON ORDLine.OrderID = ord.id
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
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# bp list with total purchase
@api_view(['POST'])
def filter_purchase_ledger_dashboard(request):
    try:
        print("filter_purchase_ledger_dashboard", request.data)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SalesPersonCode = request.data['SalesPersonCode']
        Filter      = request.data['Filter']
        SalesType   = request.data['Type']
        FromDate    = request.data['FromDate']
        ToDate      = request.data['ToDate']
        SearchText  = request.data['SearchText']
        OrderByName = request.data['OrderByName']
        OrderByAmt  = request.data['OrderByAmt']
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        zones = getZoneByEmployee(SalesPersonCode)
        zonesStr = "','".join(zones)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        orderby = "Order By GroupName asc"
        if str(OrderByName).lower() == 'a-z':
            orderby = "Order By GroupName asc"
        elif str(OrderByName).lower() == 'z-a':
            orderby = "Order By GroupName desc"
        elif str(OrderByAmt).lower() == 'asc':
            orderby = "Order By DocTotal asc"
        elif str(OrderByAmt).lower() == 'desc':
            orderby = "Order By DocTotal desc"
        # endIf
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        fromToDate = ""
        if str(FromDate) != "":
            fromToDate = f"AND inv.DocDate >= '{FromDate}' AND inv.DocDate <= '{ToDate}'"
        # endIf
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        limitQuery = ""
        if 'PageNo' in request.data:
            PageNo = int(request.data['PageNo'])
            MaxSize = request.data['MaxSize']
            if str(MaxSize).lower() != "all":   
                size = int(MaxSize)
                endWith = (PageNo * size)
                startWith = (endWith - size)
                limitQuery = f"Limit {startWith}, {MaxSize}"
        # endIf
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        groupByQuery = "bp.U_U_UTL_Zone"
        SearchQuery = ""
        fieldsNamesForQuery = "CardCode as GroupCode, CardName as GroupName,"
        if str(Filter).lower() == 'group':
            groupByQuery = "bpgroup.Code"
            fieldsNamesForQuery = "bpgroup.Code as GroupCode, bpgroup.Name as GroupName,"
            if str(SearchText) != '':
                SearchQuery = f"AND (bpgroup.Code like '%%{SearchText}%%')"
        elif str(Filter).lower() == 'zone':
            groupByQuery = "bp.U_U_UTL_Zone"
            fieldsNamesForQuery = "bp.U_U_UTL_Zone as GroupCode, bp.U_U_UTL_Zone as GroupName,"
            if str(SearchText) != '':
                SearchQuery = f"AND (bp.U_U_UTL_Zone like '%%{SearchText}%%')"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        sqlQuery = ""
        if str(SalesType).lower() == "gross":
            sqlQuery = f"""
                SELECT
                    {fieldsNamesForQuery}
                    IFNULL(SUM(inv.DocTotal), 0) AS `DocTotal`,
                    IFNULL(SUM(inv.PaidToDateSys), 0) AS `PaidToDateSys`,
                    IFNULL(SUM(inv.DocTotal - inv.PaidToDateSys), 0) AS `PendingTotal`
                FROM BusinessPartner_businesspartner bp
                INNER JOIN BusinessPartner_businesspartnergroups bpgroup ON bpgroup.Code = bp.GroupCode
                LEFT JOIN PurchaseInvoices_purchaseinvoices inv ON bp.CardCode = inv.CardCode
                WHERE 
                    inv.CancelStatus = 'csNo'
                    AND bp.U_U_UTL_Zone IN('{zonesStr}')
                    {SearchQuery}
                    {fromToDate}
                GROUP BY {groupByQuery} 
                {orderby}
                {limitQuery}
            """
        else:
            sqlQuery = f"""
                SELECT
                    {fieldsNamesForQuery}
                    IFNULL(SUM(A.DocTotal), 0) AS 'DocTotal',
                    IFNULL(SUM(A.NetTotal), 0) AS 'NetTotal',
                    IFNULL(SUM(A.PaidToDateSys), 0) AS `PaidToDateSys`,
                    IFNULL(SUM(A.DocTotal - A.PaidToDateSys), 0) AS `PendingTotal`
                FROM BusinessPartner_businesspartner bp
                INNER JOIN BusinessPartner_businesspartnergroups bpgroup ON bpgroup.Code = bp.GroupCode
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
                    FROM PurchaseInvoices_purchaseinvoices inv
                    LEFT JOIN PurchaseInvoices_documentlines INVLine ON INVLine.InvoiceID = inv.id
                    WHERE 
                        inv.CancelStatus = 'csNo'
                        {fromToDate}
                    GROUP BY inv.CardCode, inv.id
                ) A ON bp.CardCode = A.CardCode
                WHERE 
                    bp.U_U_UTL_Zone IN('{zonesStr}')
                    {SearchQuery}
                GROUP BY {groupByQuery}
                {limitQuery}
            """
        
        print(sqlQuery)
        mycursor.execute(sqlQuery)
        groupData = mycursor.fetchall()
        # return Response({"message": "Success","status": 200, "data":groupData})
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
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def purchase_ledger_dashboard(request):
    try:
        print("purchase_ledger_dashboard", request.data)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SalesPersonCode = request.data['SalesPersonCode']
        Filter      = request.data['Filter']
        Code        = request.data['Code']
        SalesType   = request.data['Type']
        FromDate    = request.data['FromDate']
        ToDate      = request.data['ToDate']
        SearchText  = request.data['SearchText']
        OrderByName = request.data['OrderByName']
        OrderByAmt  = request.data['OrderByAmt']
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        zones = getZoneByEmployee(SalesPersonCode)
        zonesStr = "','".join(zones)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        orderby = "Order By bp.CardName asc"
        if str(OrderByName).lower() == 'a-z':
            orderby = "Order By bp.CardName asc"
        elif str(OrderByName).lower() == 'z-a':
            orderby = "Order By bp.CardName desc"
        elif str(OrderByAmt).lower() == 'asc':
            orderby = "Order By DocTotal asc"
        elif str(OrderByAmt).lower() == 'desc':
            orderby = "Order By DocTotal desc"
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
                INNER JOIN BusinessPartner_businesspartnergroups bpgroup ON bpgroup.Code = bp.GroupCode
                LEFT JOIN PurchaseInvoices_purchaseinvoices inv ON bp.CardCode = inv.CardCode
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
                INNER JOIN BusinessPartner_businesspartnergroups bpgroup ON bpgroup.Code = bp.GroupCode
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
                    FROM PurchaseInvoices_purchaseinvoices inv
                    LEFT JOIN PurchaseInvoices_documentlines INVLine ON INVLine.InvoiceID = inv.id
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

                sqlCreditNoteQuery = f"""
                    SELECT
                        bp.CardCode AS CardCode, bp.CardName AS CardName, IFNULL(SUM(A.DocTotal), 0) AS 'DocTotal', IFNULL(SUM(A.NetTotal), 0) AS 'NetTotal'
                    FROM BusinessPartner_businesspartner bp
                    INNER JOIN(
                        SELECT
                            inv.CardCode, inv.id, inv.DocTotal, inv.PaidToDateSys, IFNULL(SUM(INVLine.LineTotal), 0) AS LineTotal,
                            IFNULL(
                                SUM(
                                    CASE 
                                        WHEN inv.DiscountPercent != 0.0 
                                        THEN INVLine.LineTotal -( INVLine.LineTotal * inv.DiscountPercent / 100 ) 
                                        ELSE INVLine.LineTotal
                                    END
                            ), 0 ) AS NetTotal
                            FROM Invoice_creditnotes inv
                            LEFT JOIN Invoice_creditnotesdocumentlines INVLine ON INVLine.CreditNotesId = inv.id
                            WHERE inv.CancelStatus = 'csNo' { fromToDate }
                            GROUP BY inv.CardCode, inv.id 
                        ) A ON bp.CardCode = A.CardCode
                    WHERE
                        bp.CardCode = '{CardCode}';
                """
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
            # endfor
        # endif
        TotalSales          = round(TotalSales, 2)
        DifferenceAmount    = round(PendingTotal, 2)
        TotalReceivePayment = round(TotalReceivePayment, 2)

        return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": TotalSales, "TotalReceivePayment": TotalReceivePayment, "DifferenceAmount": DifferenceAmount})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# bp list with total purchase
@api_view(['POST'])
def bp_purchase_ledger(request):
    # try:
        print("bp_purchase_ledger",request.data)
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
                orderList = PurchaseInvoices.objects.filter(CancelStatus="csNo", CardCode = CardCode, DocDate__gte = FromDate, DocDate__lte = ToDate).values("id","DocTotal", "CreateDate", "VatSum", "DocEntry", "DocumentStatus", "DocDate", "DiscountPercent", "PaidToDateSys", "DocNum").order_by('-DocDate')
            else:
                orderList = PurchaseInvoices.objects.filter(CancelStatus="csNo", CardCode = CardCode).values("id","DocTotal", "CreateDate", "VatSum", "DocEntry", "DocumentStatus", "DocDate", "DiscountPercent", "PaidToDateSys", "DocNum").order_by('-DocDate')
            
            # print("Length of objects orderList: ", len(orderList))
            if len(orderList) != 0:
                for order in orderList:
                    allPaymentsList = []
                    docEntrys.append(order['DocEntry'])
                    DocTotal = order['DocTotal']
                    VatSum = order['VatSum']
                    DocumentStatus = order['DocumentStatus']
                    PaidToDateSys = order['PaidToDateSys']
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

                    PaymentStatus = "Unpaid"                    
                    if DocumentStatus == "bost_Close":
                        PaymentStatus = "Paid"
                    elif float(PaidToDateSys) > 0:
                        PaymentStatus = "Partially Paid"
                        
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
            IFNULL(SUM(A.NetTotal), 0) AS 'NetTotal'
        FROM BusinessPartner_businesspartner bp
        INNER JOIN (
            SELECT
                inv.CardCode,
                inv.id,
                inv.DocTotal,
                IFNULL(SUM(INVLine.LineTotal), 0) AS LineTotal,
                IFNULL(
                    SUM(CASE
                        WHEN inv.DiscountPercent != 0.0 THEN INVLine.LineTotal - (INVLine.LineTotal * inv.DiscountPercent / 100)
                        ELSE INVLine.LineTotal
                    END), 0
                ) AS NetTotal
            FROM PurchaseInvoices_purchasecreditnotes inv
            LEFT JOIN PurchaseInvoices_creditnotesdocumentlines INVLine ON INVLine.CreditNotesId = inv.id
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
    # except Exception as e:
    #     return Response({"message": str(e),"status": 201,"data":[]})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# bp list with total payment receipt
@api_view(['POST'])
def purchase_receipt_dashboard(request):
    try:
        print("purchase_receipt_dashboard", request.data)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SalesPersonCode = request.data['SalesPersonCode']
        Filter      = request.data['Filter']
        Code        = request.data['Code']
        FromDate    = request.data['FromDate']
        ToDate      = request.data['ToDate']
        SearchText  = request.data['SearchText']
        OrderByName = request.data['OrderByName']
        OrderByAmt  = request.data['OrderByAmt']
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        zones = getZoneByEmployee(SalesPersonCode)
        zonesStr = "','".join(zones)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        orderby = "Order By bp.CardName asc"
        if str(OrderByName).lower() == 'a-z':
            orderby = "Order By bp.CardName asc"
        elif str(OrderByName).lower() == 'z-a':
            orderby = "Order By bp.CardName desc"
        elif str(OrderByAmt).lower() == 'asc':
            orderby = "Order By DocTotal asc"
        elif str(OrderByAmt).lower() == 'desc':
            orderby = "Order By DocTotal desc"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        fromToDate = ""
        if str(FromDate) != "":
            fromToDate = f"AND INVPay.DocDate >= '{FromDate}' AND INVPay.DocDate <= '{ToDate}'"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        limitQuery = ""
        if 'PageNo' in request.data:
            PageNo = int(request.data['PageNo'])
            MaxSize = request.data['MaxSize']
            if MaxSize != "All":
                size = int(MaxSize)
                endWith = (PageNo * size)
                startWith = (endWith - size)
                limitQuery = f"Limit {startWith}, {MaxSize}"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SearchQuery = ""
        if str(SearchText) != '':
            SearchQuery = f"AND (bp.CardCode like '%%{SearchText}%%' OR bp.CardName like '%%{SearchText}%%')"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        filterBy = f"AND bp.U_U_UTL_Zone IN('{zonesStr}')"
        if str(Filter).lower() == 'group':
            filterBy = f"AND bp.U_U_UTL_Zone IN('{zonesStr}') AND bp.GroupCode = '{Code}'"
        elif str(Filter).lower() == 'zone':
            filterBy = f"AND bp.U_U_UTL_Zone = '{Code}'"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        sqlReceipt = f"""
            SELECT
                bp.CardCode,
                bp.CardName,
                IFNULL(SUM(INVPay.TransferSum), 0) AS `TransferSum`
            FROM BusinessPartner_businesspartner bp
                LEFT JOIN PurchaseInvoices_vendorpayments INVPay ON INVPay.CardCode = bp.CardCode
            WHERE 
                INVPay.JournalRemarks != 'Canceled'
                {filterBy}
                {fromToDate}
                {SearchQuery}
            GROUP BY bp.CardCode 
            {orderby}
            {limitQuery}
        """
        # AND bp.CardType = 'cSupplier'

        print(sqlReceipt)
        mycursor.execute(sqlReceipt)
        receipData = mycursor.fetchall()
        dataContext = []
        totalSales = 0
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
        
        TotalSales = totalSales
        TotalReceivePayment = round(totalSales, 2)

        return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": TotalSales, "TotalReceivePayment": TotalReceivePayment, "DifferenceAmount":0})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# bp list with total payment receipt
@api_view(['POST'])
def bp_purchase_receipt(request):
    try:
        print("bp_purchase_receipt", request.data)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        CardCode = request.data['CardCode']
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        
        dataContext = []
        docEntrys = []
        totalSalesByBp = 0
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
                orderList = VendorPayments.objects.filter(CardCode = CardCode, DocDate__gte = FromDate, DocDate__lte = ToDate).exclude(JournalRemarks = 'Canceled').values("id","DocDate", "TransferSum", "DocEntry", "Comments", "DocNum").order_by('-DocDate')
            else:
                orderList = VendorPayments.objects.filter(CardCode = CardCode).exclude(JournalRemarks = 'Canceled').values("id","DocDate", "TransferSum", "DocEntry", "Comments", "DocNum").order_by('-DocDate')
            
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
                bp.CardCode,
                bp.CardName,
                IFNULL(SUM(INVPay.TransferSum), 0) AS `TotalReceivePayment`
            FROM BusinessPartner_businesspartner bp
                LEFT JOIN PurchaseInvoices_vendorpayments INVPay ON INVPay.CardCode = bp.CardCode
            WHERE 
                INVPay.JournalRemarks != 'Canceled'
                AND bp.CardCode = '{CardCode}'
                {fromToDate};
        """

        print(sqlReceipt)
        mycursor.execute(sqlReceipt)
        TotalSales = 0
        TotalReceivePayment = 0
        receipData = mycursor.fetchall()
        if len(receipData) > 0:
            TotalReceivePayment = receipData[0]['TotalReceivePayment']

        return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": TotalSales, "TotalReceivePayment": TotalReceivePayment, "BPData":BPDataa})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# @api_view(['POST'])
# def one_receipt(request):
#     try:
#         ReceiptId=request.data['ReceiptId']
#         paymentObj = VendorPayments.objects.filter(DocEntry = ReceiptId)
#         result = showIncomingPayments(paymentObj)
#         return Response({"message":"successful","status":"200","data":result}) 
#     except Exception as e:
#         return Response({"message":str(e),"status":"201","data":[]})

# bp list with total purchase
@api_view(['POST'])
def ap_credit_note_dashboard(request):
    try:
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']

        Filter = ""
        Code = ""
        if 'Filter' in request.data:
            Filter = request.data['Filter']
            Code = request.data['Code']
            
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SalesType = "Gross"
        if 'Type' in request.data:
            SalesType = request.data['Type']
        
        SearchText = ""
        if 'SearchText' in request.data:
            SearchText = request.data['SearchText']

        SalesPersonCode = -1
        if 'SalesPersonCode' in request.data:
            SalesPersonCode = request.data['SalesPersonCode']
        zones = getZoneByEmployee(SalesPersonCode)

        cardCodeList = []
        if str(FromDate) != "":
            cardCodeList = list(PurchaseCreditNotes.objects.filter(DocDate__gte = FromDate, DocDate__lte = ToDate).values_list('CardCode', flat=True).distinct())
        else:
            cardCodeList = list(PurchaseCreditNotes.objects.all().values_list('CardCode', flat=True).distinct())
        
        bpObjs = []
        if str(Filter).lower() == 'group':
            bpObjs = BusinessPartner.objects.filter(Q(GroupCode = Code) & Q(U_U_UTL_Zone__in = zones) & Q(CardCode__in = cardCodeList) & Q( Q(CardCode__icontains = SearchText) | Q(CardName__icontains = SearchText)) ).values("id", "CardCode", "CardName", "PayTermsGrpCode","CreditLimit","CreditLimitLeft").order_by('CardCode')
        elif str(Filter).lower() == 'zone':
            bpObjs = BusinessPartner.objects.filter(Q(U_U_UTL_Zone = Code) & Q(CardCode__in = cardCodeList) & Q( Q(CardCode__icontains = SearchText) | Q(CardName__icontains = SearchText))).values("id", "CardCode", "CardName", "PayTermsGrpCode","CreditLimit","CreditLimitLeft").order_by('CardCode')
        else:
            bpObjs = BusinessPartner.objects.filter(Q(U_U_UTL_Zone__in = zones) & Q(CardCode__in = cardCodeList) & Q( Q(CardCode__icontains = SearchText) | Q(CardName__icontains = SearchText))).values("id", "CardCode", "CardName", "PayTermsGrpCode","CreditLimit","CreditLimitLeft").order_by('CardCode')

        print(bpObjs)
        print(bpObjs.query)
        # bpObjs = BusinessPartner.objects.filter(Q(U_U_UTL_Zone__in = zones) & Q(CardCode__in = cardCodeList) & Q( Q(CardCode__icontains = SearchText) | Q(CardName__icontains = SearchText))).values("id", "CardCode", "CardName")
        if 'PageNo' in request.data:
            PageNo = int(request.data['PageNo'])
            MaxSize = request.data['MaxSize']
            if MaxSize != "All":
                size = int(MaxSize)
                endWith = (PageNo * size)
                startWith = (endWith - size)
                bpObjs = bpObjs[startWith:endWith]

        dataContext = []
        totalSales = 0
        allPaymentsList = 0
        for bpobj in bpObjs:
            creditNotesList = []
            totalCreditNoteByBP = 0 
            if str(FromDate) != "":
                creditNotesList = PurchaseCreditNotes.objects.filter(CancelStatus="csNo", CardCode = bpobj['CardCode'], DocDate__gte = FromDate, DocDate__lte = ToDate).values("id","DocTotal", "CreateDate", "VatSum", "DocEntry", "DocDate", "DiscountPercent").order_by('-DocDate')
            else:
                creditNotesList = PurchaseCreditNotes.objects.filter(CancelStatus="csNo", CardCode = bpobj['CardCode']).values("id","DocTotal", "CreateDate", "VatSum", "DocEntry", "DocDate", "DiscountPercent").order_by('-DocDate')

            for creditNotes in creditNotesList:
                creditNoteId = creditNotes['id']
                # docEntry = creditNotes['DocEntry']
                DocTotal = creditNotes['DocTotal']
                DiscountPercent = creditNotes['DiscountPercent']
                if str(SalesType).lower() == "net":
                    BaseTotal = 0
                    itemObjs = CreditNotesDocumentLines.objects.filter(CreditNotesId = creditNoteId).values("id","LineTotal")
                    for itObjs in itemObjs:
                        LineTotal = float(itObjs['LineTotal'])
                        BaseTotal = BaseTotal + LineTotal
                    disAmt = 0
                    if BaseTotal != 0:
                        if float(DiscountPercent) != 0.0:
                            disAmt = (BaseTotal * DiscountPercent) / 100
                    DocTotal = round(float(BaseTotal - disAmt), 2)
                totalCreditNoteByBP = totalCreditNoteByBP + float(DocTotal)

            bpData = {"CardName": bpobj['CardName'], "CardCode": bpobj['CardCode'], "TotalSales": round(totalCreditNoteByBP, 2)}
            dataContext.append(bpData)
            totalSales = float(totalSales) + float(totalCreditNoteByBP)

        TotalSales = 0
        TotalReceivePayment = round(totalSales, 2)
        DifferenceAmount = 0

        return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": TotalSales, "TotalReceivePayment": TotalReceivePayment, "DifferenceAmount": DifferenceAmount})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
        

