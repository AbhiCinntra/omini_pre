from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from BusinessPartner.models import BPEmployee
from BusinessPartner.serializers import BPEmployeeSerializer

from Employee.serializers import EmployeeSerializer
from Opportunity.models import Opportunity
from Opportunity.serializers import OpportunitySerializer
from PaymentTermsTypes.models import PaymentTermsTypes
from PaymentTermsTypes.serializers import PaymentTermsTypesSerializer
from Item.models import UoMList
from .models import *
from Employee.models import Employee

import requests, json

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import *
from rest_framework.parsers import JSONParser

import os
from django.core.files.storage import FileSystemStorage
from Attachment.models import Attachment
from Attachment.serializers import AttachmentSerializer

# import setting file
from django.conf import settings
from django.db.models import Q

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# custome function import
from global_methods import employeeViewAccess, getAllReportingToIds
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Create your views here.  

#Quotation Create API
@api_view(['POST'])
def create(request):
    fetchid = 0
    try:
        TaxDate = request.data['TaxDate']
        DocDueDate = request.data['DocDueDate']
        DocDate = request.data['DocDate']
        ContactPersonCode = request.data['ContactPersonCode']
        DiscountPercent = request.data['DiscountPercent']
        CardCode = request.data['CardCode']
        CardName = request.data['CardName']
        Comments = request.data['Comments']
        SalesPersonCode = request.data['SalesPersonCode']
        U_OPPID = request.data['U_OPPID']
        U_OPPRNM = request.data['U_OPPRNM']
        U_QUOTNM = request.data['U_QUOTNM']
        
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
        DocTotal=0
        for line in lines:
            DocTotal = float(DocTotal) + float(line['Quantity']) * float(line['UnitPrice'])
        print(DocTotal)

        model=Quotation(TaxDate = TaxDate, DocDueDate = DocDueDate, ContactPersonCode = ContactPersonCode, DiscountPercent = DiscountPercent, DocDate = DocDate, CardCode = CardCode, CardName = CardName, Comments = Comments, SalesPersonCode = SalesPersonCode, DocumentStatus="bost_Open", DocTotal = DocTotal, U_OPPID=U_OPPID, U_OPPRNM=U_OPPRNM, U_QUOTNM=U_QUOTNM, U_FAV='N', CreateDate = CreateDate, CreateTime = CreateTime, UpdateDate = UpdateDate, UpdateTime = UpdateTime,
        PaymentType = PaymentType, DeliveryMode = DeliveryMode, DeliveryTerm = DeliveryTerm, AdditionalCharges = AdditionalCharges, TermCondition = TermCondition, DeliveryCharge = DeliveryCharge, Unit = Unit, U_LAT = U_LAT, U_LONG = U_LONG, Link = Link, PayTermsGrpCode = PayTermsGrpCode, FreeDelivery = FreeDelivery, CreatedBy = CreatedBy)
        
        model.save()
        qt = Quotation.objects.latest('id')
        fetchid = qt.id
        model.save()
        
        addr = request.data['AddressExtension']
        
        model_add = AddressExtension(QuotationID = qt.id, BillToBuilding = addr['BillToBuilding'], ShipToState = addr['ShipToState'], BillToCity = addr['BillToCity'], ShipToCountry = addr['ShipToCountry'], BillToZipCode = addr['BillToZipCode'], ShipToStreet = addr['ShipToStreet'], BillToState = addr['BillToState'], ShipToZipCode = addr['ShipToZipCode'], BillToStreet = addr['BillToStreet'], ShipToBuilding = addr['ShipToBuilding'], ShipToCity = addr['ShipToCity'], BillToCountry = addr['BillToCountry'], U_SCOUNTRY = addr['U_SCOUNTRY'], U_SSTATE = addr['U_SSTATE'], U_SHPTYPB = addr['U_SHPTYPB'], U_BSTATE = addr['U_BSTATE'], U_BCOUNTRY = addr['U_BCOUNTRY'], U_SHPTYPS = addr['U_SHPTYPS'],ShipToDistrict = addr['ShipToDistrict'], BillToDistrict = addr['BillToDistrict'])
        
        model_add.save()
        
        LineNum = 0
        newLines = []
        for line in lines:
            model_lines = DocumentLines(LineNum = LineNum, QuotationID = qt.id, Quantity = line['Quantity'], UnitPrice = line['UnitPrice'], DiscountPercent = line['DiscountPercent'], ItemCode = line['ItemCode'], ItemDescription = line['ItemDescription'], TaxCode = line['TaxCode'], FreeText = line['FreeText'], UomNo = line['UomNo'], UnitWeight = line['UnitWeight'], UnitPriceown = line['UnitPriceown'])
            model_lines.save()
            LineNum=LineNum+1
            # uomObj = UoMList.objects.get(Name = line['UomNo'])
            line['UnitPrice'] = line['UnitPriceown']
            line['UoMCode'] = line['UomNo']
            # line['UoMEntry'] = uomObj.AbsEntry
            line.pop('UnitPriceown', None)
            line.pop('UomNo', None)
            newLines.append(line)
        
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

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
            # "BPL_IDAssignedToInvoice": Unit, #default only one branch exist in SAP
            "BPL_IDAssignedToInvoice": 3, #default only one branch exist in SAP
            "PaymentGroupCode":request.data['PayTermsGrpCode'],
            "U_UTL_FOLD": request.data['DocDate'],
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
            "DocumentLines": newLines
        }
        
        print(">>>>>>>>>>>>>>>>>>>>>>>>")

        res = settings.CALLAPI('post', '/Quotations', 'api', qt_data)
        live = json.loads(res.text)
        if "DocEntry" in live:
            print(live['DocEntry'])
            DocEntry = live['DocEntry']
            
            model = Quotation.objects.get(pk = fetchid)
            model.DocEntry = DocEntry
            model.save()
            
            documentLines = live['DocumentLines']
            # print(documentLines)
            for docline in documentLines:
                LineNum = docline['LineNum']
                TaxCode = docline['TaxCode']
                TaxRate = docline['TaxPercentagePerRow']

                if DocumentLines.objects.filter(QuotationID = fetchid, LineNum = LineNum).exists():
                    DocumentLines.objects.filter(QuotationID = fetchid, LineNum = LineNum).update(TaxCode = TaxCode, TaxRate = TaxRate)

            return Response({"message":"successful","status":200,"data":[{"qt_Id":fetchid, "DocEntry":DocEntry, "qt_data": qt_data}]})
        else:
            SAP_MSG = live['error']['message']['value']
            print(SAP_MSG)
            Quotation.objects.filter(id=fetchid).delete()
            DocumentLines.objects.filter(QuotationID=fetchid).delete()
            AddressExtension.objects.filter(QuotationID=fetchid).delete()
            return Response({"message":SAP_MSG,"SAP_error":SAP_MSG, "status":202,"data":[{"qt_data": qt_data}]})

        if U_OPPID !="":
            oppObj = Opportunity.objects.get(pk=U_OPPID)
            oppObj.QTStatus=1
            oppObj.save()

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        # return Response({"message":"successful","status":200,"data":[{"qt_Id":qt.id, "DocEntry":qt.id}]})        
    except Exception as e:
        Quotation.objects.filter(id=fetchid).delete()
        DocumentLines.objects.filter(QuotationID=fetchid).delete()
        AddressExtension.objects.filter(QuotationID=fetchid).delete()
        return Response({"message":str(e),"status":201,"data":[]})

#Quotation Fav Update API
@api_view(['POST'])
def fav(request):
    fetchid = request.data['id']
    model = Quotation.objects.get(pk = fetchid)
    model.U_FAV  = request.data['U_FAV']
    model.save()
    return Response({"message":"successful","status":200, "data":[]})

#Quotation Update API
@api_view(['POST'])
def approve(request):
    fetchid = request.data['id']
    try:
        model = Quotation.objects.get(pk = fetchid)
        model.U_APPROVEID = request.data['U_APPROVEID']
        model.U_APPROVENM = request.data['U_APPROVENM']
        model.save()
        return Response({"message":"successful","status":200, "data":[]})
    except Exception as e:
        return Response({"message":"Not Update","status":201,"data":[{"Error":str(e)}]})

#Quotation Update API
@api_view(['POST'])
def update(request):
    fetchid = request.data['id']
    try:
    # if True:
        model = Quotation.objects.get(pk = fetchid)
        model.TaxDate = request.data['TaxDate']
        model.DocDate = request.data['DocDate']
        model.DocDueDate = request.data['DocDueDate']
        model.ContactPersonCode = request.data['ContactPersonCode']
        model.DiscountPercent = request.data['DiscountPercent']
        model.Comments = request.data['Comments']
        model.SalesPersonCode = request.data['SalesPersonCode']
        
        model.U_QUOTNM = request.data['U_QUOTNM']
        
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
        quotationUpdatedItemIds = []
        newLines = []
        for line in lines:
            if line["id"] !="":
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
                model_line.UnitPriceown=line['UnitPriceown']
                model_line.save()
                quotationUpdatedItemIds.append(line["id"])
            else:
                lastline = DocumentLines.objects.filter(QuotationID = fetchid).order_by('-LineNum')[:1]
                NewLine = int(lastline[0].LineNum) + 1
                model_lines = DocumentLines(QuotationID = fetchid, LineNum=NewLine, Quantity = line['Quantity'], UnitPrice = line['UnitPrice'], DiscountPercent = line['DiscountPercent'], ItemCode = line['ItemCode'], ItemDescription = line['ItemDescription'], TaxCode = line['TaxCode'], FreeText = line['FreeText'], UomNo = line['UomNo'], UnitWeight = line['UnitWeight'], UnitPriceown = line['UnitPriceown'])
                model_lines.save()
                quotItemObj = DocumentLines.objects.latest('id')
                quotationUpdatedItemIds.append(quotItemObj.id)

            line['UnitPrice'] = line['UnitPriceown']
            line['UoMCode'] = line['UomNo']
            line.pop('UnitPriceown', None)
            line.pop('UomNo', None)
            newLines.append(line)

        print("QuotationUpdatedItemIds", quotationUpdatedItemIds)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # delete extra Quotation item from database
        if len(quotationUpdatedItemIds) != 0:
            if DocumentLines.objects.filter(QuotationID = fetchid).exclude(id__in = quotationUpdatedItemIds).exists():
                DocumentLines.objects.filter(QuotationID = fetchid).exclude(id__in = quotationUpdatedItemIds).delete()
        
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

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
            "BPL_IDAssignedToInvoice": 3, #default only one branch exist in SAP
            "PaymentGroupCode":request.data['PayTermsGrpCode'],
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
                "PlaceOfSupply": request.data['AddressExtension']['ShipToState']
            },
            # "DocumentLines": lines
            "DocumentLines": newLines
        }
        print("qt_data", qt_data)
        print(">>>>>>>>>>>>>>>>>>>>>>>>")

        # res = settings.CALLAPI('post', '/Quotations', 'api', qt_data)
        res = settings.CALLAPI("patch", "/Quotations("+model.DocEntry+")", "api", qt_data)
        # live = json.loads(res.text)
        if int(res.status_code) == 200 or int(res.status_code) == 204:
            return Response({"message":"successful","status":200, "data":[{"qt_data": qt_data}]})
        else:
            res1 = json.loads(res.content)
            SAP_MSG = res1['error']['message']['value']
            return Response({"message":SAP_MSG,"status":202,"SAP_error":SAP_MSG, "data":[{"qt_data": qt_data}]})


        # print(res)
        # if len(res.content) !=0 :
        #     res1 = json.loads(res.content)
        #     SAP_MSG = res1['error']['message']['value']
        #     return Response({"message":SAP_MSG,"status":202,"SAP_error":SAP_MSG, "data":[{"qt_data": qt_data}]})
        # else:
        #     documentLines = live['DocumentLines']
        #     for docline in documentLines:
        #         LineNum = docline['LineNum']
        #         TaxCode = docline['TaxCode']
        #         TaxRate = docline['TaxPercentagePerRow']

        #         if DocumentLines.objects.filter(QuotationID = fetchid, LineNum = LineNum).exists():
        #             DocumentLines.objects.filter(QuotationID = fetchid, LineNum = LineNum).update(TaxCode = TaxCode, TaxRate = TaxRate)

        #     return Response({"message":"successful","status":200, "data":[{"qt_data": qt_data}]})
        
        # return Response({"message":"successful","status":200, "data":[request.data]})
    except Exception as e:
        return Response({"message":"Not Update","status":201,"data":[{"Error":str(e)}]})

#Quotation All API
@api_view(["GET"])
def all(request):
    # allqt = [];
    # quot_obj = Quotation.objects.all().order_by("-id")    
    # allqt = QuotationShow(quot_obj)    
    # return Response({"message": "Success","status": 200,"data":allqt})
    
    quotation_obj = Quotation.objects.all().order_by("-id")
    result = showQuote(quotation_obj)
    return Response({"message": "Success","status": 200,"data":result})


def QuotationShow(quot_obj):
    allqt = []
    for qt in quot_obj:
        qtaddr = AddressExtension.objects.filter(QuotationID=qt.id)
        
        qtaddr_json = AddressExtensionSerializer(qtaddr, many=True)
        
        jss_ = json.loads(json.dumps(qtaddr_json.data))
        jss0 = ''
        for j in jss_:
            jss0=j
        
        lines = DocumentLines.objects.filter(QuotationID=qt.id)
        
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
            'U_QUOTNM':qt.U_QUOTNM,            
            'U_OPPID':qt.U_OPPID,
            'U_OPPRNM':qt.U_OPPRNM,
            'U_FAV':qt.U_FAV,
            'AddressExtension':jss0,
            'DocumentLines':jss1,
            
            "CreateDate":qt.CreateDate,
            "CreateTime":qt.CreateTime,
            "UpdateDate":qt.UpdateDate,
            "UpdateTime":qt.UpdateTime
            }
            
        allqt.append(context)
    return allqt

#Quotation All API
@api_view(["POST"])
def all_filter(request):
    json_data = request.data
    
    if "U_OPPID" in json_data:
        if json_data['U_OPPID'] !='':
            
            quot_obj = Quotation.objects.filter(U_OPPID=json_data['U_OPPID']).order_by("-id")
            if len(quot_obj) ==0:
                return Response({"message": "Success","status": 200,"data":[]})
            else:
                
                #allqt = QuotationShow(quot_obj)
                allqt = showQuote(quot_obj)
                        
            return Response({"message": "Success","status": 200,"data":allqt})
                
    
    if "SalesPersonCode" in json_data:
        print("yes")
        
        if json_data['SalesPersonCode']!="":
            SalesPersonID = json_data['SalesPersonCode']
            empList = employeeViewAccess(SalesPersonID)
            # empList = getAllReportingToIds(SalesPersonID)
            
            print(empList)
            
            for ke in json_data.keys():
                if ke =='U_FAV' :
                    print("yes filter")
                    if json_data['U_FAV'] !='':
                        quot_obj = Quotation.objects.filter(SalesPersonCode__in=empList, U_FAV=json_data['U_FAV']).order_by("-id")
                        if len(quot_obj) ==0:
                            return Response({"message": "Not Available","status": 201,"data":[]})
                        else:
                            #allqt = QuotationShow(quot_obj)
                            allqt = showQuote(quot_obj)
                            return Response({"message": "Success","status": 200,"data":allqt})
                
                else:
                    print("no filter")
                    # qt = Quotation.objects.filter(SalesPersonCode__in=empList).order_by("-id")
                    # quot_json = QuotationSerializer(quot_obj, many=True)
                    # return Response({"message": "Success","status": 200,"data":quot_json.data})
                    quot_obj = Quotation.objects.filter(Q(SalesPersonCode__in=empList) | Q(CreatedBy__in = empList)).order_by("-id")
                    #allqt = QuotationShow(quot_obj)
                    allqt = showQuote(quot_obj)
                        
                    return Response({"message": "Success","status": 200,"data":allqt})
                    
            
        else:
            return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesPersonCode?"}]})
    else:
        print("no")
        return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesPersonCode?"}]})

#Quotation One API
@api_view(["POST"])
def one(request):
    id=request.data['id']
    # quot_obj = Quotation.objects.filter(id=id)
    # allqt = QuotationShow(quot_obj)
    # return Response({"message": "Success","status": 200,"data":allqt})
    
    quot_obj = Quotation.objects.filter(id=id)
    result = showQuote(quot_obj)
    return Response({"message": "Success","status": 200,"data":result})

#Quotation delete
@api_view(['POST'])
def delete(request):
    fetchid=request.data['id']
    try:
        fetchdata=Quotation.objects.filter(pk=fetchid).delete()
        return Response({"message": "Success","status": 200,"data":[]})
    except:
         return Response({"message":"Id wrong","status":"201","data":[]})
     
def showQuote(objs):
    allQuote = [];
    for obj in objs:
        salesType = obj.SalesPersonCode
        createdBy = obj.CreatedBy
        contactType = obj.ContactPersonCode
        quoteId = obj.id
        paymentType = obj.PayTermsGrpCode
        quotjson = QuotationSerializer(obj)
        finalQuotData = json.loads(json.dumps(quotjson.data))

        if salesType != "":
            salesTypeObj = Employee.objects.filter(SalesEmployeeCode = salesType).values("id", "SalesEmployeeCode", "SalesEmployeeName", "Email", "Mobile")
            salesTypejson = EmployeeSerializer(salesTypeObj, many=True)
            finalQuotData['SalesPersonCode'] = json.loads(json.dumps(salesTypejson.data))
        else:
            finalQuotData['SalesPersonCode'] = []
        
        if createdBy != "":
            salesTypeObj = Employee.objects.filter(SalesEmployeeCode = createdBy).values("id", "SalesEmployeeCode", "SalesEmployeeName", "Email", "Mobile")
            salesTypejson = EmployeeSerializer(salesTypeObj, many=True)
            finalQuotData['CreatedBy'] = json.loads(json.dumps(salesTypejson.data))
        else:
            finalQuotData['CreatedBy'] = []
        
        if contactType != "":
            contactTypeObj = BPEmployee.objects.filter(InternalCode = contactType).values("id","FirstName","E_Mail", "InternalCode")
            contactTypejson = BPEmployeeSerializer(contactTypeObj, many = True)
            finalQuotData['ContactPersonCode'] = json.loads(json.dumps(contactTypejson.data))
        else:
            finalQuotData['ContactPersonCode'] = []
 
        if quoteId != "" :
            print('in address')
            # addrObj = AddressExtension.objects.filter(QuotationID = quoteId)
            # addrjson = AddressExtensionSerializer(addrObj, many=True)
            addrObj = AddressExtension.objects.get(QuotationID = quoteId)
            addrjson = AddressExtensionSerializer(addrObj)
            
            linesobj = DocumentLines.objects.filter(QuotationID=quoteId)
            lines_json = DocumentLinesSerializer(linesobj, many=True)
            
            finalQuotData['AddressExtension'] = json.loads(json.dumps(addrjson.data))
            
            finalQuotData['DocumentLines'] = json.loads(json.dumps(lines_json.data))
            
        else:
            finalQuotData['AddressExtension'] = {}
            finalQuotData['DocumentLines'] = []
            
        if Attachment.objects.filter(LinkID = obj.id, LinkType="Quotation").exists():
            Attach_dls = Attachment.objects.filter(LinkID = obj.id, LinkType="Quotation")
            Attach_json = AttachmentSerializer(Attach_dls, many=True)
            finalQuotData['Attach'] = Attach_json.data
        else:
            finalQuotData['Attach'] = []

        if paymentType != "":
            paymentTypeObj = PaymentTermsTypes.objects.filter(GroupNumber = paymentType)
            paymentjson = PaymentTermsTypesSerializer(paymentTypeObj, many = True)
            finalQuotData['PayTermsGrpCode'] = json.loads(json.dumps(paymentjson.data))
        else:
            finalQuotData['PayTermsGrpCode'] = []
            
        allQuote.append(finalQuotData)
    return allQuote

#added by millan on 10-November-2022 for adding attachment
@api_view(["POST"])
def quot_attachment_create(request):
    try:
        quotId = request.data['quotId']
        CreateDate = request.data['CreateDate']
        CreateTime = request.data['CreateTime']

        for File in request.FILES.getlist('Attach'):
            attachmentsImage_url = ""
            target ='./bridge/static/image/QuotAttachment'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+File.name, File)
            file_size = os.stat(file)
            Size = file_size.st_size
            productImage_url = fss.url(file)
            attachmentsImage_url = productImage_url.replace('/bridge', '')

            att=Attachment(File=attachmentsImage_url, LinkID=quotId, CreateDate=CreateDate, CreateTime=CreateTime, Size=Size, LinkType='Quotation')
            
            att.save()  
            
        return Response({"message": "success","status": 200,"data":[]})
    except Exception as e:
        return Response({"message": "Error","status": 201,"data":str(e)})

#added by millan on 10-November-2022 for deleting an attachment
@api_view(['POST'])
def quot_attachment_delete(request):
    try:
        fetchid = request.data['id']
        
        quotId = request.data['quotId']
        
        if Attachment.objects.filter(LinkID=quotId, LinkType='Quotation', pk = fetchid).exists():
            
            Attachment.objects.filter(LinkID=quotId, LinkType='Quotation', pk = fetchid).delete()
            
            return Response({"message":"successful","status":"200","data":[]})
        else:
            return Response({"message":"ID Not Found","status":"201","data":[]})
        
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})

