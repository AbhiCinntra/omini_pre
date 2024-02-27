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
from Order.models import Order
from Order.models import DocumentLines as Order_DocumentLines
from Order.models import AddressExtension as Order_AddressExtension

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
        ReceiptId=request.data['ReceiptId']
        paymentObj = VendorPayments.objects.filter(DocEntry = ReceiptId)
        # paymentObj = VendorPayments.objects.filter(pk=ReceiptId)
        result = showIncomingPayments(paymentObj)
        return Response({"message":"successful","status":"200","data":result})
        # if VendorPayments.objects.filter(pk=ReceiptId).exists():
        #     paymentObj = VendorPayments.objects.filter(pk=ReceiptId)
        #     result = showIncomingPayments(paymentObj)
        #     return Response({"message":"successful","status":"200","data":result})
        # else:
        #     return Response({"message":"Invalid Receipt Id?","status":"201","data":[]})      
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
            return Response({"message":"Invalid BP Code?","status":"201","data":[]})      
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
                
                incomingPayIds = VendorPaymentsInvoices.objects.filter(InvoiceDocEntry = invObj.DocEntry, DocDate__gte = FromDate, DocDate__lte = ToDate).values_list('IncomingPaymentsId', flat=True)
                incomingPayObj = VendorPayments.objects.filter(pk__in = incomingPayIds)
                result = showIncomingPayments(incomingPayObj)
            else:
                incomingPayIds = VendorPaymentsInvoices.objects.filter(InvoiceDocEntry = invObj.DocEntry).values_list('IncomingPaymentsId', flat=True)
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
        paymentObj = VendorPaymentsInvoicesSerializer(obj, many=False)
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
        if VendorPaymentsInvoices.objects.filter(IncomingPaymentsId = obj.id).exists():
            invObjs = VendorPaymentsInvoices.objects.filter(IncomingPaymentsId = obj.id)
            invJson = VendorPaymentsInvoicesSerializer(invObjs, many=True)
            finalIncomingPayment['IncomingPaymentInvoices'] = invJson.data
        else:
            finalIncomingPayment['IncomingPaymentInvoices'] = []
        allIncomingPayments.append(finalIncomingPayment)

    return allIncomingPayments