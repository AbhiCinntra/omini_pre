from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from BusinessPartner.models import BPAddresses, BPBranch, BPEmployee, BusinessPartnerGroups
from BusinessPartner.serializers import BPAddressesSerializer, BPEmployeeSerializer

from Company.models import Branch
from Employee.serializers import EmployeeSerializer
from PaymentTermsTypes.models import PaymentTermsTypes
from PaymentTermsTypes.serializers import PaymentTermsTypesSerializer
from BusinessPartner.models import BusinessPartner
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

date = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d')
yearmonth = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m')
time = dt.now(timezone("Asia/Kolkata")).strftime('%H:%M %p')

from urllib.parse import unquote

# Create your views here.  

#Invoice Create API
@api_view(['POST'])
def create(request):
    invoice_obj = Invoice.objects.filter(OrderID=request.data['oid'])
    if len(invoice_obj) != 0:
        for inv_obj in invoice_obj:
            print(inv_obj.id)
        return Response({"message":"success","status":200,"data":[{"id":inv_obj.id}]})
    else:
        odr = Order.objects.get(pk=request.data['oid'])
        try:
            TaxDate = odr.TaxDate
            DocDueDate = odr.DocDueDate
            ContactPersonCode = odr.ContactPersonCode
            DiscountPercent = odr.DiscountPercent
            DocDate = odr.DocDate
            CardCode = odr.CardCode
            CardName = odr.CardName
            Comments = odr.Comments
            SalesPersonCode = odr.SalesPersonCode
            CreateDate = odr.CreateDate
            CreateTime = odr.CreateTime
            UpdateDate = odr.UpdateDate
            UpdateTime = odr.UpdateTime
            OrderID = odr.id
            lines = Order_DocumentLines.objects.filter(OrderID=request.data['oid'])
            DocTotal=0
            for line in lines:
                DocTotal = float(DocTotal) + float(line.Quantity) * float(line.UnitPrice)
            #print(DocTotal)

            model=Invoice(TaxDate = TaxDate, DocDueDate = DocDueDate, ContactPersonCode = ContactPersonCode, DiscountPercent = DiscountPercent, DocDate = DocDate, CardCode = CardCode, CardName = CardName, Comments = Comments, SalesPersonCode = SalesPersonCode, DocumentStatus="bost_Open", DocTotal = DocTotal, OrderID = OrderID, CreateDate = CreateDate, CreateTime = CreateTime, UpdateDate = UpdateDate, UpdateTime = UpdateTime)
            
            model.save()
            qt = Invoice.objects.latest('id')    
            #model = Invoice.objects.get(pk = fetchid)
            model.DocEntry = qt.id
            model.save()
            
            addrs = Order_AddressExtension.objects.filter(OrderID=request.data['oid'])
            for addr in addrs:
                model_add = AddressExtension(InvoiceID = qt.id, BillToBuilding = addr.BillToBuilding, ShipToState = addr.ShipToState, BillToCity = addr.BillToCity, ShipToCountry = addr.ShipToCountry, BillToZipCode = addr.BillToZipCode, ShipToStreet = addr.ShipToStreet, BillToState = addr.BillToState, ShipToZipCode = addr.ShipToZipCode, BillToStreet = addr.BillToStreet, ShipToBuilding = addr.ShipToBuilding, ShipToCity = addr.ShipToCity, BillToCountry = addr.BillToCountry, U_SCOUNTRY = addr.U_SCOUNTRY, U_SSTATE = addr.U_SSTATE, U_SHPTYPB = addr.U_SHPTYPB, U_BSTATE = addr.U_BSTATE, U_BCOUNTRY = addr.U_BCOUNTRY, U_SHPTYPS = addr.U_SHPTYPS)
                
                model_add.save()

            LineNum = 0
            for line in lines:
                model_lines = DocumentLines(LineNum = LineNum, InvoiceID = qt.id, Quantity = line.Quantity, UnitPrice = line.UnitPrice, DiscountPercent = line.DiscountPercent, ItemCode = line.ItemCode, ItemDescription = line.ItemDescription, TaxCode = line.TaxCode)
                model_lines.save()
                LineNum=LineNum+1
            
            return Response({"message":"successful","status":200,"data":[{"id":qt.id, "DocEntry":qt.id}]})
        except Exception as e:
            return Response({"message":"Not Created","status":201,"data":[{"Error":str(e)}]})

#Invoice Update API
@api_view(['POST'])
def update(request):
    fetchid = request.data['id']
    try:
        model = Invoice.objects.get(pk = fetchid)

        model.TaxDate = request.data['TaxDate']
        model.DocDate = request.data['DocDate']
        model.DocDueDate = request.data['DocDueDate']
        
        model.ContactPersonCode = request.data['ContactPersonCode']
        model.DiscountPercent = request.data['DiscountPercent']
        model.Comments = request.data['Comments']
        model.SalesPersonCode = request.data['SalesPersonCode']
        
        model.UpdateDate = request.data['UpdateDate']
        model.UpdateTime = request.data['UpdateTime']

        model.save()
        
        model_add = AddressExtension.objects.get(id = request.data['AddressExtension']['id'])
        #print(model_add)
        
        model_add.BillToBuilding = request.data['AddressExtension']['BillToBuilding']
        model_add.ShipToState = request.data['AddressExtension']['ShipToState']
        model_add.BillToCity = request.data['AddressExtension']['BillToCity']
        model_add.ShipToCountry = request.data['AddressExtension']['ShipToCountry']
        model_add.BillToZipCode = request.data['AddressExtension']['BillToZipCode']
        model_add.ShipToStreet = request.data['AddressExtension']['ShipToStreet']
        model_add.BillToState = request.data['AddressExtension']['BillToState']
        model_add.ShipToZipCode = request.data['AddressExtension']['ShipToZipCode']
        model_add.BillToStreet = request.data['AddressExtension']['BillToStreet']
        model_add.ShipToBuilding = request.data['AddressExtension']['ShipToBuilding']
        model_add.ShipToCity = request.data['AddressExtension']['ShipToCity']
        model_add.BillToCountry = request.data['AddressExtension']['BillToCountry']
        model_add.U_SCOUNTRY = request.data['AddressExtension']['U_SCOUNTRY']
        model_add.U_SSTATE = request.data['AddressExtension']['U_SSTATE']
        model_add.U_SHPTYPB = request.data['AddressExtension']['U_SHPTYPB']
        model_add.U_BSTATE = request.data['AddressExtension']['U_BSTATE']
        model_add.U_BCOUNTRY = request.data['AddressExtension']['U_BCOUNTRY']
        model_add.U_SHPTYPS = request.data['AddressExtension']['U_SHPTYPS']
   
        model_add.save()
        #print("add save")
        
        lines = request.data['DocumentLines']
        for line in lines:
            if "id" in line:
                model_line = DocumentLines.objects.get(pk = line['id'])
                model_line.Quantity=line['Quantity']
                model_line.UnitPrice=line['UnitPrice']
                model_line.DiscountPercent=line['DiscountPercent']
                model_line.ItemCode=line['ItemCode']
                model_line.ItemDescription=line['ItemDescription']
                model_line.TaxCode=line['TaxCode']            
                model_line.save()
            else:
                lastline = DocumentLines.objects.filter(InvoiceID = fetchid).order_by('-LineNum')[:1]
                NewLine = int(lastline[0].LineNum) + 1
                model_lines = DocumentLines(InvoiceID = fetchid, LineNum=NewLine, Quantity = line['Quantity'], UnitPrice = line['UnitPrice'], DiscountPercent = line['DiscountPercent'], ItemCode = line['ItemCode'], ItemDescription = line['ItemDescription'], TaxCode = line['TaxCode'])
                model_lines.save()
            
        return Response({"message":"successful","status":200, "data":[request.data]})
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})

def InvoiceShow(Invoices_obj):
    allqt = [];
    for qt in Invoices_obj:
        qtaddr = AddressExtension.objects.filter(InvoiceID=qt.id)
        
        qtaddr_json = AddressExtensionSerializer(qtaddr, many=True)
        jss0 = ''
        jss_ = json.loads(json.dumps(qtaddr_json.data))
        for j in jss_:
            jss0=j
        
        lines = DocumentLines.objects.filter(InvoiceID=qt.id)
        
        lines_json = DocumentLinesSerializer(lines, many=True)
        
        jss1 = json.loads(json.dumps(lines_json.data))
        
        context = {
            'id':qt.id,
            'DocEntry':qt.DocEntry,
            'OrderID':qt.OrderID,
            'DocDueDate':qt.DocDueDate,
            'DocDate':qt.DocDate,
            'TaxDate':qt.TaxDate,
            'ContactPersonCode':qt.ContactPersonCode,
            'DiscountPercent':qt.DiscountPercent,
            'CardCode':qt.CardCode,
            'CardName':qt.CardName,
            'Comments':qt.Comments,
            'SalesPersonCode':qt.SalesPersonCode,
            
            'DocumentStatus':qt.DocumentStatus,
            'DocCurrency':qt.DocCurrency,
            'DocTotal':qt.DocTotal,
            'VatSum':qt.VatSum,
            'CreationDate':qt.CreationDate,
            
            'AddressExtension':jss0,
            'DocumentLines':jss1,
            
            "CreateDate":qt.CreateDate,
            "CreateTime":qt.CreateTime,
            "UpdateDate":qt.UpdateDate,
            "UpdateTime":qt.UpdateTime
            }
            
        allqt.append(context)
        
    return allqt

@api_view(["POST"])
def delivery(request):

    json_data = request.data
    
    if "SalesEmployeeCode" in json_data:
        #print("yes")
        
        if json_data['SalesEmployeeCode']!="":
            SalesEmployeeCode = json_data['SalesEmployeeCode']
            
            emp_obj =  Employee.objects.get(SalesEmployeeCode=SalesEmployeeCode)
            if emp_obj.role == 'admin':
                emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
                SalesEmployeeCode=[]
                for emp in emps:
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)                    
            elif emp_obj.role == 'manager':
                emps = Employee.objects.filter(reportingTo=SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
                SalesEmployeeCode=[SalesEmployeeCode]
                for emp in emps:
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)
            else:
                SalesEmployeeCode=[SalesEmployeeCode]
                # emps = Employee.objects.filter(reportingTo=emp_obj.reportingTo)#.values('id', 'SalesEmployeeCode')
                # SalesEmployeeCode=[]
                # for emp in emps:
                    # SalesEmployeeCode.append(emp.SalesEmployeeCode)
            
            #print(SalesEmployeeCode)

            if json_data['Type'] =="over":
                ord = Invoice.objects.filter(SalesPersonCode__in=SalesEmployeeCode, DocumentStatus="bost_Open", DocDueDate__lt=date)
                allord = InvoiceShow(ord)
                ##print(allord)
            elif json_data['Type'] =="open":
                ord = Invoice.objects.filter(SalesPersonCode__in=SalesEmployeeCode, DocumentStatus="bost_Open", DocDueDate__gte=date)
                allord = InvoiceShow(ord)
                ##print(allord)
            else:
                ord = Invoice.objects.filter(SalesPersonCode__in=SalesEmployeeCode, DocumentStatus="bost_Close")
                allord = InvoiceShow(ord)
                ##print(allord)
			
            #{"SalesEmployeeCode":"2"}
            return Response({"message": "Success","status": 200,"data":allord})
            
            #return Response({"message": "Success","status": 201,"data":[{"emp":SalesEmployeeCode}]})
        else:
            return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})
    else:
        return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})
	
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Invoice All API
@api_view(["POST"])
def all_filter(request):
    try:
        SalesPersonCode = request.data['SalesPersonCode']
        if Employee.objects.filter(SalesEmployeeCode = SalesPersonCode).exists():
            empList = getAllReportingToIds(SalesPersonCode)
            #print("empList: ", empList)
            quot_obj = Invoice.objects.filter(SalesPersonCode__in=empList).order_by("-id")
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
            quot_obj = Invoice.objects.filter(SalesPersonCode__in=empList).order_by("-id")
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
        invoice_obj = Invoice.objects.all().order_by("-id")
        result = showInvoice(invoice_obj)
        return Response({"message": "Success","status": 200,"data":result})
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})
    
#Invoice One API
@api_view(["POST"])
def one(request):
    # try:
        id=request.data['id'] 
        invoice_obj = Invoice.objects.filter(DocEntry = id)
        # invoice_obj = Invoice.objects.filter(pk=id)
        result = showInvoice(invoice_obj)
        return Response({"message": "Success","status": 200,"data":result})
    # except Exception as e:
    #     return Response({"message":str(e),"status":"201","data":[]})
    

#Invoice delete
@api_view(['POST'])
def delete(request):
    fetchid=request.data['id']
    try:
        fetchdata=Invoice.objects.filter(pk=fetchid).delete()
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
        cpcjson = InvoiceSerializer(obj)
        finalCPCData = json.loads(json.dumps(cpcjson.data))
        BaseEntry = 0
        paymentType = obj.PaymentGroupCode
       
        ################################addedd################################
        BPLID = obj.BPLID
        if Branch.objects.filter(BPLId=BPLID).exists():
            branch_obj = Branch.objects.filter(BPLId=BPLID).first()
            finalCPCData["BPLName"] = branch_obj.BPLName
            finalCPCData["Address"] = unquote(branch_obj.Address)
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
        elif float(obj.PaidToDateSys) > 0:
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
        cpcjson = InvoiceSerializer(obj)
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
            finalCPCData["Address"] = unquote(branch_obj.Address)
            finalCPCData["State"] = branch_obj.State
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
        paymentObj = IncomingPayments.objects.filter(DocEntry = ReceiptId)
        result = showIncomingPayments(paymentObj)
        return Response({"message":"successful","status":"200","data":result})
        # if IncomingPayments.objects.filter(pk=ReceiptId).exists():
        #     paymentObj = IncomingPayments.objects.filter(pk=ReceiptId)
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
            paymentObj = IncomingPayments.objects.filter(CardCode = CardCode).exclude(JournalRemarks = 'Canceled').order_by('-DocDate')
            
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
def incoming_payments(request):
    try:
        InvoiceId=request.data['id']
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        if Invoice.objects.filter(pk=InvoiceId).exists():
            invObj = Invoice.objects.filter(pk=InvoiceId).first()
            incomingPayObj = []
            result = []
            if str(FromDate) !="":
                
                incomingPayIds = IncomingPaymentInvoices.objects.filter(InvoiceDocEntry = invObj.DocEntry, DocDate__gte = FromDate, DocDate__lte = ToDate).values_list('IncomingPaymentsId', flat=True)
                incomingPayObj = IncomingPayments.objects.filter(pk__in = incomingPayIds).exclude(JournalRemarks = 'Canceled')
                result = showIncomingPayments(incomingPayObj)
            else:
                incomingPayIds = IncomingPaymentInvoices.objects.filter(InvoiceDocEntry = invObj.DocEntry).values_list('IncomingPaymentsId', flat=True)
                incomingPayObj = IncomingPayments.objects.filter(pk__in = incomingPayIds).exclude(JournalRemarks = 'Canceled')
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
def all_incoming_payments(request):
    try:
        SalesEmployeeCode = request.data['SalesEmployeeCode']
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        allEmp = getAllReportingToIds(SalesEmployeeCode)
        docEntrys = list(Invoice.objects.filter(SalesPersonCode__in = allEmp).values_list('DocEntry', flat=True))
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
            totalSalesList = list(Invoice.objects.filter(SalesPersonCode__in = allEmp, DocDate__gte = FromDate, DocDate__lte = ToDate).values_list('DocTotal', flat=True))
            allPaymentsList = IncomingPaymentInvoices.objects.filter(InvoiceDocEntry__in = docEntrys, DocDate__gte = FromDate, DocDate__lte = ToDate).values_list('SumApplied', flat=True)
            
        else:
            totalSalesList = list(Invoice.objects.filter(SalesPersonCode__in = allEmp).values_list('DocTotal', flat=True))
            allPaymentsList = IncomingPaymentInvoices.objects.filter(InvoiceDocEntry__in = docEntrys).values_list('SumApplied', flat=True)
            
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
@api_view(['POST'])
def credit_notes(request):
    try:
        InvoiceId=request.data['id']
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        if Invoice.objects.filter(pk=InvoiceId).exists():
            invObj = Invoice.objects.filter(pk=InvoiceId).first()
            incomingPayObj = []
            if str(FromDate) != "":
                incomingPayObj = CreditNotes.objects.filter(InvoiceDocEntry = invObj.DocEntry, DocDate__gte = FromDate, DocDate__lte = ToDate)
            else:
                incomingPayObj = CreditNotes.objects.filter(InvoiceDocEntry = invObj.DocEntry)

            incomingPayJson = CreditNotesSerializer(incomingPayObj, many=True)
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
def credit_notes_one(request):
    try:
        id = request.data['id']
        credit_objs = CreditNotes.objects.filter(DocEntry = id)
        # credit_objs = CreditNotes.objects.filter(pk=id)
        CreditNoteList = showCreditNote(credit_objs)
        return Response({"message":"successful","status":"200","data":CreditNoteList})
        # if CreditNotes.objects.filter(pk=id).exists():
        #     credit_objs = CreditNotes.objects.filter(pk=id)
        #     CreditNoteList = showCreditNote(credit_objs)
        #     return Response({"message":"successful","status":"200","data":CreditNoteList})
        # else:
        #     return Response({"message":"Invalid Credit Note Id?","status":"201","data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# bp list with total purchase
"""
{
    "SalesPersonCode": -1,
    "PageNo": "3",
    "MaxSize": "20",
    "FromDate": "",
    "ToDate": ""
}

"""

@api_view(['POST'])
def payment_collection_dashboard(request):
    try:
        # SalesType = request.data['Type']
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']

        SalesPersonCode = -1
        if 'SalesPersonCode' in request.data:
            SalesPersonCode = request.data['SalesPersonCode']
        zones = getZoneByEmployee(SalesPersonCode)

        cardCodeList = list(Invoice.objects.all().values_list('CardCode', flat=True).distinct())
        #print("<><><><>< cardCodeList", cardCodeList)
        bpObjs = []
        # bpObjs = BusinessPartner.objects.filter(CardCode__in = cardCodeList).values("id", "CardCode", "CardName")
        if 'SearchText' in request.data:
            SearchText = request.data['SearchText']
            bpObjs = BusinessPartner.objects.filter(Q(U_U_UTL_Zone__in = zones) & Q(CardCode__in = cardCodeList) & Q( Q(CardCode__icontains = SearchText) | Q(CardName__icontains = SearchText))).values("id", "CardCode", "CardName")
        else:
            bpObjs = BusinessPartner.objects.filter(U_U_UTL_Zone__in = zones, CardCode__in = cardCodeList).values("id", "CardCode", "CardName")

        if 'PageNo' in request.data:
            PageNo = int(request.data['PageNo'])
            MaxSize = request.data['MaxSize']
            if MaxSize != "All":
                size = int(MaxSize)
                endWith = (PageNo * size)
                startWith = (endWith - size)
                bpObjs = bpObjs[startWith:endWith]

        dataContext = []
        docEntrys = []
        totalSales = 0
        allPaymentsList = 0
        for bpobj in bpObjs:
            orderList = []
            if str(FromDate) != "":
                orderList = Invoice.objects.filter(CancelStatus="csNo", CardCode = bpobj['CardCode'], DocDate__gte = FromDate, DocDate__lte = ToDate).values("id","DocTotal", "CreateDate", "VatSum", "DocEntry").order_by('-DocDate')
            else:
                orderList = Invoice.objects.filter(CancelStatus="csNo", CardCode = bpobj['CardCode']).values("id","DocTotal", "CreateDate", "VatSum", "DocEntry").order_by('-DocDate')
            
            totalSalesByBp = 0 
            #print("Length of objects orderList: ", len(orderList))
            if len(orderList) != 0:
                #print("Query", orderList.query)
                for order in orderList:
                    #print("in invoice list")
                    docEntry = order['DocEntry']
                    #print(docEntry)
                    docEntrys.append(docEntry)
                    DocTotal = order['DocTotal']
                    # VatSum = order['VatSum']
                    totalSalesByBp = totalSalesByBp + float(DocTotal)
                
                #print("docEntry", docEntrys)
                if str(FromDate) != "":
                    allPayments = IncomingPayments.objects.filter(CardCode = bpobj['CardCode'], DocDate__gte = FromDate, DocDate__lte = ToDate).exclude(JournalRemarks = 'Canceled').values_list('TransferSum', flat=True)
                    # allPayments = IncomingPaymentInvoices.objects.filter(InvoiceDocEntry__in = docEntrys, DocDate__gte = FromDate, DocDate__lte = ToDate).values_list('SumApplied', flat=True)
                else:
                    allPayments = IncomingPayments.objects.filter(CardCode = bpobj['CardCode']).exclude(JournalRemarks = 'Canceled').values_list('TransferSum', flat=True)
                    # allPayments = IncomingPaymentInvoices.objects.filter(InvoiceDocEntry__in = docEntrys).values_list('SumApplied', flat=True)

                
                #print("allPayments: ",allPayments)

                allPayment = 0
                for item in allPayments:
                    allPayment += float(item)
                
                allPaymentsList = allPaymentsList + allPayment

                InvDifferenceAmount = round(float(float(totalSalesByBp) - float(allPaymentsList)), 2)

                bpData = {
                    "CardName": bpobj['CardName'],
                    "CardCode": bpobj['CardCode'],
                    "TotalSales": round(InvDifferenceAmount, 2)
                }
                dataContext.append(bpData)
                totalSales = float(totalSales) + float(totalSalesByBp)
            else:
                pass
                #print('no invoices')

        TotalSales = totalSales
        TotalReceivePayment = round(allPaymentsList, 2)
        DifferenceAmount = round(float(float(TotalSales) - float(allPaymentsList)), 2)

        return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": TotalSales, "TotalReceivePayment": TotalReceivePayment, "DifferenceAmount": DifferenceAmount})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# bp list with total purchase
@api_view(['POST'])
def bp_payment_collection(request):
    try:
        CardCode = request.data['CardCode']
        # SalesType = request.data['Type'] # Gross/Net
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        
        dataContext = []
        docEntrys = []
        totalSales = 0
        totalSalesByBp = 0
        allPaymentsList = 0

        if BusinessPartner.objects.filter(CardCode = CardCode).exists():
            orderList = []
            if str(FromDate) != "":
                orderList = Invoice.objects.filter(CancelStatus="csNo", CardCode = CardCode, DocDate__gte = FromDate, DocDate__lte = ToDate).values("id","DocTotal", "CreateDate", "VatSum", "DocEntry").order_by('-DocDate')
            else:
                orderList = Invoice.objects.filter(CancelStatus="csNo", CardCode = CardCode).values("id","DocTotal", "CreateDate", "VatSum", "DocEntry").order_by('-DocDate')
            
            #print("Length of objects orderList: ", len(orderList))
            
            if 'PageNo' in request.data:
                PageNo = int(request.data['PageNo'])
                MaxSize = request.data['MaxSize']
                if MaxSize != "All":
                    size = int(MaxSize)
                    endWith = (PageNo * size)
                    startWith = (endWith - size)
                    orderList = orderList[startWith:endWith]
                    
            if len(orderList) != 0:
                for order in orderList:
                    docEntrys.append(order['DocEntry'])
                    DocTotal = order['DocTotal']

                    if str(FromDate) != "":
                        allPayments = IncomingPayments.objects.filter(CardCode = CardCode, DocDate__gte = FromDate, DocDate__lte = ToDate).exclude(JournalRemarks = 'Canceled').values_list('TransferSum', flat=True).order_by('-DocDate')
                        # allPayments = IncomingPaymentInvoices.objects.filter(InvoiceDocEntry = order['DocEntry'], DocDate__gte = FromDate, DocDate__lte = ToDate).values_list('SumApplied', flat=True)
                    else:
                        allPayments = IncomingPayments.objects.filter(CardCode = CardCode).exclude(JournalRemarks = 'Canceled').values_list('TransferSum', flat=True).order_by('-DocDate')
                        # allPayments = IncomingPaymentInvoices.objects.filter(InvoiceDocEntry = order['DocEntry']).values_list('SumApplied', flat=True)
                    
                    #print("allPayments: ",allPayments)

                    allPayment = 0
                    for item in allPayments:
                        allPayment += float(item)
                    
                    allPaymentsList = allPaymentsList + allPayment

                    InvDifferenceAmount = round(float(float(DocTotal) - float(allPayment)), 2)

                    bpData = {
                        "OrderId": order['id'],
                        "OrderAmount": InvDifferenceAmount,
                        "CreateDate": order['CreateDate']
                    }                    
                    dataContext.append(bpData)
                    totalSalesByBp = totalSalesByBp + float(DocTotal)
            else:
                print('no invoice')
        else:
            return Response({"message": "Invalid CardCode","status": 201, "data":[], "TotalSales": 0})

        TotalSales = round(totalSalesByBp, 2)
        TotalReceivePayment = round(allPaymentsList, 2)
        DifferenceAmount = round(float(float(totalSalesByBp) - float(allPaymentsList)), 2)

        return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": TotalSales, "TotalReceivePayment": TotalReceivePayment, "DifferenceAmount": DifferenceAmount})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# bp list with total purchase
@api_view(['POST'])
def credit_note_dashboard(request):
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
            cardCodeList = list(CreditNotes.objects.filter(DocDate__gte = FromDate, DocDate__lte = ToDate).values_list('CardCode', flat=True).distinct())
        else:
            cardCodeList = list(CreditNotes.objects.all().values_list('CardCode', flat=True).distinct())
        
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
                creditNotesList = CreditNotes.objects.filter(CancelStatus="csNo", CardCode = bpobj['CardCode'], DocDate__gte = FromDate, DocDate__lte = ToDate).values("id","DocTotal", "CreateDate", "VatSum", "DocEntry", "DocDate", "DiscountPercent").order_by('-DocDate')
            else:
                creditNotesList = CreditNotes.objects.filter(CancelStatus="csNo", CardCode = bpobj['CardCode']).values("id","DocTotal", "CreateDate", "VatSum", "DocEntry", "DocDate", "DiscountPercent").order_by('-DocDate')

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
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# bp list with total purchase
@api_view(['POST'])
def bp_credit_note(request):
    # try:
        CardCode = request.data['CardCode']
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']

        SalesType = "Gross" # Gross/Net
        if 'Type' in request.data:
            SalesType = request.data['Type']

        # SearchText = ""
        # if 'SearchText' in request.data:
        #     SearchText = request.data['SearchText']
        
        dataContext = []
        docEntrys = []
        totalSalesByBp = 0
        allPaymentsList = 0

        BPData = []
        if BusinessPartner.objects.filter(CardCode = CardCode).exists():
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            bpobj = BusinessPartner.objects.filter(CardCode = CardCode).first()
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

            if str(FromDate) != "":
                creditNotesList = CreditNotes.objects.filter(CancelStatus="csNo", CardCode = CardCode, DocDate__gte = FromDate, DocDate__lte = ToDate).values("id","DocTotal", "CreateDate", "VatSum", "DocEntry", "DocDate", "DiscountPercent", "Comments", "DocNum").order_by('-DocDate')
            else:
                creditNotesList = CreditNotes.objects.filter(CancelStatus="csNo", CardCode = CardCode).values("id","DocTotal", "CreateDate", "VatSum", "DocEntry", "DocDate", "DiscountPercent", "Comments", "DocNum").order_by('-DocDate')

            if len(creditNotesList) != 0:
                if 'PageNo' in request.data:
                    PageNo = int(request.data['PageNo'])
                    MaxSize = request.data['MaxSize']
                    if MaxSize != "All":
                        size = int(MaxSize)
                        endWith = (PageNo * size)
                        startWith = (endWith - size)
                        creditNotesList = creditNotesList[startWith:endWith]
                    
                for creditNote in creditNotesList:
                    # DocTotal = float(creditNote.DocTotal)
                    creditNoteId = creditNote['id']
                    DocEntry = creditNote['DocEntry']
                    DocNum = creditNote['DocNum']
                    DocDate = creditNote['DocDate']
                    DocTotal = float(creditNote['DocTotal'])
                    DiscountPercent = creditNote['DiscountPercent']
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
                    # totalCreditNoteByBP = totalCreditNoteByBP + float(DocTotal)

                    allPaymentsList = allPaymentsList + DocTotal
                    
                    bpData = {
                        "OrderId": DocEntry,
                        "DocEntry": DocNum,
                        "OrderAmount": DocTotal,
                        "CreateDate": DocDate,
                        "Comments": unquote(creditNote['Comments'])
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
    # except Exception as e:
    #     return Response({"message": str(e),"status": 201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])  
def pending_payment_collection(request):
    try:
        all_collection = []
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        # cardCodeList = list(Invoice.objects.filter(DocumentStatus = 'bost_Open').values_list('CardCode', flat=True).distinct())
        # #print("<><><><>< cardCodeList", cardCodeList)
        # bpObjs = BusinessPartner.objects.filter(CardCode__in = cardCodeList).values("id", "CardCode", "CardName")
        # if Invoice.objects.filter(DocumentStatus = 'bost_Open').exists():
        inv_obj = []
        if str(FromDate) != "":
            inv_obj = Invoice.objects.filter(CancelStatus="csNo", DocumentStatus = 'bost_Open', DocDate__gte = FromDate, DocDate__lte = ToDate).order_by('-id')
        else:
            inv_obj = Invoice.objects.filter(CancelStatus="csNo", DocumentStatus = 'bost_Open').order_by('-id')

        if len(inv_obj) > 0:
            if 'PageNo' in request.data:
                PageNo = int(request.data['PageNo'])
                MaxSize = request.data['MaxSize']
                if MaxSize != "All":
                    size = int(MaxSize)
                    endWith = (PageNo * size)
                    startWith = (endWith - size)
                    inv_obj = inv_obj[startWith:endWith]
                    
            for obj in inv_obj:
                InvoiceEntry = obj.DocEntry
                if DocumentLines.objects.filter(InvoiceID = obj.id).exists():

                    itemObj = DocumentLines.objects.filter(InvoiceID = obj.id).values('BaseEntry').first()

                    OrderEntry = itemObj['BaseEntry']
                    CardName = obj.CardName
                    totalOrderAmount = 0
                    if Order.objects.filter(DocEntry = OrderEntry).exists():
                        ord_obj = Order.objects.filter(DocEntry = OrderEntry).first()
                        totalOrderAmount = ord_obj.DocTotal
                        
                    totalInvoiceAmount = float(obj.DocTotal)
                    DocDueDate = datetime.datetime.strptime(obj.DocDueDate, "%Y-%m-%d")
                    CreateDate = datetime.datetime.strptime(obj.CreateDate, "%Y-%m-%d")
                    TodayDate = datetime.datetime.strptime(date, "%Y-%m-%d")

                    PaymentStatus = "Due"
                    DiscountAmount = 0
                    DiscountPercentage = 0
                    dateDifference = (TodayDate - CreateDate).days
                    #print(dateDifference)
                    if dateDifference <= 10:
                        DiscountAmount = (totalInvoiceAmount * 0.04)
                        DiscountPercentage = 4
                    elif (dateDifference >= 11) and (dateDifference <= 20):
                        DiscountAmount = (totalInvoiceAmount * 0.03)
                        DiscountPercentage = 3
                    elif (dateDifference >= 21) and (dateDifference <= 30):
                        DiscountAmount = (totalInvoiceAmount * 0.02)
                        DiscountPercentage = 2
                    elif (dateDifference >= 31) and (dateDifference <= 40):
                        DiscountAmount = (totalInvoiceAmount * 0.01)
                        DiscountPercentage = 1
                    elif TodayDate < DocDueDate:
                        PaymentStatus = "Due"
                    else:
                        PaymentStatus = "Overdue"

                    contaxt = {
                        "InvoiceNo": InvoiceEntry,
                        "OrderNo": OrderEntry, 
                        "CustomerName": CardName,
                        "OrderAmount": totalOrderAmount, 
                        "InvoiceAmount": totalInvoiceAmount,
                        "PaymentDueDate": DocDueDate.date(),
                        "CreateDate": CreateDate.date(),
                        "DiscountAmount": DiscountAmount,
                        "DiscountPercentage": DiscountPercentage,
                        "PaymentStatus": PaymentStatus
                    }
                    all_collection.append(contaxt)
                    
        return Response({"message":"successful","status":"200","data":all_collection})
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def bp_wise_sold_items(request):
    try:
        contaxt = {}
        CardCode = request.data['CardCode']
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']

        if BusinessPartner.objects.filter(CardCode = CardCode).exists():
            invoiceIDs = []
            if str(FromDate) != "":
                invoiceIDs = Invoice.objects.filter(CardCode = CardCode, DocDate__gte = FromDate, DocDate__lte = ToDate).values_list('id', flat=True)
            else:
                invoiceIDs = Invoice.objects.filter(CardCode = CardCode).values_list('id', flat=True)

            itemCodes = DocumentLines.objects.filter(InvoiceID__in = invoiceIDs).values_list('ItemCode', flat=True).distinct()
            if 'PageNo' in request.data:
                PageNo = int(request.data['PageNo'])
                MaxSize = request.data['MaxSize']
                if MaxSize != "All":
                    size = int(MaxSize)
                    endWith = (PageNo * size)
                    startWith = (endWith - size)
                    itemCodes = itemCodes[startWith:endWith]

            itemList = []
            for code in itemCodes:
                itms = DocumentLines.objects.filter(InvoiceID__in = invoiceIDs, ItemCode = code).order_by('id')
                ItemQuantity = 0
                InvoiceID = 0
                ItemOrderList = []
                LastSoldDate = ""
                for itm in itms:
                    ItemQuantity = ItemQuantity + int(itm.Quantity)
                    InvoiceID = itm.InvoiceID
                    # createDate = Invoice.objects.filter(pk = InvoiceID).values_list('DocDate', flat=True).first()
                    inv_obj = Invoice.objects.filter(pk = InvoiceID).first()
                    itemOrder = {
                        "OrderId": inv_obj.DocEntry,
                        "UnitPirce": itm.UnitPrice,
                        "SoldDate":str(inv_obj.DocDate),
                        "TotalQty": ItemQuantity,
                    }
                    ItemOrderList.append(itemOrder)
                    LastSoldDate = inv_obj.DocDate


                tempContaxt = {
                    "ItemName": itms[0].ItemDescription,
                    "ItemCode": itms[0].ItemCode,
                    "UnitPirce": itms[0].UnitPrice,
                    "LastSoldDate":LastSoldDate,
                    "TotalQty": ItemQuantity,
                    "ItemOrderList": ItemOrderList
                }
                itemList.append(tempContaxt)

            return Response({"message":"Success","status":200,"data":itemList}) 
        else:            
            return Response({"message":"Invalid CardCode","status":201,"data":[]}) 
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# update Category Invoice and Uom
@api_view(['GET'])
def syncInvoice(request):
    # try:
        # Import and sync Invoice
        invoiceFile ="Invoice/INV.py"
        exec(compile(open(invoiceFile, "rb").read(), invoiceFile, 'exec'), {})
        
        # Import and sync Invoice recive payment
        incomingPayments ="Invoice/inv_incoming_payments.py"
        exec(compile(open(incomingPayments, "rb").read(), incomingPayments, 'exec'), {})
       
        # Import and sync Invoice return items or credit note
        creditNotes ="Invoice/inv_credit_notes.py"
        exec(compile(open(creditNotes, "rb").read(), creditNotes, 'exec'), {})

        return Response({"message":"Successful","status":200, "data":[]})
    # except Exception as e:
    #     return Response({"message":str(e),"status":201,"Model": "Invoice" ,"data":[]})


def showIncomingPayments(objs):
    allIncomingPayments = []
    for obj in objs:
        paymentObj = IncomingPaymentsSerializer(obj, many=False)
        finalIncomingPayment = json.loads(json.dumps(paymentObj.data))
        ################################addedd################################
        BPLID = obj.BPLID
        if Branch.objects.filter(BPLId=BPLID).exists():
            branch_obj = Branch.objects.filter(BPLId=BPLID).first()
            finalIncomingPayment["BPLName"] = branch_obj.BPLName
            finalIncomingPayment["Address"] = unquote(branch_obj.Address)
            finalIncomingPayment["State"] = branch_obj.State
            finalIncomingPayment["TaxIdNum"] = branch_obj.TaxIdNum
            finalIncomingPayment["Branch_GSTIN"] = branch_obj.FederalTaxID
        else:
            finalIncomingPayment["BPLName"] = ""
            finalIncomingPayment["Address"] = ""
            finalIncomingPayment["State"] = ""
            finalIncomingPayment["TaxIdNum"] = ""
            finalIncomingPayment["Branch_GSTIN"] = ""
        ################################addedd################################

        if IncomingPaymentInvoices.objects.filter(IncomingPaymentsId = obj.id).exists():
            invObjs = IncomingPaymentInvoices.objects.filter(IncomingPaymentsId = obj.id)
            invJson = IncomingPaymentInvoicesSerializer(invObjs, many=True)
            finalIncomingPayment['IncomingPaymentInvoices'] = invJson.data
        else:
            finalIncomingPayment['IncomingPaymentInvoices'] = []
        allIncomingPayments.append(finalIncomingPayment)

    return allIncomingPayments