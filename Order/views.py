from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse

from BusinessPartner.models import BPEmployee, BusinessPartner
from BusinessPartner.serializers import BPEmployeeSerializer
from Employee.serializers import EmployeeSerializer
from PaymentTermsTypes.models import PaymentTermsTypes
from PaymentTermsTypes.serializers import PaymentTermsTypesSerializer
from Item.models import UoMList
from Company.models import Branch
from .models import *
from Employee.models import Employee

import requests, json

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import *
from rest_framework.parsers import JSONParser

from pytz import timezone
from datetime import datetime as dt

date = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d')
yearmonth = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m')
time = dt.now(timezone("Asia/Kolkata")).strftime('%H:%M %p')

import os
from django.core.files.storage import FileSystemStorage
from Attachment.models import Attachment
from Attachment.serializers import AttachmentSerializer

# import setting file
from django.conf import settings
from django.db.models import Q
# Create your views here.

from datetime import date, datetime, timedelta
# tz = pytz.timezone('Asia/Kolkata')
currentDate = date.today()

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# custome function import
from global_methods import employeeViewAccess, findTodaysUnitSales, findTodaysUnitSalesByBP, getAllReportingToIds
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#Order Create API
@api_view(['POST'])
def create(request):
    orderId = 0
    try:
    # if True:
        TaxDate = request.data['TaxDate']
        DocDueDate = request.data['DocDueDate']
        ContactPersonCode = request.data['ContactPersonCode']
        DiscountPercent = request.data['DiscountPercent']
        DocDate = request.data['DocDate']
        CardCode = request.data['CardCode']
        CardName = request.data['CardName']
        Comments = request.data['Comments']
        SalesPersonCode = request.data['SalesPersonCode']

        U_QUOTNM = request.data['U_QUOTNM']
        U_QUOTID = request.data['U_QUOTID']
        U_OPPID = request.data['U_OPPID']
        U_OPPRNM = request.data['U_OPPRNM']
        
        CreateDate = request.data['CreateDate']
        CreateTime = request.data['CreateTime']
        UpdateDate = request.data['UpdateDate']
        UpdateTime = request.data['UpdateTime']

        PaymentType = request.data['PaymentType']
        DeliveryMode = request.data['DeliveryMode']
        DeliveryTerm = request.data['DeliveryTerm']
        AdditionalCharges = request.data['AdditionalCharges']
        TermCondition = request.data['TermCondition']
        DeliveryCharge = request.data['DeliveryCharge']
        Unit = request.data['Unit']
        U_LAT = request.data['U_LAT']
        U_LONG = request.data['U_LONG']
        Link = request.data['Link']
        PayTermsGrpCode = request.data['PayTermsGrpCode']
        FreeDelivery = request.data['FreeDelivery']
        CreatedBy = request.data['CreatedBy']

        lines = request.data['DocumentLines']
        # <><><><><><><><><><><><><><><><><><><><>
        
        # <><><><><><><><><><><><><><><><><><><><>
        DocTotal=0
        for line in lines:
            DocTotal = float(DocTotal) + float(line['Quantity']) * float(line['UnitPriceown'])
        print(DocTotal)
        # <><><><><><><><><><><><><><><><><><><><>
        
        # <><><><><><><><><><><><><><><><><><><><>
        # if BusinessPartner.objects.filter(CardCode = CardCode).exists():
        #     bpObj = BusinessPartner.objects.get(CardCode = CardCode)
        #     if float(bpObj.CreditLimitLeft) > 0:
        #         if float(DocTotal) > float(bpObj.CreditLimitLeft):
        #             return Response({"message":"BP Credit limit exceeded","status":201,"data":[]})
        #         else:
        #             pass
        #     else:
        #         return Response({"message":"BP Credit limit exceeded","status":201,"data":[]})
        # else:
        #     return Response({"message":"Invalid CardCode","status":201,"data":[]})
        # <><>>><><><><><><><><><><><><><><<>>
        # Order Create
        # <><>>><><><><><><><><><><><><><><<>>
        model=Order(CancelStatus='csNo', TaxDate = TaxDate, DocDueDate = DocDueDate, ContactPersonCode = ContactPersonCode, DiscountPercent = DiscountPercent, DocDate = DocDate, CardCode = CardCode, CardName = CardName, Comments = Comments, SalesPersonCode = SalesPersonCode, DocumentStatus="bost_Open", DocTotal = DocTotal, CreateDate = CreateDate, CreateTime = CreateTime, UpdateDate = UpdateDate, UpdateTime = UpdateTime, U_QUOTNM = U_QUOTNM, U_QUOTID = U_QUOTID, U_OPPID = U_OPPID, U_OPPRNM = U_OPPRNM, NetTotal=DocTotal, PaymentType = PaymentType, DeliveryMode = DeliveryMode, DeliveryTerm = DeliveryTerm, AdditionalCharges = AdditionalCharges, TermCondition = TermCondition, DeliveryCharge = DeliveryCharge, Unit = Unit, U_LAT = U_LAT, U_LONG = U_LONG, Link = Link, PayTermsGrpCode = PayTermsGrpCode, FreeDelivery = FreeDelivery, CreatedBy = CreatedBy)
        model.save()

        qt = Order.objects.latest('id')    
        orderId = qt.id
        # model.DocEntry = orderId
        # model.save()

        # <><>>><><><><><><><><><><><><><><>><>
        # AddressExtension 
        # <><>>><><><><><><><><><><><><><><>><>
        addr = request.data['AddressExtension']
        model_add = AddressExtension(OrderID = orderId, BillToBuilding = addr['BillToBuilding'], ShipToState = addr['ShipToState'], BillToCity = addr['BillToCity'], ShipToCountry = addr['ShipToCountry'], BillToZipCode = addr['BillToZipCode'], ShipToStreet = addr['ShipToStreet'], BillToState = addr['BillToState'], ShipToZipCode = addr['ShipToZipCode'], BillToStreet = addr['BillToStreet'], ShipToBuilding = addr['ShipToBuilding'], ShipToCity = addr['ShipToCity'], BillToCountry = addr['BillToCountry'], U_SCOUNTRY = addr['U_SCOUNTRY'], U_SSTATE = addr['U_SSTATE'], U_SHPTYPB = addr['U_SHPTYPB'], U_BSTATE = addr['U_BSTATE'], U_BCOUNTRY = addr['U_BCOUNTRY'], U_SHPTYPS = addr['U_SHPTYPS'],ShipToDistrict = addr['ShipToDistrict'], BillToDistrict = addr['BillToDistrict'])
        model_add.save()

        # <><>>><><><><><><><><><><><><><><>><>
        # DocumentLines
        # <><>>><><><><><><><><><><><><><><>><>
        LineNum = 0
        orderSalesinKG = 0
        newLines = []
        for line in lines:
            model_lines = DocumentLines(LineNum = LineNum, OrderID = orderId, Quantity = line['Quantity'], UnitPrice = line['UnitPrice'], DiscountPercent = line['DiscountPercent'], ItemCode = line['ItemCode'], ItemDescription = line['ItemDescription'], TaxCode = line['TaxCode'], FreeText = line['FreeText'], UomNo = line['UomNo'], UnitWeight = line['UnitWeight'], UnitPriceown = line['UnitPriceown'])
            model_lines.save()
            LineNum=LineNum+1
            orderSalesinKG = (orderSalesinKG + (float(line['UnitWeight']) * int(line['Quantity'])))
            # uomObj = UoMList.objects.get(Name = line['UomNo'])
            line['UnitPrice'] = line['UnitPriceown']
            line['UoMCode'] = line['UomNo']
            # line['UoMEntry'] = uomObj.AbsEntry
            line.pop('UnitPriceown', None)
            line.pop('UomNo', None)
            newLines.append(line)
        # <><><><><><><><><><><><><><><><><>
        #  ----- findTodaysUnitSales ------
        # <><><><><><><><><><><><><><><><><>
        # totalSalesInKG = findTodaysUnitSales(Unit)
        totalSalesInKG = findTodaysUnitSalesByBP(Unit, CardCode)
        tempTotal = float(float(orderSalesinKG) + float(totalSalesInKG))
        maxSalesLimit = 25000 #1000kg = 1Tonne
        if tempTotal > maxSalesLimit:
            Order.objects.filter(pk = orderId).update(ApprovalStatus = 'Pending')
            return Response({"message":"successful","status":200,"data":[{"qt_Id":orderId}]})
        else:
            pass
        # endif

        Series = 90
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        if Branch.objects.filter(BPLId = Unit).exists():
            branchObj = Branch.objects.get(BPLId = Unit)
            Series = branchObj.Series
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        # <><><><><><><><><><><><><><><>
        #  ----- SAP DATA PUSH ------
        # <><><><><><><><><><><><><><><>
        qt_data = {
            "TaxDate": request.data['TaxDate'],
            "DocDueDate": request.data['DocDueDate'],
            "DocDate": request.data['DocDate'],
            "ContactPersonCode": request.data['ContactPersonCode'],
            "DiscountPercent": request.data['DiscountPercent'],
            "CardCode": request.data['CardCode'],
            "CardName": request.data['CardName'],
            "Comments": request.data['Comments'],
            "SalesPersonCode": request.data['SalesPersonCode'],
            "BPL_IDAssignedToInvoice": Unit, #default only one branch exist in SAP
            # "BPL_IDAssignedToInvoice": 3, #default only one branch exist in SAP
            "PaymentGroupCode":request.data['PayTermsGrpCode'],
            "U_UTL_FOLD": request.data['DocDate'],
            "Series": Series,
            # "U_PORTAL_NO":qt.id,
            "AddressExtension": {
                "BillToBuilding": request.data['AddressExtension']['BillToBuilding'],
                "ShipToState": request.data['AddressExtension']['ShipToState'],
                "BillToCity": request.data['AddressExtension']['BillToCity'],
                "ShipToCountry": request.data['AddressExtension']['ShipToCountry'],
                "BillToZipCode": request.data['AddressExtension']['BillToZipCode'],
                "ShipToStreet": request.data['AddressExtension']['ShipToStreet'],
                "BillToState": request.data['AddressExtension']['BillToState'],
                "ShipToZipCode": request.data['AddressExtension']['ShipToZipCode'],
                "BillToStreet": request.data['AddressExtension']['BillToStreet'],
                "ShipToBuilding": request.data['AddressExtension']['ShipToBuilding'],
                "ShipToCity": request.data['AddressExtension']['ShipToCity'],
                "BillToCountry": request.data['AddressExtension']['BillToCountry'],
                # "U_SCOUNTRYS": request.data['AddressExtension']['U_SCOUNTRY'],
                # "U_SSTATES": request.data['AddressExtension']['U_SSTATE'],
                # "U_SHPTYPSS": request.data['AddressExtension']['U_SHPTYPS'],
                # "U_BSTATEB": request.data['AddressExtension']['U_BSTATE'],
                # "U_BCOUNTRYB": request.data['AddressExtension']['U_BCOUNTRY'],
                # "U_SHPTYPBB": request.data['AddressExtension']['U_SHPTYPB'],
                "PlaceOfSupply": addr['ShipToState']
            },
            # "DocumentLines": lines
            "DocumentLines": newLines,
            "DocumentAdditionalExpenses":[
                {
                    "ExpenseCode": 1,
                    "TaxCode": "CSGST18",
                    "LineTotal": request.data['DeliveryCharge']
                },
                {
                    "ExpenseCode": 2,
                    "TaxCode": "CSGST18",
                    "LineTotal": request.data['AdditionalCharges']
                }
            ]
        }
        
        print(">>>>>>>>>>>>>>>>>>>>>>>>")
        res = settings.CALLAPI('post', '/Orders', 'api', qt_data)
        live = json.loads(res.text)
        if "DocEntry" in live:
            print(live['DocEntry'])
            DocEntry = live['DocEntry']
            
            model = Order.objects.get(pk = orderId)
            model.DocEntry = DocEntry
            model.VatSum = live['VatSum']
            model.DocTotal = live['DocTotal']
            model.save()

            documentLines = live['DocumentLines']
            # print(documentLines)
            for docline in documentLines:
                LineNum = docline['LineNum']
                TaxCode = docline['TaxCode']
                TaxRate = docline['TaxPercentagePerRow']

                if DocumentLines.objects.filter(OrderID = orderId, LineNum = LineNum).exists():
                    DocumentLines.objects.filter(OrderID = orderId, LineNum = LineNum).update(TaxCode = TaxCode, TaxRate = TaxRate)

            
            res = settings.CALLAPI('get', f"/BusinessPartners('{CardCode}')", 'api', '')
            resData = json.loads(res.text)
            if 'odata.metadata' in resData:
                print("CreditLimit: ", resData['CreditLimit'])

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

            return Response({"message":"successful","status":200,"data":[{"qt_Id":orderId, "DocEntry":DocEntry, "qt_data": qt_data}]})
        else:
            SAP_MSG = live['error']['message']['value']
            print(SAP_MSG)
            AddressExtension.objects.filter(OrderID = orderId).delete()
            DocumentLines.objects.filter(OrderID = orderId).delete()
            Order.objects.filter(pk=orderId).delete()
            return Response({"message":SAP_MSG,"SAP_error":SAP_MSG, "status":202,"data":[{"qt_data": qt_data}]})
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # return Response({"message":"successful","status":200,"data":[{"qt_Id":orderId, "DocEntry":orderId}]})

    except Exception as e:
        if Order.objects.filter(pk=orderId).exists():
            AddressExtension.objects.filter(OrderID = orderId).delete()
            DocumentLines.objects.filter(OrderID = orderId).delete()
            Order.objects.filter(pk=orderId).delete()
        return Response({"message":"Not Created","status":201,"data":[{"Error":str(e)}]})


#Order Update API
@api_view(['POST'])
def update(request):
    fetchid = request.data['id']
    try:
        model = Order.objects.get(pk = fetchid)

        model.TaxDate = request.data['TaxDate']
        model.DocDate = request.data['DocDate']
        model.DocDueDate = request.data['DocDueDate']
        
        model.ContactPersonCode = request.data['ContactPersonCode']
        model.DiscountPercent = request.data['DiscountPercent']
        model.Comments = request.data['Comments']
        model.SalesPersonCode = request.data['SalesPersonCode']
        
        model.UpdateDate = request.data['UpdateDate']
        model.UpdateTime = request.data['UpdateTime']

        model.PaymentType = request.data['PaymentType']
        model.DeliveryMode = request.data['DeliveryMode']
        model.DeliveryTerm = request.data['DeliveryTerm']
        model.AdditionalCharges = request.data['AdditionalCharges']
        model.TermCondition = request.data['TermCondition']
        model.DeliveryCharge = request.data['DeliveryCharge']
        model.Unit = request.data['Unit']
        model.U_LAT = request.data['U_LAT']
        model.U_LONG = request.data['U_LONG']
        model.Link = request.data['Link']
        model.PayTermsGrpCode = request.data['PayTermsGrpCode']
        model.FreeDelivery = request.data['FreeDelivery']

        model.save()
        
        model_add = AddressExtension.objects.get(id = request.data['AddressExtension']['id'])
        print(model_add)
        
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
        model_add.ShipToDistrict = request.data['AddressExtension']['ShipToDistrict']
        model_add.BillToDistrict = request.data['AddressExtension']['BillToDistrict']
   
        model_add.save()
        print("add save")
        
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
                model_line.FreeText=line['FreeText']
                model_line.UomNo=line['UomNo']
                model_line.UnitWeight=line['UnitWeight']          
                model_line.save()
            else:
                lastline = DocumentLines.objects.filter(OrderID = fetchid).order_by('-LineNum')[:1]
                NewLine = int(lastline[0].LineNum) + 1
                model_lines = DocumentLines(OrderID = fetchid, LineNum=NewLine, Quantity = line['Quantity'], UnitPrice = line['UnitPrice'], DiscountPercent = line['DiscountPercent'], ItemCode = line['ItemCode'], ItemDescription = line['ItemDescription'], TaxCode = line['TaxCode'], FreeText = line['FreeText'], UomNo = line['UomNo'], UnitWeight = line['UnitWeight'])
                model_lines.save()
            
        return Response({"message":"successful","status":200, "data":[request.data]})
    except Exception as e:
        return Response({"message":"Not Update","status":201,"data":[{"Error":str(e)}]})

def OrderShow(Orders_obj):
    allqt = [];
    for qt in Orders_obj:
        qtaddr = AddressExtension.objects.filter(OrderID=qt.id)
        
        qtaddr_json = AddressExtensionSerializer(qtaddr, many=True)
        
        jss_ = json.loads(json.dumps(qtaddr_json.data))
        for j in jss_:
            jss0=j
        
        lines = DocumentLines.objects.filter(OrderID=qt.id)
        
        lines_json = DocumentLinesSerializer(lines, many=True)
        
        jss1 = json.loads(json.dumps(lines_json.data))
        
        context = {
            'id':qt.id,
            'DocEntry':qt.DocEntry,
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
        print("yes")
        
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
            
            print(SalesEmployeeCode)

            if json_data['Type'] =="over":
                ord = Order.objects.filter(SalesPersonCode__in=SalesEmployeeCode, DocumentStatus="bost_Open", DocDueDate__lt=date)
                allord = OrderShow(ord)
                #print(allord)
            elif json_data['Type'] =="open":
                ord = Order.objects.filter(SalesPersonCode__in=SalesEmployeeCode, DocumentStatus="bost_Open", DocDueDate__gte=date)
                allord = OrderShow(ord)
                #print(allord)
            else:
                ord = Order.objects.filter(SalesPersonCode__in=SalesEmployeeCode, DocumentStatus="bost_Close")
                allord = OrderShow(ord)
                #print(allord)
			
            #{"SalesEmployeeCode":"2"}
            return Response({"message": "Success","status": 200,"data":allord})
            
            #return Response({"message": "Success","status": 201,"data":[{"emp":SalesEmployeeCode}]})
        else:
            return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})
    else:
        return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})
	
#Quotation All API
@api_view(["POST"])
def all_filter(request):
    json_data = request.data
    
    # if "U_OPPID" in json_data:
        # if json_data['U_OPPID'] !='':
            # quot_obj = Quotation.objects.filter(U_OPPID=json_data['U_OPPID']).order_by("-id")
            # if len(quot_obj) ==0:
                # return Response({"message": "Not Available","status": 201,"data":[]})
            # else:
                # allqt = QuotationShow(quot_obj)
            # return Response({"message": "Success","status": 200,"data":allqt})
            
    if "SalesPersonCode" in json_data:
        print("yes")
        
        if json_data['SalesPersonCode']!="":
            SalesPersonID = json_data['SalesPersonCode']

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            empList = employeeViewAccess(SalesPersonID)
            # empList = getAllReportingToIds(SalesPersonID)
            print(empList)
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            
            for ke in json_data.keys():
                if ke =='U_FAV' :
                    print("yes filter")
                    if json_data['U_FAV'] !='':
                        quot_obj = Order.objects.filter(SalesPersonCode__in=empList, U_FAV=json_data['U_FAV']).order_by("-id")
                        if len(quot_obj) ==0:
                            return Response({"message": "Not Available","status": 201,"data":[]})
                        else:
                            allqt = showOrder(quot_obj)
                            return Response({"message": "Success","status": 200,"data":allqt})

                # elif ke =='U_TYPE' :
                    # if json_data['U_TYPE'] !='':
                        # quot_obj = Quotation.objects.filter(SalesPersonCode__in=empList, U_TYPE=json_data['U_TYPE']).order_by("-id")
                        # if len(quot_obj) ==0:
                            # return Response({"message": "Not Available","status": 201,"data":[]})
                        # else:
                            # quot_json = QuotationSerializer(quot_obj, many=True)
                            # return Response({"message": "Success","status": 200,"data":quot_json.data})
                # elif ke =='Status' :
                    # if json_data['Status'] !='':
                        # quot_obj = Quotation.objects.filter(SalesPersonCode__in=empList, Status=json_data['Status']).order_by("-id")
                        # if len(quot_obj) ==0:
                            # return Response({"message": "Not Available","status": 201,"data":[]})
                        # else:
                            # quot_json = QuotationSerializer(quot_obj, many=True)
                            # return Response({"message": "Success","status": 200,"data":quot_json.data})
                
                else:
                    print("no filter")
                    # qt = Quotation.objects.filter(SalesPersonCode__in=empList).order_by("-id")
                    # quot_json = QuotationSerializer(quot_obj, many=True)
                    # return Response({"message": "Success","status": 200,"data":quot_json.data})
                    quot_obj = Order.objects.filter(Q(SalesPersonCode__in=empList) | Q(CreatedBy__in = empList)).order_by("-id")
                    allqt = showOrder(quot_obj)
                    return Response({"message": "Success","status": 200,"data":allqt})
        else:
            return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesPersonCode?"}]})
    else:
        print("no")
        return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesPersonCode?"}]})
	
#Quotation All API
@api_view(["POST"])
def all_filter_pagination(request):
    try:
        SalesPersonCode = request.data['SalesPersonCode']
        PageNo = int(request.data['PageNo'])
        MaxSize = request.data['MaxSize']
        TotalOrder = 0
        if Employee.objects.filter(SalesEmployeeCode = SalesPersonCode).exists():

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            empList = employeeViewAccess(SalesPersonCode)
            # empList = getAllReportingToIds(SalesPersonID)
            print(empList)
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        
            if MaxSize != "All":
                size = int(MaxSize)
                endWith = (PageNo * size)
                startWith = (endWith - size)
                # quot_obj = quot_obj[startWith:endWith]
                quot_obj = Order.objects.filter(Q(SalesPersonCode__in=empList) | Q(CreatedBy__in = empList)).order_by("-id")[startWith:endWith]
                TotalOrder = len(quot_obj)
            else:
                quot_obj = Order.objects.filter(Q(SalesPersonCode__in=empList) | Q(CreatedBy__in = empList)).order_by("-id")
                TotalOrder = len(quot_obj)

            allqt = showOrder(quot_obj)
            return Response({"message": "Success","status": 200,"data":allqt, "TotalOrder": TotalOrder})
        else:
            return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesPersonCode?"}]})
    except Exception as e:
        print("no")
        return Response({"message": str(e),"status": 201,"data":[]})

#Order All API
@api_view(["GET"])
def all(request):
    # Orders_obj = Order.objects.all().order_by("-id")
    # allqt = OrderShow(Orders_obj)
    # return Response({"message": "Success","status": 200,"data":allqt})
    # print("Units: ", findTodaysUnitSales('hyderabad'))

    order_obj = Order.objects.all().order_by("-id")
    result = showOrder(order_obj)
    
    return Response({"message": "Success","status": 200,"data":result})

#Order One API
@api_view(["POST"])
def one(request):
    id=request.data['id']
    
    # Orders_obj = Order.objects.filter(id=id)
    # allqt = OrderShow(Orders_obj)
    # return Response({"message": "Success","status": 200,"data":allqt})
    
    oneOrder = [];
    order_obj = Order.objects.filter(pk=id)
    result = showOrder(order_obj)
    
    return Response({"message": "Success","status": 200,"data":result})

#Order delete
@api_view(['POST'])
def delete(request):
    fetchid=request.data['id']
    try:
        fetchdata=Order.objects.filter(pk=fetchid).delete()
        return Response({"message":"successful","status":"200","data":[]})        
    except:
        return Response({"message":"Id wrong","status":"201","data":[]})
     
# to get order contact person details and salesEmployeeDetails
def showOrder(objs):
    allOrders = []
    for obj in objs:
        cpcType = obj.ContactPersonCode
        salesType = obj.SalesPersonCode
        createdBy = obj.CreatedBy
        orderId = obj.id
        paymentType = obj.PayTermsGrpCode
        orderjson = OrderSerializer(obj)
        finalOrderData = json.loads(json.dumps(orderjson.data))
        finalOrderData['NetTotal'] = round(float(float(obj.DocTotal) - float(obj.VatSum)), 2)
        if cpcType != "":
            cpcTypeObj = BPEmployee.objects.filter(InternalCode = cpcType).values("id","FirstName","E_Mail", "MobilePhone")  #updated by millan on 15-09-2022
            cpcTypejson = BPEmployeeSerializer(cpcTypeObj, many = True)
            finalOrderData['ContactPersonCode']=json.loads(json.dumps(cpcTypejson.data))
        else:
            finalOrderData['ContactPersonCode']=[]
            
        if salesType != "" :
            salesTypeObj = Employee.objects.filter(SalesEmployeeCode = salesType).values("id", "SalesEmployeeCode", "SalesEmployeeName", "Email", "Mobile")
            salesTypejson = EmployeeSerializer(salesTypeObj, many=True)
            finalOrderData['SalesPersonCode'] = json.loads(json.dumps(salesTypejson.data))
        else:
            finalOrderData['SalesPersonCode']
        
        if createdBy != "" :
            salesTypeObj = Employee.objects.filter(SalesEmployeeCode = createdBy).values("id", "SalesEmployeeCode", "SalesEmployeeName", "Email", "Mobile")
            salesTypejson = EmployeeSerializer(salesTypeObj, many=True)
            finalOrderData['CreatedBy'] = json.loads(json.dumps(salesTypejson.data))
        else:
            finalOrderData['CreatedBy']
        
        if orderId != "" :
            #addrObj = AddressExtension.objects.filter(OrderID = orderId)
            #addrjson = AddressExtensionSerializer(addrObj, many=True)
            
            addrObj = AddressExtension.objects.get(OrderID = orderId)
            addrjson = AddressExtensionSerializer(addrObj)
            
            linesobj = DocumentLines.objects.filter(OrderID=orderId)
            lines_json = DocumentLinesSerializer(linesobj, many=True)
            
            finalOrderData['AddressExtension'] = json.loads(json.dumps(addrjson.data))
            
            finalOrderData['DocumentLines'] = json.loads(json.dumps(lines_json.data))
            
        else:
            finalOrderData['AddressExtension'] = {}
            finalOrderData['DocumentLines'] = []   
            
        if Attachment.objects.filter(LinkID = obj.id, LinkType="Order").exists():
            Attach_dls = Attachment.objects.filter(LinkID = obj.id, LinkType="Order")
            Attach_json = AttachmentSerializer(Attach_dls, many=True)
            finalOrderData['Attach'] = Attach_json.data
        else:
            finalOrderData['Attach'] = []

        if paymentType != "":
            paymentTypeObj = PaymentTermsTypes.objects.filter(GroupNumber = paymentType)
            paymentjson = PaymentTermsTypesSerializer(paymentTypeObj, many = True)
            finalOrderData['PayTermsGrpCode'] = json.loads(json.dumps(paymentjson.data))
        else:
            finalOrderData['PayTermsGrpCode'] = []
        
        allOrders.append(finalOrderData)
    
    return allOrders


#added by millan on 10-November-2022 for adding attachment
@api_view(["POST"])
def ord_attachment_create(request):
    try:
        orderId = request.data['orderId']
        CreateDate = request.data['CreateDate']
        CreateTime = request.data['CreateTime']

        for File in request.FILES.getlist('Attach'):
            attachmentsImage_url = ""
            target ='./bridge/static/image/OrderAttachment'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+File.name, File)
            file_size = os.stat(file)
            Size = file_size.st_size
            productImage_url = fss.url(file)
            attachmentsImage_url = productImage_url.replace('/bridge', '')

            att=Attachment(File=attachmentsImage_url, LinkID=orderId, CreateDate=CreateDate, CreateTime=CreateTime, Size=Size, LinkType='Order')
            
            att.save()  
            
        return Response({"message": "success","status": 200,"data":[]})
    except Exception as e:
        return Response({"message": "Error","status": 201,"data":str(e)})

#added by millan on 10-November-2022 for deleting an attachment
@api_view(['POST'])
def ord_attachment_delete(request):
    try:
        fetchid = request.data['id']
        
        ordId = request.data['ordId']
        
        if Attachment.objects.filter(LinkID=ordId, LinkType='Order', pk = fetchid).exists():
            Attachment.objects.filter(LinkID=ordId, LinkType='Order', pk = fetchid).delete()
            return Response({"message":"successful","status":"200","data":[]})
        else:
            return Response({"message":"ID Not Found","status":"201","data":[]})
        
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#
#
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Order top 5 order by salesperson
@api_view(["POST"])
def top5Order(request):
    try:
        SalesPersonCode = request.data['SalesPersonCode']
        empIds = getAllReportingToIds(SalesPersonCode)
        order_obj = Order.objects.filter(SalesPersonCode__in = empIds).order_by("-id")[0:5]
        result = showOrder(order_obj)
        return Response({"message": "Success","status": 200,"data":result})
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#
#
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Order Update API
@api_view(['POST'])
def approve(request):
    try:
        SalesEmployeeCode = request.data['SalesEmployeeCode']
        OrderID = request.data['OrderID']
        ApprovalStatus = request.data['ApprovalStatus']
        Remarks = request.data['Remarks']
        
        if Order.objects.filter(pk = OrderID).exists():
            if Employee.objects.filter(SalesEmployeeCode = SalesEmployeeCode).exists():
                
                # employee objs
                empObj = Employee.objects.get(SalesEmployeeCode = SalesEmployeeCode)
                orderObj = Order.objects.get(pk = OrderID)

                if str(orderObj.ApprovalStatus) == str(ApprovalStatus):
                    remarkobj = OrderStatusRemarks(
                        OrderID = OrderID,
                        SalesEmployeeCode = SalesEmployeeCode,
                        Status = ApprovalStatus,
                        Remarks = Remarks,
                    ).save()
                    return Response({"message":"Success","status":200,"data":[]})
                else:
                    pass

                # if str(empObj.unit).lower() ==  str(orderObj.Unit).lower():
                rolesArray = ["admin", "director", "unit head"]
                if str(empObj.role).lower() in rolesArray:
                    if str(ApprovalStatus).strip() == 'Approved':
                        # print("in if roles", str(empObj.role).lower())
                        orderObj.ApproverId = SalesEmployeeCode
                        orderObj.ApprovalStatus = ApprovalStatus
                        orderObj.save()
                        
                        remarkobj = OrderStatusRemarks(
                            OrderID = OrderID,
                            SalesEmployeeCode = SalesEmployeeCode,
                            Status = ApprovalStatus,
                            Remarks = Remarks,
                        ).save()
                        # if the order got approve then Order DocDueDate will be plus 2 day from the date of approved

                        print("in if", str(ApprovalStatus).strip())
                        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                        dueDate = currentDate + timedelta(days=2)
                        Order.objects.filter(pk = OrderID).update(DocDueDate = str(dueDate))
                        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                        
                        addressObj = AddressExtension.objects.filter(OrderID = OrderID)[0]
                        itemObj = DocumentLines.objects.filter(OrderID = OrderID)
                        itemJson = DocumentLinesSerializer(itemObj, many=True)
                        newLines = []
                        itemLine = json.loads(json.dumps(itemJson.data))
                        for line in itemLine:
                            
                            # uomObj = UoMList.objects.get(Name = line['UomNo'])
                            line['UnitPrice'] = line['UnitPriceown']
                            line['UoMCode'] = line['UomNo']
                            # line['UoMEntry'] = uomObj.AbsEntry
                            line.pop('UnitPriceown', None)
                            line.pop('UomNo', None)
                            newLines.append(line)

                        DocEntry = 0
                        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                        qt_data = {
                            "TaxDate": orderObj.TaxDate,
                            "DocDueDate": orderObj.DocDueDate,
                            "DocDate": orderObj.DocDate,
                            "ContactPersonCode": orderObj.ContactPersonCode,
                            "DiscountPercent": orderObj.DiscountPercent,
                            "CardCode": orderObj.CardCode,
                            "CardName": orderObj.CardName,
                            "Comments": orderObj.Comments,
                            "SalesPersonCode": orderObj.SalesPersonCode,
                            "BPL_IDAssignedToInvoice": 5, #default only one branch exist in SAP
                            "PaymentGroupCode":orderObj.PayTermsGrpCode,
                            # "U_PORTAL_NO":qt.id,
                            "AddressExtension": {
                                "BillToBuilding": addressObj.BillToBuilding,
                                "ShipToState": addressObj.ShipToState,
                                "BillToCity": addressObj.BillToCity,
                                "ShipToCountry": addressObj.ShipToCountry,
                                "BillToZipCode": addressObj.BillToZipCode,
                                "ShipToStreet": addressObj.ShipToStreet,
                                "BillToState": addressObj.BillToState,
                                "ShipToZipCode": addressObj.ShipToZipCode,
                                "BillToStreet": addressObj.BillToStreet,
                                "ShipToBuilding": addressObj.ShipToBuilding,
                                "ShipToCity": addressObj.ShipToCity,
                                "BillToCountry": addressObj.BillToCountry,
                                # "U_SCOUNTRYS": request.data['AddressExtension']['U_SCOUNTRY'],
                                # "U_SSTATES": request.data['AddressExtension']['U_SSTATE'],
                                # "U_SHPTYPSS": request.data['AddressExtension']['U_SHPTYPS'],
                                # "U_BSTATEB": request.data['AddressExtension']['U_BSTATE'],
                                # "U_BCOUNTRYB": request.data['AddressExtension']['U_BCOUNTRY'],
                                # "U_SHPTYPBB": request.data['AddressExtension']['U_SHPTYPB'],
                                "PlaceOfSupply": addressObj.ShipToState
                            },
                            # "DocumentLines": json.loads(json.dumps(itemJson.data))
                            "DocumentLines": newLines
                        }

                        print(qt_data)
                        
                        print(">>>>>>>>>>>>>>>>>>>>>>>>")

                        res = settings.CALLAPI('post', '/Orders', 'api', qt_data)
                        live = json.loads(res.text)
                        if "DocEntry" in live:
                            print(live['DocEntry'])
                            DocEntry = live['DocEntry']
                            
                            model = Order.objects.get(pk = OrderID)
                            model.DocEntry = DocEntry
                            model.save()

                            documentLines = live['DocumentLines']
                            # print(documentLines)
                            for docline in documentLines:
                                LineNum = docline['LineNum']
                                TaxCode = docline['TaxCode']
                                TaxRate = docline['TaxPercentagePerRow']

                                if DocumentLines.objects.filter(OrderID = OrderID, LineNum = LineNum).exists():
                                    DocumentLines.objects.filter(OrderID = OrderID, LineNum = LineNum).update(TaxCode = TaxCode, TaxRate = TaxRate)
                                # endif
                            # endfor

                            res = settings.CALLAPI('get', f"/BusinessPartners('{orderObj.CardCode}')", 'api', '')
                            resData = json.loads(res.text)
                            if 'odata.metadata' in resData:
                                print("CreditLimit: ", resData['CreditLimit'])

                                updatedCreditLimit = float(resData['CreditLimit'])
                                CurrentAccountBalance = resData['CurrentAccountBalance']
                                OpenDeliveryNotesBalance = resData['OpenDeliveryNotesBalance']
                                OpenOrdersBalance = resData['OpenOrdersBalance']
                                OpenChecksBalance = resData['OpenChecksBalance'] # not in currently used

                                totalCreditLimitUsed = float(float(CurrentAccountBalance) + float(OpenDeliveryNotesBalance) + float(OpenOrdersBalance))
                                newLeftCreditLimit = float(updatedCreditLimit - totalCreditLimitUsed)
                                BusinessPartner.objects.filter(CardCode = orderObj.CardCode).update(
                                    CreditLimit = updatedCreditLimit,
                                    CreditLimitLeft = newLeftCreditLimit,
                                    CurrentAccountBalance = CurrentAccountBalance,
                                    OpenDeliveryNotesBalance = OpenDeliveryNotesBalance,
                                    OpenOrdersBalance = OpenOrdersBalance,
                                    OpenChecksBalance = OpenChecksBalance
                                )

                            return Response({"message":"Success","status":200,"data":[{"qt_data": qt_data}]})
                        else:
                            SAP_MSG = live['error']['message']['value']
                            print(SAP_MSG)
                            return Response({"message":SAP_MSG,"SAP_error":SAP_MSG, "status":202,"data":[{"qt_data": qt_data}]})
                    # endif
                    else:
                        orderObj.ApproverId = SalesEmployeeCode
                        orderObj.ApprovalStatus = ApprovalStatus
                        orderObj.save()
                        
                        # print("in else", str(ApprovalStatus).strip())
                        # return Response({"message":"Invalid Approval status","status":201,"data":[]})
                        remarkobj = OrderStatusRemarks(
                            OrderID = OrderID,
                            SalesEmployeeCode = SalesEmployeeCode,
                            Status = orderObj.ApprovalStatus,
                            Remarks = Remarks,
                        ).save()
                        return Response({"message":"Success","status":200,"data":[]})
                else:
                    # print("in else roles", str(empObj.role).lower())
                    remarkobj = OrderStatusRemarks(
                        OrderID = OrderID,
                        SalesEmployeeCode = SalesEmployeeCode,
                        Status = orderObj.ApprovalStatus,
                        Remarks = Remarks,
                    ).save()
                    return Response({"message":"Success","status":200,"data":[]})
            else:
                return Response({"message":"Invalid SalesEmployeeCode","status":201,"data":[]})
        else:
            return Response({"message":"Invalid Order Id","status":201,"data":[]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})

#Quotation pending for approval
@api_view(["POST"])
def remarksHistory(request):
    try:
        qtid = request.data['id']
        allRemarks = []
        if OrderStatusRemarks.objects.filter(OrderID = qtid).exists():
            remarkObj = OrderStatusRemarks.objects.filter(OrderID = qtid).order_by('-id')
            print(remarkObj)
            for obj in remarkObj:
                SalesEmployeeCode = obj.SalesEmployeeCode
                remarkJson = OrderStatusRemarksSerializer(obj)
                remarkData = json.loads(json.dumps(remarkJson.data))

                if Employee.objects.filter(SalesEmployeeCode = SalesEmployeeCode).exists():
                    empObj = Employee.objects.filter(SalesEmployeeCode = SalesEmployeeCode).values_list('firstName', flat=True)[0]
                    remarkData['EmployeeName'] = str(empObj)
                else:
                    remarkData['EmployeeName'] = ""

                allRemarks.append(remarkData)
        else:
            print('nodata')
        return Response({"message":"Success","status":200,"data":allRemarks}) 
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})


@api_view(['POST'])
def bp_wise_sold_items(request):
    try:
        CardCode = request.data['CardCode']
        contaxt = {}
        if BusinessPartner.objects.filter(CardCode = CardCode).exists():  
            orderIds = Order.objects.filter(CardCode = CardCode).values_list('id', flat=True)
            itemCodes = DocumentLines.objects.filter(OrderID__in = orderIds).values_list('ItemCode', flat=True).distinct()
            itemList = []
            for code in itemCodes:
                itms = DocumentLines.objects.filter(OrderID__in = orderIds, ItemCode = code).order_by('id')
                ItemQuantity = 0
                orderId = 0
                ItemOrderList = []
                LastSoldDate = ""
                for itm in itms:
                    ItemQuantity = ItemQuantity + int(itm.Quantity)
                    orderId = itm.OrderID
                    createDate = Order.objects.filter(pk = orderId).values_list('DocDate', flat=True).first()
                    itemOrder = {
                        "OrderId": orderId,
                        "UnitPirce": itm.UnitPrice,
                        "SoldDate":str(createDate),
                        "TotalQty": ItemQuantity,
                    }
                    ItemOrderList.append(itemOrder)
                    LastSoldDate = createDate
                tempContaxt = {
                    "ItemName": itms[0].ItemDescription,
                    "ItemCode": itms[0].ItemCode,
                    "UnitPirce": itms[0].UnitPrice,
                    "LastSoldDate":LastSoldDate,
                    "TotalQty": ItemQuantity,
                    "ItemOrderList": ItemOrderList
                }
                itemList.append(tempContaxt)

            # for itm in itmObjs:
            #     createDate = Order.objects.filter(pk = itm.OrderID).values_list('DocDate', flat=True).first()
            #     tempContaxt = {
            #         "ItemName": itm.ItemDescription,
            #         "ItemCode": itm.ItemCode,
            #         "UnitPirce": itm.UnitPrice,
            #         "LastSoldDate":str(createDate),
            #         "TotalQty": itm.Quantity
            #     }
            #     itemList.append(tempContaxt)
            return Response({"message":"Success","status":200,"data":itemList}) 
        else:            
            return Response({"message":"Invalid CardCode","status":201,"data":[]}) 
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})