from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from BusinessPartner.models import BPEmployee
from BusinessPartner.serializers import BPEmployeeSerializer

from Employee.serializers import EmployeeSerializer
from PaymentTermsTypes.models import PaymentTermsTypes
from PaymentTermsTypes.serializers import PaymentTermsTypesSerializer
from BusinessPartner.models import BusinessPartner
from BusinessPartner.serializers import BPAddressesSerializer
from BusinessPartner.models import BPAddresses
from Company.models import Branch
from global_methods import *
from .models import *
from Employee.models import Employee
from django.db.models import Q
from rest_framework.decorators import api_view    
from rest_framework.response import Response
from .serializers import *
from pytz import timezone
from datetime import datetime as dt
from urllib.parse import unquote

import json
import datetime

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
            quot_obj = PurchaseOrders.objects.filter(SalesPersonCode__in=empList).order_by("-id")
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
            quot_obj = PurchaseOrders.objects.filter(SalesPersonCode__in=empList).order_by("-id")
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
        invoice_obj = PurchaseOrders.objects.all().order_by("-id")
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
        invoice_obj = PurchaseOrders.objects.filter(DocEntry = id)
        # invoice_obj = PurchaseOrders.objects.filter(pk=id)
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
        fetchdata=PurchaseOrders.objects.filter(pk=fetchid).delete()
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
        cpcjson = PurchaseOrdersSerializer(obj)
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
        if AddressExtension.objects.filter(OrderID = invId).exists():
            addrObj = AddressExtension.objects.filter(OrderID = invId)
            addrjson = AddressExtensionSerializer(addrObj, many=True)
            finalCPCData['AddressExtension'] = json.loads(json.dumps(addrjson.data))
        else:
            finalCPCData['AddressExtension'] = []
        ################################addedd################################
            
        ################################addedd################################
        BaseTotal = 0
        if DocumentLines.objects.filter(OrderID=invId).exists():
            linesobj = DocumentLines.objects.filter(OrderID=invId)
            lines_json = DocumentLinesSerializer(linesobj, many=True)
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
        allInvoice.append(finalCPCData)
    return allInvoice
