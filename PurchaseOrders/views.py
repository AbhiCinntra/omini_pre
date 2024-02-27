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

# import setting file
from django.db.models import Q
from django.conf import settings
import mysql.connector

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
            allqt = showPurchaseOrder(quot_obj)
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
            allqt = showPurchaseOrder(quot_obj)
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
        result = showPurchaseOrder(invoice_obj)
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
        result = showPurchaseOrder(invoice_obj)
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
     
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# to get invoice contact person details and salesEmployeeDetails
def showPurchaseOrder(objs):
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
        if BPAddresses.objects.filter(BPCode=bp_code).exists():
            bp_obj = BPAddresses.objects.filter(BPCode=bp_code)
            bpAddrson = BPAddressesSerializer(bp_obj, many=True)
            finalCPCData["BPAddresses"] = bpAddrson.data
        else:
            finalCPCData["BPAddresses"] = []
        ############################added#####################################
        if BPEmployee.objects.filter(InternalCode = cpcType).exists():
            cpcTypeObj = BPEmployee.objects.filter(InternalCode = cpcType).values("id","FirstName","E_Mail", "MobilePhone")  #updated by millan on 15-09-2022
            cpcTypejson = BPEmployeeSerializer(cpcTypeObj, many = True)
            finalCPCData['ContactPersonCode']=json.loads(json.dumps(cpcTypejson.data))
        else:
            finalCPCData['ContactPersonCode'] = []
        ################################addedd################################
        if Employee.objects.filter(SalesEmployeeCode = salesType).exists():
            salesTypeObj = Employee.objects.filter(SalesEmployeeCode = salesType).values("id", "SalesEmployeeCode", "SalesEmployeeName", "Email", "Mobile")
            salesTypejson = EmployeeSerializer(salesTypeObj, many=True)
            finalCPCData['SalesPersonCode'] = json.loads(json.dumps(salesTypejson.data))
        else:
            finalCPCData['SalesPersonCode'] = []
        ################################addedd################################
        if AddressExtension.objects.filter(OrderID = invId).exists():
            addrObj = AddressExtension.objects.filter(OrderID = invId)
            addrjson = AddressExtensionSerializer(addrObj, many=True)
            finalCPCData['AddressExtension'] = json.loads(json.dumps(addrjson.data))
        else:
            finalCPCData['AddressExtension'] = []
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
        if PaymentTermsTypes.objects.filter(GroupNumber = paymentType).exists():
            paymentTypeObj = PaymentTermsTypes.objects.filter(GroupNumber = paymentType)
            paymentjson = PaymentTermsTypesSerializer(paymentTypeObj, many = True)
            finalCPCData['PayTermsGrpCode'] = json.loads(json.dumps(paymentjson.data))
        else:
            finalCPCData['PayTermsGrpCode'] = []
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
        allInvoice.append(finalCPCData)
    return allInvoice
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Pending sales order dashboard
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Pendig Delivery
@api_view(["POST"])
def pending_purchase_order_dashboard(request):
    try:
        print("pending_purchase_order_dashboard", request.data)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SalesPersonCode = request.data['SalesPersonCode']
        # Filter      = request.data['Filter']
        # Code        = request.data['Code']
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
            fromToDate = f"AND ord.DocDate >= '{FromDate}' AND ord.DocDate <= '{ToDate}'"
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

        sqlPendingOrder = f"""
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
                    COALESCE(SUM(
                        CASE
                            WHEN ord.DiscountPercent > 0 THEN (OpenAmount - (OpenAmount * ord.DiscountPercent ) / 100)
                            ELSE (OpenAmount)
                        END
                    ), 0) AS TotalOpenAmount,
                    COALESCE(SUM(ORDLine.RemainingOpenQuantity), 0) AS TotalRemainingOpenQuantity
                FROM PurchaseOrders_purchaseorders ord
                LEFT JOIN PurchaseOrders_documentlines ORDLine ON ORDLine.OrderID = ord.id
                WHERE 
                    ord.CancelStatus = 'csNo'
                    AND ord.DocumentStatus = 'bost_Open'
                    AND RemainingOpenQuantity > 0
                    {fromToDate}
                GROUP BY ord.CardCode, ord.id
                Order By ord.DocDate desc
            ) A ON bp.CardCode = A.CardCode
            WHERE
                bp.U_U_UTL_Zone IN('{zonesStr}')
                {SearchQuery}
            GROUP BY bp.CardCode
            HAVING
                TotalRemainingOpenQuantity > 0
            {orderby} {limitQuery}
        """
        print(sqlPendingOrder)
        mycursor.execute(sqlPendingOrder)
        pendingSalesData = mycursor.fetchall()
        TotalPendingSales = 0
        dataContaxt = []
        if len(pendingSalesData) > 0:
            for data in pendingSalesData:
                CardCode = data['CardCode']
                CardName = data['CardName']
                TotalPendingAmount = data['TotalOpenAmount']
                TotalPendingQuantity = data['TotalRemainingOpenQuantity']
                TotalPendingSales = TotalPendingSales + TotalPendingAmount
                bpData = {
                    "CardCode": CardCode,
                    "CardName": CardName,
                    "PendingAmount": round(float(TotalPendingAmount), 2),
                    "PendingQuantity": round(float(TotalPendingQuantity)),
                    "Orderwise": []
                }
                dataContaxt.append(bpData)

        return Response({"message": "Success","status": 200,"data":[{"Total":round(TotalPendingSales, 2), "Partywise":dataContaxt}]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Pending sales order wise
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Pendig Delivery
@api_view(["POST"])
def bp_pending_purchase_order(request):
    try:
        print('bp_pending_purchase_order', request.data)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        CardCode    = request.data['CardCode']
        FromDate    = request.data['FromDate']
        ToDate      = request.data['ToDate']
        # SearchText  = request.data['SearchText']
        OrderByName = request.data['OrderByName']
        OrderByAmt  = request.data['OrderByAmt']
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
        fromToDate = ""
        if str(FromDate) != "":
            fromToDate = f"AND ord.DocDate >= '{FromDate}' AND ord.DocDate <= '{ToDate}'"
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
        # SearchQuery = ""
        # if str(SearchText) != '':
        #     SearchQuery = f"AND (bp.CardCode like '%%{SearchText}%%' OR bp.CardName like '%%{SearchText}%%')"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        sqlPendingOrder = f"""
            SELECT
                bp.CardCode as CardCode, bp.CardName as CardName, A.id, A.DocEntry, A.DocNum, A.DocDueDate,
                IFNULL((A.DocTotal), 0) AS 'DocTotal',
                IFNULL((A.TotalOpenAmount), 0) AS 'TotalOpenAmount',
                IFNULL((A.TotalRemainingOpenQuantity), 0) AS 'TotalRemainingOpenQuantity'
            FROM BusinessPartner_businesspartner bp
            INNER JOIN (
                SELECT
                    ord.id, ord.CardCode, ord.DocEntry, ord.DocNum, ord.DocTotal, ord.DocDueDate,
                    COALESCE(SUM( CASE WHEN ord.DiscountPercent > 0 THEN (OpenAmount - (OpenAmount * ord.DiscountPercent ) / 100) ELSE (OpenAmount) END ), 0) AS TotalOpenAmount,
                    COALESCE(SUM(ORDLine.RemainingOpenQuantity), 0) AS TotalRemainingOpenQuantity
                FROM PurchaseOrders_purchaseorders ord
                LEFT JOIN PurchaseOrders_documentlines ORDLine ON ORDLine.OrderID = ord.id
                WHERE
                    ord.CancelStatus = 'csNo'
                    AND ord.DocumentStatus = 'bost_Open'
                    AND RemainingOpenQuantity > 0
                    {fromToDate}
                GROUP BY ord.CardCode, ord.id
                Order By ord.DocDate desc
            ) A ON bp.CardCode = A.CardCode
            WHERE bp.CardCode = '{CardCode}'
            HAVING TotalRemainingOpenQuantity > 0
            {orderby} {limitQuery}
        """
        print(sqlPendingOrder)
        mycursor.execute(sqlPendingOrder)
        pendingSalesData = mycursor.fetchall()
        TotalPendingSales = 0
        dataContaxt = []
        if len(pendingSalesData) > 0:
            for data in pendingSalesData:
                OrderID     = data['id']
                CardCode    = data['CardCode']
                CardName    = data['CardName']
                DocNum      = data['DocNum']
                DocDueDate  = data['DocDueDate']
                OrderDocEntry        = data['DocEntry']
                TotalPendingAmount   = data['TotalOpenAmount']
                TotalPendingQuantity = data['TotalRemainingOpenQuantity']
                TotalPendingSales    = TotalPendingSales + TotalPendingAmount
                bpData = {
                    "OrderID": OrderDocEntry,
                    "OrderDocEntry": OrderDocEntry, 
                    "DocNum": DocNum,
                    "CardCode": CardCode,
                    "CardName": CardName,
                    "DocDueDate": DocDueDate,
                    "PendingAmount":round(float(TotalPendingAmount), 2),
                    "PendingQty":round(float(TotalPendingQuantity))
                }
                dataContaxt.append(bpData)

        # return Response({"message": "Success","status": 200,"data":[{"Total":round(TotalPendingSales, 2), "Partywise":dataContaxt}]})
        return Response({"message": "Success","status": 200,"data":{"orderwise":dataContaxt}})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":{"orderwise":[]}})
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Pending sales order wise
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Pendig Delivery
@api_view(["POST"])
def pending_items_by_purchase_order(request):
    try:
        print('pending_items_by_purchase_order', request.data)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        OrderID = request.data['OrderID']
        if PurchaseOrders.objects.filter(DocEntry = OrderID).exists():
            allord = []
            odObj = PurchaseOrders.objects.get(DocEntry = OrderID)
            allitem  = DocumentLines.objects.filter(OrderID = odObj.id, LineStatus = 'bost_Open').exclude(RemainingOpenQuantity = "0.0")
            for item in allitem:
                # PendingAmount = float(item.Price) * float(item.RemainingOpenQuantity)
                # PendingAmount = round(float(item.UnitPrice) * float(item.RemainingOpenQuantity), 2),
                # print("DiscountPercent", DiscountPercent, "item.Price", item.Price, "item.RemainingOpenQuantity", item.RemainingOpenQuantity)
                DiscountPercent = float(odObj.DiscountPercent)
                PendingAmount   = float(item.OpenAmount)
                if DiscountPercent > 0:
                    PendingAmount = PendingAmount - ((PendingAmount * DiscountPercent) / 100)
                # endif
                itemObj = {
                    "OrderID": odObj.DocEntry,
                    "OrderDocEntry": odObj.DocEntry,
                    "ItemCode": item.ItemCode,
                    "ItemDescription": item.ItemDescription,
                    "Quantity": item.Quantity,
                    "PendingQty": item.RemainingOpenQuantity,
                    "UnitPrice": item.UnitPrice,
                    "PendingAmount": round(PendingAmount),
                    "DocDueDate": odObj.DocDueDate
                } 
                allord.append(itemObj)
            return Response({"message": "Success","status": 200,"data":allord})
        else:
            return Response({"message": "Invalid Order ID?","status": 201,"data":[]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})