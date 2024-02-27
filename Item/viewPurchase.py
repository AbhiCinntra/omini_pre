import math
from django.shortcuts import render, redirect  

from PurchaseInvoices.models import VendorPaymentsInvoices, PurchaseInvoices
from BusinessPartner.models import BusinessPartner, BusinessPartnerGroups
from BusinessPartner.models import BPBranch
from PaymentTermsTypes.models import PaymentTermsTypes
from global_methods import *
from .models import *
from Employee.models import Employee
import mysql.connector

# import PurchaseInvoices
from PurchaseInvoices.models import DocumentLines as PurchaseInvoices_documentlines
import requests, json

from rest_framework.decorators import api_view  
from rest_framework.response import Response
from .serializers import *

from pytz import timezone
from datetime import datetime as dt

# import setting file
from django.conf import settings
from django.db.models import Q
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
date = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d')
yearmonth = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m')
time = dt.now(timezone("Asia/Kolkata")).strftime('%H:%M %p')

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
from django.db import connection as db_connection
# >>>>>>>>>>>>>>>>>>>>>>> 
@api_view(['POST'])
def ap_filter_item_dashboard(request):
    try:
        print(request.data)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        Filter = request.data['Filter'] if 'Filter' in request.data else ""
        # SalesType = request.data['Type']
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        SearchText = request.data['SearchText']
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SalesEmployeeCode = request.data['SalesEmployeeCode']
        zone_wise = request.data["Zone"] if "Zone" in request.data else ""

        if zone_wise!="":
            zonesStr = str(zone_wise)
        else:
            zones = getZoneByEmployee(SalesEmployeeCode)
            zonesStr = "','".join(zones)
       

        print("SalesEmployeeCode", SalesEmployeeCode)
        groupBy = "GROUP BY Item_item.U_UTL_ITMCT"
        fieldName = "Item_item.U_UTL_ITMCT AS GroupCode, Item_item.U_UTL_ITMCT AS GroupName,"
        if Filter =="Zone":
            groupBy = "GROUP BY bp.U_U_UTL_Zone"
            fieldName = "bp.U_U_UTL_Zone AS GroupCode, bp.U_U_UTL_Zone AS GroupName,"
        
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        OrderByName = "" #a-z/z-a
        OrderByAmt = "" #desc
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
            orderby = "Order By TotalPrice asc"
        elif str(OrderByAmt).lower() == 'desc':
            orderby = "Order By TotalPrice desc"
        else:
            orderby = "Order By GroupName asc"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        fromToDate = ""
        if str(FromDate) != "":
            fromToDate = f"AND PurchaseInvoices_purchaseinvoices.DocDate >= '{FromDate}' AND PurchaseInvoices_purchaseinvoices.DocDate <= '{ToDate}'"
        
        SearchQuery = ''
        if str(SearchText) != '':
            SearchQuery = f"AND (PurchaseInvoices_documentlines.`ItemCode` like '%%{SearchText}%%' OR PurchaseInvoices_documentlines.`ItemDescription` like '%%{SearchText}%%')"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # mycursor = db_connection.cursor()
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

        TotalSales = 0
        dataContext = []
        sqlQuery = f"""
            SELECT
                PurchaseInvoices_documentlines.`id`,
                {fieldName}                
                SUM(PurchaseInvoices_documentlines.LineTotal) AS NetTotal,
                IFNULL(SUM((PurchaseInvoices_documentlines.LineTotal + (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_documentlines.TaxRate / 100))), 0) AS TotalPriceWithoutHeadDiscount,
                IFNULL(SUM(
                    CASE
                        WHEN PurchaseInvoices_purchaseinvoices.DiscountPercent > 0 THEN
                            (PurchaseInvoices_documentlines.LineTotal - (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_purchaseinvoices.DiscountPercent / 100))
                        ELSE
                            (PurchaseInvoices_documentlines.LineTotal)
                    END
                ), 0) AS TotalPrice,
                SUM(PurchaseInvoices_documentlines.Quantity) AS TotalQty,
                (LineTotal / Quantity) AS UnitPrice,
                COUNT( DISTINCT PurchaseInvoices_documentlines.InvoiceID ) AS NoOfInvoice
            FROM `PurchaseInvoices_documentlines`
            INNER JOIN Item_item ON Item_item.ItemCode = PurchaseInvoices_documentlines.ItemCode
            INNER JOIN PurchaseInvoices_purchaseinvoices ON PurchaseInvoices_purchaseinvoices.id = PurchaseInvoices_documentlines.InvoiceID
            INNER JOIN BusinessPartner_businesspartner bp ON bp.CardCode = PurchaseInvoices_purchaseinvoices.CardCode AND bp.U_U_UTL_Zone IN('{zonesStr}')
            WHERE 
                PurchaseInvoices_purchaseinvoices.CancelStatus = 'csNo' 
                AND (PurchaseInvoices_documentlines.ItemCode != '' AND PurchaseInvoices_documentlines.ItemCode != 'None') 
                AND (Item_item.U_UTL_ITSBG != '' AND Item_item.U_UTL_ITSBG != 'None') 
                AND (Item_item.U_UTL_ITMCT != '' AND Item_item.U_UTL_ITMCT != 'None') 
                { SearchQuery }
                { fromToDate }
            {groupBy}
            { orderby }
            { limitQuery }
        """

        print(sqlQuery)
        mycursor.execute(sqlQuery)
        itemList = mycursor.fetchall()
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        print("NoOfroup", itemList)
        for item in itemList:
            GroupCode   = str(item['GroupCode'])
            GroupName   = str(item['GroupName'])
            TotalPrice  = str(item['TotalPrice'])
            TotalQty    = str(item['TotalQty'])

            bpData = {
                "GroupCode": GroupCode,
                "GroupName": GroupName,
                "TotalPrice": TotalPrice,
                "TotalQty": TotalQty,
                "SubGroup": []
            }
            dataContext.append(bpData)
        # endif

        allCreditNote = 0

        return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": round(TotalSales, 2), "TotalCreditNote":-abs(allCreditNote)})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

# >>>>>>>>>>>>>>>>>>>>>>>   
@api_view(['POST'])
def ap_filter_bpgroup_item(request):
    try:
        print(request.data)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # Filter = request.data['Filter']
        CardCode = request.data['CardCode']
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        SearchText = request.data['SearchText']
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SalesEmployeeCode = request.data['SalesEmployeeCode']
        zones = getZoneByEmployee(SalesEmployeeCode)
        zonesStr = "','".join(zones)
        print("SalesEmployeeCode", SalesEmployeeCode)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        OrderByName = "" #a-z/z-a
        OrderByAmt = "" #desc
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
            orderby = "Order By TotalPrice asc"
        elif str(OrderByAmt).lower() == 'desc':
            orderby = "Order By TotalPrice desc"
        else:
            orderby = "Order By GroupName asc"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        fromToDate = ""
        if str(FromDate) != "":
            fromToDate = f"AND PurchaseInvoices_purchaseinvoices.DocDate >= '{FromDate}' AND PurchaseInvoices_purchaseinvoices.DocDate <= '{ToDate}'"
        
        SearchQuery = ''
        if str(SearchText) != '':
            SearchQuery = f"AND (PurchaseInvoices_documentlines.`ItemCode` like '%%{SearchText}%%' OR PurchaseInvoices_documentlines.`ItemDescription` like '%%{SearchText}%%')"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # mycursor = db_connection.cursor()
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
        TotalSales = 0

        dataContext = []
        sqlQuery = f"""
            SELECT
                PurchaseInvoices_documentlines.`id`,
                Item_item.U_UTL_ITMCT AS GroupCode,
                Item_item.U_UTL_ITMCT AS GroupName,
                SUM(PurchaseInvoices_documentlines.LineTotal) AS NetTotal,
                IFNULL(SUM((PurchaseInvoices_documentlines.LineTotal + (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_documentlines.TaxRate / 100))), 0) AS TotalPriceWithoutHeadDiscount,
                IFNULL(SUM(
                    CASE
                        WHEN PurchaseInvoices_purchaseinvoices.DiscountPercent > 0 THEN
                            (PurchaseInvoices_documentlines.LineTotal - (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_purchaseinvoices.DiscountPercent / 100))
                        ELSE
                            (PurchaseInvoices_documentlines.LineTotal)
                    END
                ), 0) AS TotalPrice,
                SUM(PurchaseInvoices_documentlines.Quantity) AS TotalQty,
                (LineTotal / Quantity) AS UnitPrice,
                COUNT( DISTINCT PurchaseInvoices_documentlines.InvoiceID ) AS NoOfInvoice
            FROM `PurchaseInvoices_documentlines`
            INNER JOIN Item_item ON Item_item.ItemCode = PurchaseInvoices_documentlines.ItemCode
            INNER JOIN PurchaseInvoices_purchaseinvoices ON PurchaseInvoices_purchaseinvoices.id = PurchaseInvoices_documentlines.InvoiceID
            INNER JOIN BusinessPartner_businesspartner bp ON bp.CardCode = PurchaseInvoices_purchaseinvoices.CardCode AND bp.U_U_UTL_Zone IN('{zonesStr}')
            WHERE 
                PurchaseInvoices_purchaseinvoices.CancelStatus = 'csNo' and PurchaseInvoices_purchaseinvoices.CardCode='{CardCode}'
                AND (PurchaseInvoices_documentlines.ItemCode != '' AND PurchaseInvoices_documentlines.ItemCode != 'None')
                AND (Item_item.U_UTL_ITSBG != '' AND Item_item.U_UTL_ITSBG != 'None') 
                AND (Item_item.U_UTL_ITMCT != '' AND Item_item.U_UTL_ITMCT != 'None') 
                { SearchQuery } 
                { fromToDate }
            GROUP BY Item_item.U_UTL_ITMCT
            { orderby }
            { limitQuery }
        """

        print(sqlQuery)
        mycursor.execute(sqlQuery)
        itemList = mycursor.fetchall()
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        print("NoOfroup", itemList)
        for item in itemList:
            GroupCode   = str(item['GroupCode'])
            GroupName   = str(item['GroupName'])
            TotalPrice  = str(item['TotalPrice'])
            TotalQty    = str(item['TotalQty'])
            bpData = {
                "GroupCode": GroupCode,
                "GroupName": GroupName,
                "TotalPrice": TotalPrice,
                "TotalQty": TotalQty,
                "SubGroup": []
            }
            dataContext.append(bpData)
        # endif

        allCreditNote = 0

        return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": round(TotalSales, 2), "TotalCreditNote":-abs(allCreditNote)})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
    
# >>>>>>>>>>>>>>>>>>>>>>> 
@api_view(['POST'])
def ap_filter_bpsubgroup_item(request):
    try:
        print(request.data)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        SearchText = request.data['SearchText']
        CategoryCode = request.data['CategoryCode']
        CardCode = request.data['CardCode']
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SalesEmployeeCode = request.data['SalesEmployeeCode']

        zone_wise = request.data["Zone"] if "Zone" in request.data else ""

        if zone_wise!="":
            zonesStr = str(zone_wise)
        else:
            zones = getZoneByEmployee(SalesEmployeeCode)
            zonesStr = "','".join(zones)

        # zones = getZoneByEmployee(SalesEmployeeCode)
        # zonesStr = "','".join(zones)
        print("SalesEmployeeCode", SalesEmployeeCode)       
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
            orderby = "Order By Item_item.U_UTL_ITSBG asc"
        elif str(OrderByName).lower() == 'z-a':
            orderby = "Order By Item_item.U_UTL_ITSBG desc"
        elif str(OrderByAmt).lower() == 'asc':
            orderby = "Order By LineTotal asc"
        elif str(OrderByAmt).lower() == 'desc':
            orderby = "Order By LineTotal desc"
        else:
            orderby = "Order By Item_item.U_UTL_ITSBG asc"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        fromToDate = ""
        if str(FromDate) != "":
            fromToDate = f"AND PurchaseInvoices_purchaseinvoices.DocDate >= '{FromDate}' AND PurchaseInvoices_purchaseinvoices.DocDate <= '{ToDate}'"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SearchQuery = ''
        if str(SearchText).strip() != '':
            SearchQuery = f"AND (Item_item.`U_UTL_ITSBG` like '%%{SearchText}%%')"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # mycursor = db_connection.cursor()
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
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

        TotalSales = 0
        dataContext = []
        sqlQuery = f"""
            SELECT PurchaseInvoices_documentlines.`id`, Item_item.U_UTL_ITSBG, 
                sum(PurchaseInvoices_documentlines.LineTotal) as LineTotal, 
                sum(PurchaseInvoices_documentlines.Quantity) as Quantity 
            FROM `PurchaseInvoices_documentlines` 
            INNER Join Item_item ON Item_item.ItemCode = PurchaseInvoices_documentlines.ItemCode 
            INNER Join PurchaseInvoices_purchaseinvoices ON PurchaseInvoices_purchaseinvoices.id = PurchaseInvoices_documentlines.InvoiceID  
            INNER Join BusinessPartner_businesspartner bp ON bp.CardCode = PurchaseInvoices_purchaseinvoices.CardCode
            WHERE 
                PurchaseInvoices_purchaseinvoices.CancelStatus='csNo' AND bp.CardCode = '{CardCode}'
                AND (PurchaseInvoices_documentlines.ItemCode != '' AND PurchaseInvoices_documentlines.ItemCode != 'None')
                AND Item_item.U_UTL_ITMCT = '{CategoryCode}'
                AND bp.U_U_UTL_Zone IN('{zonesStr}')
                {SearchQuery}
                {fromToDate}
            GROUP BY Item_item.`U_UTL_ITSBG` {orderby} {limitQuery}
        """
        #GROUP BY PurchaseInvoices_documentlines.`U_UTL_ITSBG` {orderby} {limitQuery}

        print(sqlQuery)
        mycursor.execute(sqlQuery)
        itemList = mycursor.fetchall()
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        UnitPrice = 0
        totalPrice = 0
        totalQty = 0
        NoOfInvoice = len(itemList)
        print("NoOfInvoice", NoOfInvoice)
        if len(itemList) != 0:
            subGroupData = []
            for item in itemList:
                U_UTL_ITSBG = str(item['U_UTL_ITSBG'])
                UnitPrice   = float(item['LineTotal'])
                Quantity    = int(item['Quantity'])
                totalPrice  = totalPrice + UnitPrice
                totalQty    = totalQty + Quantity
                print("U_UTL_ITSBG", U_UTL_ITSBG)
                
                subGroup = {
                    "GroupName": U_UTL_ITSBG,
                    "GroupCode": U_UTL_ITSBG,
                    "TotalPrice": round(UnitPrice, 2),
                    "TotalQty": Quantity
                }
                dataContext.append(subGroup)
        # endif
        TotalSales = totalPrice
        allCreditNote = 0
        # endfor
        
        return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": round(TotalSales, 2), "TotalCreditNote":-abs(allCreditNote)})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

# >>>>>>>>>>>>>>>>>>>>>>> 
@api_view(['POST'])
def ap_filter_bpitem(request):
    try:
        print("sold_items_dashboard", json.loads(json.dumps(request.data)))
        print(request.data)
        SearchText = request.data['SearchText']
        FromDate   = request.data['FromDate']
        ToDate     = request.data['ToDate']
        GroupCode  = request.data['GroupCode']
        CardCode  = request.data['CardCode']
    
        SubGroupCode = request.data["SubGroupCode"] if "SubGroupCode" in request.data else ""
        if SubGroupCode!="":
            item_sub_category_query = f"AND Item_item.U_UTL_ITSBG = '{SubGroupCode}'"
        else:
            item_sub_category_query = f"AND Item_item.U_UTL_ITMCT = '{GroupCode}'"

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SalesEmployeeCode = -1
        if 'SalesEmployeeCode' in request.data:
            SalesEmployeeCode = request.data['SalesEmployeeCode']
        zones = getZoneByEmployee(SalesEmployeeCode)
        zonesStr = "','".join(zones)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        OrderByName = "" #a-z/z-a
        OrderByAmt = "" #desc
        if 'OrderByName' in request.data:
            OrderByName = str(request.data['OrderByName']).strip()
        if 'OrderByAmt' in request.data:
            OrderByAmt = str(request.data['OrderByAmt']).strip()
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        orderby = ""
        if str(OrderByName).lower() == 'a-z':
            orderby = "Order By Item_item.ItemName asc"
        elif str(OrderByName).lower() == 'z-a':
            orderby = "Order By Item_item.ItemName desc"
        elif str(OrderByAmt).lower() == 'asc':
            orderby = "Order By TotalPrice asc"
        elif str(OrderByAmt).lower() == 'desc':
            orderby = "Order By TotalPrice desc"
        else:
            orderby = "Order By Item_item.ItemName asc"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        fromToDate = ""
        if str(FromDate) != "":
            fromToDate = f"AND PurchaseInvoices_purchaseinvoices.DocDate >= '{FromDate}' AND PurchaseInvoices_purchaseinvoices.DocDate <= '{ToDate}'"
        
        SearchQuery = ''
        if str(SearchText) != '':
            SearchQuery = f"AND (PurchaseInvoices_documentlines.`ItemCode` like '%%{SearchText}%%' OR PurchaseInvoices_documentlines.`ItemDescription` like '%%{SearchText}%%')"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # mycursor = db_connection.cursor()
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

        allItems   = []
        TotalSales = 0
        sqlQuery = ""
        sqlQuery2 = ""
        sqlQuery = f"""
            SELECT
                PurchaseInvoices_documentlines.`id`,
                PurchaseInvoices_documentlines.`ItemDescription` AS ItemName,
                PurchaseInvoices_documentlines.ItemCode AS ItemCode,
                SUM(PurchaseInvoices_documentlines.LineTotal) AS NetTotal,
                IFNULL(SUM((PurchaseInvoices_documentlines.LineTotal + (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_documentlines.TaxRate / 100))), 0) AS TotalPriceWithoutHeadDiscount,
                IFNULL(SUM(
                    CASE
                        WHEN PurchaseInvoices_purchaseinvoices.DiscountPercent > 0 THEN
                            (PurchaseInvoices_documentlines.LineTotal - (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_purchaseinvoices.DiscountPercent / 100))
                        ELSE
                            (PurchaseInvoices_documentlines.LineTotal)
                    END
                ), 0) AS TotalPrice,
                SUM(PurchaseInvoices_documentlines.Quantity) AS TotalQty,
                (LineTotal / Quantity) AS UnitPrice,
                COUNT( DISTINCT PurchaseInvoices_documentlines.InvoiceID ) AS NoOfInvoice
            FROM `PurchaseInvoices_documentlines`
            INNER JOIN Item_item ON Item_item.ItemCode = PurchaseInvoices_documentlines.ItemCode
            INNER JOIN PurchaseInvoices_purchaseinvoices ON PurchaseInvoices_purchaseinvoices.id = PurchaseInvoices_documentlines.InvoiceID
            INNER JOIN BusinessPartner_businesspartner bp ON bp.CardCode = PurchaseInvoices_purchaseinvoices.CardCode AND bp.U_U_UTL_Zone IN('{zonesStr}')
            WHERE 
                PurchaseInvoices_purchaseinvoices.CancelStatus = 'csNo' AND PurchaseInvoices_purchaseinvoices.CardCode='{CardCode}' 
                AND (PurchaseInvoices_documentlines.ItemCode != '' AND PurchaseInvoices_documentlines.ItemCode != 'None')
                { item_sub_category_query }
                { SearchQuery } 
                { fromToDate }
            GROUP BY PurchaseInvoices_documentlines.`ItemCode` 
            { orderby }
            { limitQuery }
        """            
        # sqlQuery2 = f"""SELECT PurchaseInvoices_documentlines.`id`, PurchaseInvoices_documentlines.`ItemDescription` AS ItemName, PurchaseInvoices_documentlines.ItemCode AS ItemCode, SUM(PurchaseInvoices_documentlines.LineTotal) AS NetTotal, IFNULL(SUM((PurchaseInvoices_documentlines.LineTotal + (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_documentlines.TaxRate / 100))), 0) AS TotalPriceWithoutHeadDiscount, IFNULL(SUM( CASE WHEN PurchaseInvoices_purchaseinvoices.DiscountPercent > 0 THEN (PurchaseInvoices_documentlines.LineTotal - (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_purchaseinvoices.DiscountPercent / 100)) ELSE (PurchaseInvoices_documentlines.LineTotal) END ), 0) AS TotalPrice, SUM(PurchaseInvoices_documentlines.Quantity) AS TotalQty, (LineTotal / Quantity) AS UnitPrice, COUNT( DISTINCT PurchaseInvoices_documentlines.InvoiceID ) AS NoOfInvoice FROM `PurchaseInvoices_documentlines` INNER JOIN Item_item ON Item_item.ItemCode = PurchaseInvoices_documentlines.ItemCode INNER JOIN PurchaseInvoices_purchaseinvoices ON PurchaseInvoices_purchaseinvoices.id = PurchaseInvoices_documentlines.InvoiceID INNER JOIN BusinessPartner_businesspartner bp ON bp.CardCode = PurchaseInvoices_purchaseinvoices.CardCode AND bp.U_U_UTL_Zone IN('{zonesStr}') WHERE PurchaseInvoices_purchaseinvoices.CancelStatus = 'csNo' AND (PurchaseInvoices_documentlines.ItemCode != '' AND PurchaseInvoices_documentlines.ItemCode != 'None') { item_sub_category_query } { SearchQuery } { fromToDate }"""

        sqlQuery2 = f"""
            SELECT
                PurchaseInvoices_documentlines.`id`,
                PurchaseInvoices_documentlines.`ItemDescription` AS ItemName,
                PurchaseInvoices_documentlines.ItemCode AS ItemCode,
                SUM(PurchaseInvoices_documentlines.LineTotal) AS NetTotal,
                IFNULL(SUM((PurchaseInvoices_documentlines.LineTotal + (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_documentlines.TaxRate / 100))), 0) AS TotalPriceWithoutHeadDiscount,
                IFNULL(SUM(
                    CASE
                        WHEN PurchaseInvoices_purchaseinvoices.DiscountPercent > 0 THEN
                            (PurchaseInvoices_documentlines.LineTotal - (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_purchaseinvoices.DiscountPercent / 100))
                        ELSE
                            (PurchaseInvoices_documentlines.LineTotal)
                    END
                ), 0) AS TotalPrice,
                SUM(PurchaseInvoices_documentlines.Quantity) AS TotalQty,
                (LineTotal / Quantity) AS UnitPrice,
                COUNT( DISTINCT PurchaseInvoices_documentlines.InvoiceID ) AS NoOfInvoice
            FROM `PurchaseInvoices_documentlines`
            INNER JOIN Item_item ON Item_item.ItemCode = PurchaseInvoices_documentlines.ItemCode
            INNER JOIN PurchaseInvoices_purchaseinvoices ON PurchaseInvoices_purchaseinvoices.id = PurchaseInvoices_documentlines.InvoiceID
            INNER JOIN BusinessPartner_businesspartner bp ON bp.CardCode = PurchaseInvoices_purchaseinvoices.CardCode AND bp.U_U_UTL_Zone IN('{zonesStr}')
            WHERE 
                PurchaseInvoices_purchaseinvoices.CancelStatus = 'csNo' AND PurchaseInvoices_purchaseinvoices.CardCode='{CardCode}' 
                AND (PurchaseInvoices_documentlines.ItemCode != '' AND PurchaseInvoices_documentlines.ItemCode != 'None')
                { item_sub_category_query }
                { SearchQuery } 
                { fromToDate }
        """

        print(sqlQuery)
        # itemList = PurchaseInvoices_documentlines.objects.raw(sqlQuery)
        mycursor.execute(sqlQuery)
        itemList = mycursor.fetchall()
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        print('^^^^^^^^^^^^^^^^^')

        # sqlQuery2 = f"""SELECT PurchaseInvoices_documentlines.`id`, PurchaseInvoices_documentlines.`ItemDescription` AS ItemName, PurchaseInvoices_documentlines.ItemCode AS ItemCode, SUM(PurchaseInvoices_documentlines.LineTotal) AS NetTotal, IFNULL(SUM((PurchaseInvoices_documentlines.LineTotal + (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_documentlines.TaxRate / 100))), 0) AS TotalPriceWithoutHeadDiscount, IFNULL(SUM( CASE WHEN PurchaseInvoices_purchaseinvoices.DiscountPercent > 0 THEN (PurchaseInvoices_documentlines.LineTotal - (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_purchaseinvoices.DiscountPercent / 100)) ELSE (PurchaseInvoices_documentlines.LineTotal) END ), 0) AS TotalPrice, SUM(PurchaseInvoices_documentlines.Quantity) AS TotalQty, (LineTotal / Quantity) AS UnitPrice, COUNT( DISTINCT PurchaseInvoices_documentlines.InvoiceID ) AS NoOfInvoice FROM `PurchaseInvoices_documentlines` INNER JOIN Item_item ON Item_item.ItemCode = PurchaseInvoices_documentlines.ItemCode INNER JOIN PurchaseInvoices_purchaseinvoices ON PurchaseInvoices_purchaseinvoices.id = PurchaseInvoices_documentlines.InvoiceID INNER JOIN BusinessPartner_businesspartner bp ON bp.CardCode = PurchaseInvoices_purchaseinvoices.CardCode AND (PurchaseInvoices_documentlines.ItemCode != '' AND PurchaseInvoices_documentlines.ItemCode != 'None') AND bp.U_U_UTL_Zone IN('{zonesStr}') WHERE PurchaseInvoices_purchaseinvoices.CancelStatus = 'csNo'"""
        print(sqlQuery2)
        mycursor.execute(sqlQuery2)
        totalSalesData = mycursor.fetchall()
        if len(totalSalesData) != 0:
            TotalSales   = float(totalSalesData[0]['TotalPrice'])
            
        # TotalSales = totalPrice
        allCreditNote = 0
            
        return Response({"message": "Success","status": 200, "data":itemList, "TotalSales": round(TotalSales, 2), "TotalCreditNote":-abs(allCreditNote)})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

# >>>>>>>>>>>>>>>>>>>>>>> 
@api_view(['POST'])
def ap_sub_category_items_dashboard(request):
    try:
        print(request.data)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        SearchText = request.data['SearchText']
        CategoryCode = request.data['CategoryCode']
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SalesEmployeeCode = request.data['SalesEmployeeCode']

        zone_wise = request.data["Zone"] if "Zone" in request.data else ""

        if zone_wise!="":
            zonesStr = str(zone_wise)
        else:
            zones = getZoneByEmployee(SalesEmployeeCode)
            zonesStr = "','".join(zones)

        # zones = getZoneByEmployee(SalesEmployeeCode)
        # zonesStr = "','".join(zones)
        print("SalesEmployeeCode", SalesEmployeeCode)       
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
            orderby = "Order By Item_item.U_UTL_ITSBG asc"
        elif str(OrderByName).lower() == 'z-a':
            orderby = "Order By Item_item.U_UTL_ITSBG desc"
        elif str(OrderByAmt).lower() == 'asc':
            orderby = "Order By LineTotal asc"
        elif str(OrderByAmt).lower() == 'desc':
            orderby = "Order By LineTotal desc"
        else:
            orderby = "Order By Item_item.U_UTL_ITSBG asc"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        fromToDate = ""
        if str(FromDate) != "":
            fromToDate = f"AND PurchaseInvoices_purchaseinvoices.DocDate >= '{FromDate}' AND PurchaseInvoices_purchaseinvoices.DocDate <= '{ToDate}'"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SearchQuery = ''
        if str(SearchText).strip() != '':
            SearchQuery = f"AND (PurchaseInvoices_documentlines.`U_UTL_ITSBG` like '%%{SearchText}%%')"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # mycursor = db_connection.cursor()
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
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

        TotalSales = 0
        dataContext = []
        sqlQuery = f"""
            SELECT PurchaseInvoices_documentlines.`id`, Item_item.U_UTL_ITSBG, 
                sum(PurchaseInvoices_documentlines.LineTotal) as LineTotal, 
                sum(PurchaseInvoices_documentlines.Quantity) as Quantity 
            FROM `PurchaseInvoices_documentlines` 
            INNER Join Item_item ON Item_item.ItemCode = PurchaseInvoices_documentlines.ItemCode 
            INNER Join PurchaseInvoices_purchaseinvoices ON PurchaseInvoices_purchaseinvoices.id = PurchaseInvoices_documentlines.InvoiceID  
            INNER Join BusinessPartner_businesspartner bp ON bp.CardCode = PurchaseInvoices_purchaseinvoices.CardCode
            WHERE 
                PurchaseInvoices_purchaseinvoices.CancelStatus='csNo'
                AND (PurchaseInvoices_documentlines.ItemCode != '' AND PurchaseInvoices_documentlines.ItemCode != 'None')
                AND Item_item.U_UTL_ITMCT = '{CategoryCode}'
                AND bp.U_U_UTL_Zone IN('{zonesStr}')
                {SearchQuery}
                {fromToDate}
            GROUP BY Item_item.`U_UTL_ITSBG` {orderby} {limitQuery}
        """
        #GROUP BY PurchaseInvoices_documentlines.`U_UTL_ITSBG` {orderby} {limitQuery}

        print(sqlQuery)
        mycursor.execute(sqlQuery)
        itemList = mycursor.fetchall()
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        UnitPrice = 0
        totalPrice = 0
        totalQty = 0
        NoOfInvoice = len(itemList)
        print("NoOfInvoice", NoOfInvoice)
        if len(itemList) != 0:
            subGroupData = []
            for item in itemList:
                U_UTL_ITSBG = str(item['U_UTL_ITSBG'])
                UnitPrice   = float(item['LineTotal'])
                Quantity    = int(item['Quantity'])
                totalPrice  = totalPrice + UnitPrice
                totalQty    = totalQty + Quantity
                print("U_UTL_ITSBG", U_UTL_ITSBG)
                
                subGroup = {
                    "GroupName": U_UTL_ITSBG,
                    "GroupCode": U_UTL_ITSBG,
                    "TotalPrice": round(UnitPrice, 2),
                    "TotalQty": Quantity
                }
                dataContext.append(subGroup)
        # endif
        TotalSales = totalPrice
        allCreditNote = 0
        # endfor
        
        return Response({"message": "Success","status": 200, "data":dataContext, "TotalSales": round(TotalSales, 2), "TotalCreditNote":-abs(allCreditNote)})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

# >>>>>>>>>>>>>>>>>>>>>>> 
@api_view(['POST'])
def ap_sold_items_dashboard(request):
    try:
        print("sold_items_dashboard", json.loads(json.dumps(request.data)))
        print(request.data)
        SearchText = request.data['SearchText']
        FromDate   = request.data['FromDate']
        ToDate     = request.data['ToDate']
        
        GroupCode = ""
        if 'GroupCode' in request.data:
            GroupCode  = request.data['GroupCode']
        
        SubGroupCode = ""
        if 'SubGroupCode' in request.data:
            SubGroupCode  = request.data['SubGroupCode']

        Zone = ""
        if 'Zone' in request.data:
            Zone  = request.data['Zone']

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SalesEmployeeCode = -1
        if 'SalesEmployeeCode' in request.data:
            SalesEmployeeCode = request.data['SalesEmployeeCode']
        
        zone_wise = request.data["Zone"] if "Zone" in request.data else ""

        if zone_wise!="":
            zonesStr = str(zone_wise)
        else:
            zones = getZoneByEmployee(SalesEmployeeCode)
            zonesStr = "','".join(zones)


        # zones = getZoneByEmployee(SalesEmployeeCode)
        # zonesStr = "','".join(zones)


        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        OrderByName = "" #a-z/z-a
        OrderByAmt = "" #desc
        if 'OrderByName' in request.data:
            OrderByName = str(request.data['OrderByName']).strip()
        if 'OrderByAmt' in request.data:
            OrderByAmt = str(request.data['OrderByAmt']).strip()
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        orderby = ""
        if str(OrderByName).lower() == 'a-z':
            orderby = "Order By Item_item.ItemName asc"
        elif str(OrderByName).lower() == 'z-a':
            orderby = "Order By Item_item.ItemName desc"
        elif str(OrderByAmt).lower() == 'asc':
            orderby = "Order By TotalPrice asc"
        elif str(OrderByAmt).lower() == 'desc':
            orderby = "Order By TotalPrice desc"
        else:
            orderby = "Order By Item_item.ItemName asc"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        fromToDate = ""
        if str(FromDate) != "":
            fromToDate = f"AND PurchaseInvoices_purchaseinvoices.DocDate >= '{FromDate}' AND PurchaseInvoices_purchaseinvoices.DocDate <= '{ToDate}'"
        
        SearchQuery = ''
        if str(SearchText) != '':
            SearchQuery = f"AND ( PurchaseInvoices_documentlines.`ItemCode` like '%%{SearchText}%%' OR PurchaseInvoices_documentlines.`ItemDescription` like '%%{SearchText}%%')"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        # mycursor = db_connection.cursor()
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
        
        allItems   = []
        TotalSales = 0
        sqlQuery = ""
        sqlQuery2 = ""
        if str(GroupCode) != "":
            sqlQuery = f"""
                SELECT
                    PurchaseInvoices_documentlines.`id`,
                    PurchaseInvoices_documentlines.`ItemDescription` AS ItemName,
                    PurchaseInvoices_documentlines.ItemCode AS ItemCode,
                    SUM(PurchaseInvoices_documentlines.LineTotal) AS NetTotal,
                    IFNULL(SUM((PurchaseInvoices_documentlines.LineTotal + (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_documentlines.TaxRate / 100))), 0) AS TotalPriceWithoutHeadDiscount,
                    IFNULL(SUM(
                        CASE
                            WHEN PurchaseInvoices_purchaseinvoices.DiscountPercent > 0 THEN
                                (PurchaseInvoices_documentlines.LineTotal - (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_purchaseinvoices.DiscountPercent / 100))
                            ELSE
                                (PurchaseInvoices_documentlines.LineTotal)
                        END
                    ), 0) AS TotalPrice,
                    SUM(PurchaseInvoices_documentlines.Quantity) AS TotalQty,
                    (LineTotal / Quantity) AS UnitPrice,
                    COUNT( DISTINCT PurchaseInvoices_documentlines.InvoiceID ) AS NoOfInvoice
                FROM `PurchaseInvoices_documentlines`
                INNER JOIN Item_item ON Item_item.ItemCode = PurchaseInvoices_documentlines.ItemCode
                INNER JOIN PurchaseInvoices_purchaseinvoices ON PurchaseInvoices_purchaseinvoices.id = PurchaseInvoices_documentlines.InvoiceID
                INNER JOIN BusinessPartner_businesspartner bp ON bp.CardCode = PurchaseInvoices_purchaseinvoices.CardCode AND bp.U_U_UTL_Zone IN('{zonesStr}')
                WHERE 
                    PurchaseInvoices_purchaseinvoices.CancelStatus = 'csNo' 
                    AND (PurchaseInvoices_documentlines.ItemCode != '' AND PurchaseInvoices_documentlines.ItemCode != 'None')
                    AND Item_item.U_UTL_ITMCT = '{GroupCode}' 
                    { SearchQuery } 
                    { fromToDate }
                GROUP BY PurchaseInvoices_documentlines.`ItemCode` 
                { orderby }
                { limitQuery }
            """            
            sqlQuery2 = f"""SELECT PurchaseInvoices_documentlines.`id`, PurchaseInvoices_documentlines.`ItemDescription` AS ItemName, PurchaseInvoices_documentlines.ItemCode AS ItemCode, SUM(PurchaseInvoices_documentlines.LineTotal) AS NetTotal, IFNULL(SUM((PurchaseInvoices_documentlines.LineTotal + (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_documentlines.TaxRate / 100))), 0) AS TotalPriceWithoutHeadDiscount, IFNULL(SUM( CASE WHEN PurchaseInvoices_purchaseinvoices.DiscountPercent > 0 THEN (PurchaseInvoices_documentlines.LineTotal - (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_purchaseinvoices.DiscountPercent / 100)) ELSE (PurchaseInvoices_documentlines.LineTotal) END ), 0) AS TotalPrice, SUM(PurchaseInvoices_documentlines.Quantity) AS TotalQty, (LineTotal / Quantity) AS UnitPrice, COUNT( DISTINCT PurchaseInvoices_documentlines.InvoiceID ) AS NoOfInvoice FROM `PurchaseInvoices_documentlines` INNER JOIN Item_item ON Item_item.ItemCode = PurchaseInvoices_documentlines.ItemCode INNER JOIN PurchaseInvoices_purchaseinvoices ON PurchaseInvoices_purchaseinvoices.id = PurchaseInvoices_documentlines.InvoiceID INNER JOIN BusinessPartner_businesspartner bp ON bp.CardCode = PurchaseInvoices_purchaseinvoices.CardCode AND bp.U_U_UTL_Zone IN('{zonesStr}') WHERE PurchaseInvoices_purchaseinvoices.CancelStatus = 'csNo' AND (PurchaseInvoices_documentlines.ItemCode != '' AND PurchaseInvoices_documentlines.ItemCode != 'None') AND Item_item.U_UTL_ITMCT = '{GroupCode}' { SearchQuery } { fromToDate }"""

        elif str(SubGroupCode) != "":
            sqlQuery = f"""
                SELECT
                    PurchaseInvoices_documentlines.`id`,
                    PurchaseInvoices_documentlines.`ItemDescription` AS ItemName,
                    PurchaseInvoices_documentlines.ItemCode AS ItemCode,
                    SUM(PurchaseInvoices_documentlines.LineTotal) AS NetTotal,
                    IFNULL(SUM((PurchaseInvoices_documentlines.LineTotal + (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_documentlines.TaxRate / 100))), 0) AS TotalPriceWithoutHeadDiscount,
                    IFNULL(SUM(
                        CASE
                            WHEN PurchaseInvoices_purchaseinvoices.DiscountPercent > 0 THEN
                                (PurchaseInvoices_documentlines.LineTotal - (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_purchaseinvoices.DiscountPercent / 100))
                            ELSE
                                (PurchaseInvoices_documentlines.LineTotal)
                        END
                    ), 0) AS TotalPrice,
                    SUM(PurchaseInvoices_documentlines.Quantity) AS TotalQty,
                    (LineTotal / Quantity) AS UnitPrice,
                    COUNT( DISTINCT PurchaseInvoices_documentlines.InvoiceID ) AS NoOfInvoice
                FROM `PurchaseInvoices_documentlines`
                INNER JOIN Item_item ON Item_item.ItemCode = PurchaseInvoices_documentlines.ItemCode
                INNER JOIN PurchaseInvoices_purchaseinvoices ON PurchaseInvoices_purchaseinvoices.id = PurchaseInvoices_documentlines.InvoiceID
                INNER JOIN BusinessPartner_businesspartner bp ON bp.CardCode = PurchaseInvoices_purchaseinvoices.CardCode AND bp.U_U_UTL_Zone IN('{zonesStr}')
                WHERE
                    PurchaseInvoices_purchaseinvoices.CancelStatus = 'csNo' 
                    AND (PurchaseInvoices_documentlines.ItemCode != '' AND PurchaseInvoices_documentlines.ItemCode != 'None')
                    AND Item_item.U_UTL_ITSBG = '{SubGroupCode}' 
                    { SearchQuery } 
                    { fromToDate }
                GROUP BY
                    PurchaseInvoices_documentlines.`ItemCode` 
                { orderby } 
                { limitQuery }
            """
            sqlQuery2 = f"""SELECT PurchaseInvoices_documentlines.`id`, PurchaseInvoices_documentlines.`ItemDescription` AS ItemName, PurchaseInvoices_documentlines.ItemCode AS ItemCode, SUM(PurchaseInvoices_documentlines.LineTotal) AS NetTotal, IFNULL(SUM((PurchaseInvoices_documentlines.LineTotal + (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_documentlines.TaxRate / 100))), 0) AS TotalPriceWithoutHeadDiscount, IFNULL(SUM( CASE WHEN PurchaseInvoices_purchaseinvoices.DiscountPercent > 0 THEN (PurchaseInvoices_documentlines.LineTotal - (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_purchaseinvoices.DiscountPercent / 100)) ELSE (PurchaseInvoices_documentlines.LineTotal) END ), 0) AS TotalPrice, (LineTotal / Quantity) AS UnitPrice, COUNT( DISTINCT PurchaseInvoices_documentlines.InvoiceID ) AS NoOfInvoice FROM `PurchaseInvoices_documentlines` INNER JOIN Item_item ON Item_item.ItemCode = PurchaseInvoices_documentlines.ItemCode INNER JOIN PurchaseInvoices_purchaseinvoices ON PurchaseInvoices_purchaseinvoices.id = PurchaseInvoices_documentlines.InvoiceID INNER JOIN BusinessPartner_businesspartner bp ON bp.CardCode = PurchaseInvoices_purchaseinvoices.CardCode AND bp.U_U_UTL_Zone IN('{zonesStr}') WHERE PurchaseInvoices_purchaseinvoices.CancelStatus = 'csNo' AND (PurchaseInvoices_documentlines.ItemCode != '' AND PurchaseInvoices_documentlines.ItemCode != 'None') AND Item_item.U_UTL_ITSBG = '{SubGroupCode}' { SearchQuery } { fromToDate }"""
            print("sqlQuery subgroupcode",sqlQuery)
            print("--------------------------------------------------------------------")
        elif str(Zone) != "":
            sqlQuery = f"""
                SELECT
                    PurchaseInvoices_documentlines.`id`,
                    PurchaseInvoices_documentlines.`ItemDescription` AS ItemName,
                    PurchaseInvoices_documentlines.ItemCode AS ItemCode,
                    SUM(PurchaseInvoices_documentlines.LineTotal) AS NetTotal,
                    IFNULL(SUM((PurchaseInvoices_documentlines.LineTotal + (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_documentlines.TaxRate / 100))), 0) AS TotalPriceWithoutHeadDiscount,
                    IFNULL(SUM(
                        CASE
                            WHEN PurchaseInvoices_purchaseinvoices.DiscountPercent > 0 THEN
                                (PurchaseInvoices_documentlines.LineTotal - (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_purchaseinvoices.DiscountPercent / 100))
                            ELSE
                                (PurchaseInvoices_documentlines.LineTotal)
                        END
                    ), 0) AS TotalPrice,
                    SUM(PurchaseInvoices_documentlines.Quantity) AS TotalQty,
                    (LineTotal / Quantity) AS UnitPrice,
                    COUNT( DISTINCT PurchaseInvoices_documentlines.InvoiceID ) AS NoOfInvoice
                FROM `PurchaseInvoices_documentlines`
                INNER JOIN Item_item ON Item_item.ItemCode = PurchaseInvoices_documentlines.ItemCode
                INNER JOIN PurchaseInvoices_purchaseinvoices ON PurchaseInvoices_purchaseinvoices.id = PurchaseInvoices_documentlines.InvoiceID
                INNER JOIN BusinessPartner_businesspartner bp ON bp.CardCode = PurchaseInvoices_purchaseinvoices.CardCode AND bp.U_U_UTL_Zone IN('{Zone}')
                WHERE
                    PurchaseInvoices_purchaseinvoices.CancelStatus = 'csNo' 
                    AND (PurchaseInvoices_documentlines.ItemCode != '' AND PurchaseInvoices_documentlines.ItemCode != 'None')
                    { SearchQuery } { fromToDate }
                GROUP BY
                    PurchaseInvoices_documentlines.`ItemCode` { orderby } { limitQuery }
            """
            sqlQuery2 = f"""SELECT PurchaseInvoices_documentlines.`id`, PurchaseInvoices_documentlines.`ItemDescription` AS ItemName, PurchaseInvoices_documentlines.ItemCode AS ItemCode, SUM(PurchaseInvoices_documentlines.LineTotal) AS NetTotal, IFNULL(SUM((PurchaseInvoices_documentlines.LineTotal + (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_documentlines.TaxRate / 100))), 0) AS TotalPriceWithoutHeadDiscount, IFNULL(SUM( CASE WHEN PurchaseInvoices_purchaseinvoices.DiscountPercent > 0 THEN (PurchaseInvoices_documentlines.LineTotal - (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_purchaseinvoices.DiscountPercent / 100)) ELSE (PurchaseInvoices_documentlines.LineTotal) END ), 0) AS TotalPrice, SUM(PurchaseInvoices_documentlines.Quantity) AS TotalQty, (LineTotal / Quantity) AS UnitPrice, COUNT( DISTINCT PurchaseInvoices_documentlines.InvoiceID ) AS NoOfInvoice FROM `PurchaseInvoices_documentlines` INNER JOIN Item_item ON Item_item.ItemCode = PurchaseInvoices_documentlines.ItemCode INNER JOIN PurchaseInvoices_purchaseinvoices ON PurchaseInvoices_purchaseinvoices.id = PurchaseInvoices_documentlines.InvoiceID INNER JOIN BusinessPartner_businesspartner bp ON bp.CardCode = PurchaseInvoices_purchaseinvoices.CardCode AND bp.U_U_UTL_Zone IN('{Zone}') WHERE PurchaseInvoices_purchaseinvoices.CancelStatus = 'csNo' AND (PurchaseInvoices_documentlines.ItemCode != '' AND PurchaseInvoices_documentlines.ItemCode != 'None') { SearchQuery } { fromToDate }"""
            
            # endelse
        else:
            sqlQuery = f"""
                SELECT
                    PurchaseInvoices_documentlines.`id`,
                    PurchaseInvoices_documentlines.`ItemDescription` AS ItemName,
                    PurchaseInvoices_documentlines.ItemCode AS ItemCode,
                    SUM(PurchaseInvoices_documentlines.LineTotal) AS NetTotal,
                    IFNULL(SUM((PurchaseInvoices_documentlines.LineTotal + (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_documentlines.TaxRate / 100))), 0) AS TotalPriceWithoutHeadDiscount,
                    IFNULL(SUM(
                        CASE
                            WHEN PurchaseInvoices_purchaseinvoices.DiscountPercent > 0 THEN
                                (PurchaseInvoices_documentlines.LineTotal - (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_purchaseinvoices.DiscountPercent / 100))
                            ELSE
                                (PurchaseInvoices_documentlines.LineTotal)
                        END
                    ), 0) AS TotalPrice,
                    SUM(PurchaseInvoices_documentlines.Quantity) AS TotalQty,
                    (LineTotal / Quantity) AS UnitPrice,
                    COUNT( DISTINCT PurchaseInvoices_documentlines.InvoiceID ) AS NoOfInvoice
                FROM `PurchaseInvoices_documentlines`
                INNER JOIN Item_item ON Item_item.ItemCode = PurchaseInvoices_documentlines.ItemCode
                INNER JOIN PurchaseInvoices_purchaseinvoices ON PurchaseInvoices_purchaseinvoices.id = PurchaseInvoices_documentlines.InvoiceID
                INNER JOIN BusinessPartner_businesspartner bp ON bp.CardCode = PurchaseInvoices_purchaseinvoices.CardCode AND bp.U_U_UTL_Zone IN('{zonesStr}')
                WHERE
                    PurchaseInvoices_purchaseinvoices.CancelStatus = 'csNo' 
                    AND (PurchaseInvoices_documentlines.ItemCode != '' AND PurchaseInvoices_documentlines.ItemCode != 'None')
                    { SearchQuery } { fromToDate }
                GROUP BY
                    PurchaseInvoices_documentlines.`ItemCode` { orderby } { limitQuery }
            """
            sqlQuery2 = f"""SELECT PurchaseInvoices_documentlines.`id`, PurchaseInvoices_documentlines.`ItemDescription` AS ItemName, PurchaseInvoices_documentlines.ItemCode AS ItemCode, SUM(PurchaseInvoices_documentlines.LineTotal) AS NetTotal, IFNULL(SUM((PurchaseInvoices_documentlines.LineTotal + (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_documentlines.TaxRate / 100))), 0) AS TotalPriceWithoutHeadDiscount, IFNULL(SUM( CASE WHEN PurchaseInvoices_purchaseinvoices.DiscountPercent > 0 THEN (PurchaseInvoices_documentlines.LineTotal - (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_purchaseinvoices.DiscountPercent / 100)) ELSE (PurchaseInvoices_documentlines.LineTotal) END ), 0) AS TotalPrice, SUM(PurchaseInvoices_documentlines.Quantity) AS TotalQty, (LineTotal / Quantity) AS UnitPrice, COUNT( DISTINCT PurchaseInvoices_documentlines.InvoiceID ) AS NoOfInvoice FROM `PurchaseInvoices_documentlines` INNER JOIN Item_item ON Item_item.ItemCode = PurchaseInvoices_documentlines.ItemCode INNER JOIN PurchaseInvoices_purchaseinvoices ON PurchaseInvoices_purchaseinvoices.id = PurchaseInvoices_documentlines.InvoiceID INNER JOIN BusinessPartner_businesspartner bp ON bp.CardCode = PurchaseInvoices_purchaseinvoices.CardCode AND bp.U_U_UTL_Zone IN('{zonesStr}') WHERE PurchaseInvoices_purchaseinvoices.CancelStatus = 'csNo' AND (PurchaseInvoices_documentlines.ItemCode != '' AND PurchaseInvoices_documentlines.ItemCode != 'None') { SearchQuery } { fromToDate }"""
            
            # endelse
        # endelse

        print(sqlQuery)
        # itemList = PurchaseInvoices_documentlines.objects.raw(sqlQuery)
        mycursor.execute(sqlQuery)
        itemList = mycursor.fetchall()
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        print('^^^^^^^^^^^^^^^^^')

        # sqlQuery2 = f"""SELECT PurchaseInvoices_documentlines.`id`, PurchaseInvoices_documentlines.`ItemDescription` AS ItemName, PurchaseInvoices_documentlines.ItemCode AS ItemCode, SUM(PurchaseInvoices_documentlines.LineTotal) AS NetTotal, IFNULL(SUM((PurchaseInvoices_documentlines.LineTotal + (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_documentlines.TaxRate / 100))), 0) AS TotalPriceWithoutHeadDiscount, IFNULL(SUM( CASE WHEN PurchaseInvoices_purchaseinvoices.DiscountPercent > 0 THEN (PurchaseInvoices_documentlines.LineTotal - (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_purchaseinvoices.DiscountPercent / 100)) ELSE (PurchaseInvoices_documentlines.LineTotal) END ), 0) AS TotalPrice, SUM(PurchaseInvoices_documentlines.Quantity) AS TotalQty, (LineTotal / Quantity) AS UnitPrice, COUNT( DISTINCT PurchaseInvoices_documentlines.InvoiceID ) AS NoOfInvoice FROM `PurchaseInvoices_documentlines` INNER JOIN Item_item ON Item_item.ItemCode = PurchaseInvoices_documentlines.ItemCode INNER JOIN PurchaseInvoices_purchaseinvoices ON PurchaseInvoices_purchaseinvoices.id = PurchaseInvoices_documentlines.InvoiceID INNER JOIN BusinessPartner_businesspartner bp ON bp.CardCode = PurchaseInvoices_purchaseinvoices.CardCode AND (PurchaseInvoices_documentlines.ItemCode != '' AND PurchaseInvoices_documentlines.ItemCode != 'None') AND bp.U_U_UTL_Zone IN('{zonesStr}') WHERE PurchaseInvoices_purchaseinvoices.CancelStatus = 'csNo'"""
        print(sqlQuery2)
        mycursor.execute(sqlQuery2)
        totalSalesData = mycursor.fetchall()
        if len(totalSalesData) != 0:
            TotalSales   = float(totalSalesData[0]['TotalPrice'])
            
        # TotalSales = totalPrice
        allCreditNote = 0
            
        return Response({"message": "Success","status": 200, "data":itemList, "TotalSales": round(TotalSales, 2), "TotalCreditNote":-abs(allCreditNote)})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

# >>>>>>>>>>>>>>>>>>>>>>> 
@api_view(["POST"])
def ap_item_overview(request):
    try:
        print("item_overview", json.loads(json.dumps(request.data)))

        allItems = []
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        ItemCode = request.data['ItemCode']

        fromToDate = ""
        if str(FromDate) != "":
            fromToDate = f"AND PurchaseInvoices_purchaseinvoices.DocDate >= '{FromDate}' AND PurchaseInvoices_purchaseinvoices.DocDate <= '{ToDate}'"
        
        if Item.objects.filter(ItemCode = ItemCode).exists():
            itemObj = Item.objects.filter(ItemCode = ItemCode).first()

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
            mycursor = mydb.cursor(dictionary=True, buffered=True)
            # mycursor = db_connection.cursor()
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            UnitPrice  = 0
            totalPrice = 0
            totalQty   = 0
            item_invoice_ids = []
            ordList = []
            sqlQuery2 = f"""
                SELECT
                    PurchaseInvoices_purchaseinvoices.id,
                    PurchaseInvoices_purchaseinvoices.DocDate,
                    MONTH(PurchaseInvoices_purchaseinvoices.DocDate) as Month,
                    PurchaseInvoices_documentlines.`ItemDescription` AS ItemName,
                    PurchaseInvoices_documentlines.ItemCode AS ItemCode,
                    IFNULL(SUM((PurchaseInvoices_documentlines.LineTotal + (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_documentlines.TaxRate / 100))), 0) AS TotalPriceWithoutHeadDiscount,
                    IFNULL(SUM(
                        CASE
                            WHEN PurchaseInvoices_purchaseinvoices.DiscountPercent > 0 THEN
                                (PurchaseInvoices_documentlines.LineTotal - (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_purchaseinvoices.DiscountPercent / 100))
                            ELSE
                                (PurchaseInvoices_documentlines.LineTotal)
                        END
                    ), 0) AS TotalPrice,
                    SUM(PurchaseInvoices_documentlines.Quantity) AS TotalQty
                FROM `PurchaseInvoices_documentlines`
                LEFT JOIN Item_item ON Item_item.ItemCode = PurchaseInvoices_documentlines.ItemCode
                LEFT JOIN PurchaseInvoices_purchaseinvoices ON PurchaseInvoices_purchaseinvoices.id = PurchaseInvoices_documentlines.InvoiceID
                WHERE 
                    PurchaseInvoices_purchaseinvoices.CancelStatus = 'csNo' 
                    AND PurchaseInvoices_documentlines.ItemCode = '{ItemCode}'
                    {fromToDate}
                GROUP BY PurchaseInvoices_purchaseinvoices.CardCode;
            """
            print(sqlQuery2)
            mycursor.execute(sqlQuery2)
            totalSalesData = mycursor.fetchall()
            if len(totalSalesData) != 0:
                for obj in totalSalesData:

                    DocDate   = str(obj['DocDate'])
                    Month   = str(obj['Month'])
                    TotalSales   = float(obj['TotalPrice'])
                    TotalQty   = float(obj['TotalQty'])
                    
                    totalPrice = totalPrice + TotalSales
                    totalQty = totalQty + TotalQty

                    ordContaxt = {
                        "DocTotal": TotalSales,
                        "Month": get_mm_yy(DocDate)
                    }
                    ordList.append(ordContaxt)
                
            MonthGroupSalesList = groupby(ordList, ['DocTotal', 'Month'], "Month", "DocTotal")

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # Total itemTotalSales 
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            itemTotalSales = f"""
                SELECT
                    PurchaseInvoices_purchaseinvoices.id,
                    PurchaseInvoices_purchaseinvoices.DocDate,
                    MONTH(PurchaseInvoices_purchaseinvoices.DocDate) as Month,
                    PurchaseInvoices_documentlines.`ItemDescription` AS ItemName,
                    PurchaseInvoices_documentlines.ItemCode AS ItemCode,
                    IFNULL(SUM(
                        CASE
                            WHEN PurchaseInvoices_purchaseinvoices.DiscountPercent > 0 THEN
                                (PurchaseInvoices_documentlines.LineTotal - (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_purchaseinvoices.DiscountPercent / 100))
                            ELSE
                                (PurchaseInvoices_documentlines.LineTotal)
                        END
                    ), 0) AS TotalPrice,
                    SUM(PurchaseInvoices_documentlines.Quantity) AS TotalQty
                FROM `PurchaseInvoices_documentlines`
                LEFT JOIN Item_item ON Item_item.ItemCode = PurchaseInvoices_documentlines.ItemCode
                LEFT JOIN PurchaseInvoices_purchaseinvoices ON PurchaseInvoices_purchaseinvoices.id = PurchaseInvoices_documentlines.InvoiceID
                WHERE 
                    PurchaseInvoices_purchaseinvoices.CancelStatus = 'csNo' 
                    AND PurchaseInvoices_documentlines.ItemCode = '{ItemCode}'
                    {fromToDate}
            """
            print(itemTotalSales)
            mycursor.execute(itemTotalSales)
            itemTotaldata = mycursor.fetchall()
            OverRollTotalPrice = 0        
            if len(itemTotaldata) > 0:
                OverRollTotalPrice = itemTotaldata[0]['TotalPrice']

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            tempitmObj = PurchaseInvoices_documentlines.objects.filter(ItemCode = ItemCode).order_by('id').last()
            invObj = PurchaseInvoices.objects.filter(pk = tempitmObj.InvoiceID).first()
            LastSalesDate = invObj.DocDate
            
            avgPrice = 0
            if float(totalQty) > 0:
                avgPrice = round(totalPrice / totalQty, 2)

            contaxt = {
                "ItemName":itemObj.ItemName,
                "ItemCode":ItemCode,
                "UnitPrice":avgPrice,
                "TotalPrice": OverRollTotalPrice,
                "TotalQty": totalQty,
                "NoOfInvoice": 0,
                "LastSalesDate": LastSalesDate,

                "TotalItemPrice": OverRollTotalPrice,
                "TotalItemQty": totalQty,

                # "SaleOrder":ordList,
                # "BPGroupSalesList":BPGroupSalesList,
                "MonthGroupSalesList": MonthGroupSalesList
            }
             # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            allItems.append(contaxt)
            return Response({"message": "Success", "status": 200, "data":allItems})
        else:
            return Response({"message": "Invalid ItemCode", "status": 201, "data":[]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})    

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(["POST"])
def ap_item_invoices(request):
    try:
        print("item_invoices", request.data)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        allItems = []
        # CardCode = request.data['CardCode']
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        ItemCode = str(request.data['ItemCode'])
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        SearchQuery = ""
        if 'SearchText' in request.data:
            SearchText = str(request.data['SearchText']).strip()
            if str(SearchText) != "":
                SearchQuery = f"AND PurchaseInvoices_purchaseinvoices.CardName like '%%{SearchText}%%'"
        
        fromToDate = ""
        if str(FromDate) != "":
            fromToDate = f"AND PurchaseInvoices_purchaseinvoices.DocDate >= '{FromDate}' AND PurchaseInvoices_purchaseinvoices.DocDate <= '{ToDate}'"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        OrderByName = "" #a-z/z-a
        OrderByAmt = "" #desc
        if 'OrderByName' in request.data:
            OrderByName = str(request.data['OrderByName']).strip()
        if 'OrderByAmt' in request.data:
            OrderByAmt = str(request.data['OrderByAmt']).strip()
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        orderby = ""
        if str(OrderByName).lower() == 'a-z':
            orderby = "Order By PurchaseInvoices_purchaseinvoices.CardName asc"
        elif str(OrderByName).lower() == 'z-a':
            orderby = "Order By PurchaseInvoices_purchaseinvoices.CardName desc"
        elif str(OrderByAmt).lower() == 'asc':
            orderby = "Order By TotalPrice asc"
        elif str(OrderByAmt).lower() == 'desc':
            orderby = "Order By TotalPrice desc"
        else:
            orderby = "Order By PurchaseInvoices_purchaseinvoices.CardName asc"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
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
        
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        if Item.objects.filter(ItemCode = ItemCode).exists():
            itemObj = Item.objects.filter(ItemCode = ItemCode).first()

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            mydb = mysql.connector.connect(host = settings.DATABASES['default']['HOST'], user = settings.DATABASES['default']['USER'], password = settings.DATABASES['default']['PASSWORD'], database = settings.DATABASES['default']['NAME'] )
            mycursor = mydb.cursor(dictionary=True, buffered=True)
            # mycursor = db_connection.cursor()
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            UnitPrice  = 0
            totalPrice = 0
            totalQty   = 0
            ordList = []
            sqlQuery2 = f"""
                SELECT
                    PurchaseInvoices_purchaseinvoices.id,
                    PurchaseInvoices_purchaseinvoices.CardCode,
                    PurchaseInvoices_purchaseinvoices.CardName,
                    PurchaseInvoices_purchaseinvoices.DocDate,
                    MONTH(PurchaseInvoices_purchaseinvoices.DocDate) as Month,
                    PurchaseInvoices_documentlines.`ItemDescription` AS ItemName,
                    PurchaseInvoices_documentlines.ItemCode AS ItemCode,
                    IFNULL(SUM((PurchaseInvoices_documentlines.LineTotal + (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_documentlines.TaxRate / 100))), 0) AS TotalPriceWithoutHeadDiscount,
                    IFNULL(SUM(
                        CASE
                            WHEN PurchaseInvoices_purchaseinvoices.DiscountPercent > 0 THEN
                                (PurchaseInvoices_documentlines.LineTotal - (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_purchaseinvoices.DiscountPercent / 100))
                            ELSE
                                (PurchaseInvoices_documentlines.LineTotal)
                        END
                    ), 0) AS TotalPrice,
                    SUM(PurchaseInvoices_documentlines.Quantity) AS TotalQty
                FROM `PurchaseInvoices_documentlines`
                LEFT JOIN Item_item ON Item_item.ItemCode = PurchaseInvoices_documentlines.ItemCode
                LEFT JOIN PurchaseInvoices_purchaseinvoices ON PurchaseInvoices_purchaseinvoices.id = PurchaseInvoices_documentlines.InvoiceID
                WHERE 
                    PurchaseInvoices_purchaseinvoices.CancelStatus = 'csNo' 
                    AND PurchaseInvoices_documentlines.ItemCode = '{ItemCode}'
                    {fromToDate}
                    {SearchQuery}
                GROUP BY PurchaseInvoices_purchaseinvoices.CardCode {orderby} {limitQuery};
            """
            print(sqlQuery2)
            mycursor.execute(sqlQuery2)
            totalSalesData = mycursor.fetchall()
            if len(totalSalesData) != 0:
                for obj in totalSalesData:

                    CardCode   = str(obj['CardCode'])
                    CardName   = str(obj['CardName'])
                    Month      = str(obj['Month'])
                    TotalSales = float(obj['TotalPrice'])
                    TotalQty   = float(obj['TotalQty'])
                    
                    totalPrice = totalPrice + TotalSales
                    totalQty = totalQty + TotalQty

                    ordContaxt = {
                        "CardCode": CardCode,
                        "CardName": CardName,
                        "TotalPrice": TotalSales,
                        "TotalQty": TotalQty,
                    }
                    ordList.append(ordContaxt)
            
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # Total itemTotalSales 
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            itemTotalSales = f"""
                SELECT
                    PurchaseInvoices_purchaseinvoices.id,
                    PurchaseInvoices_purchaseinvoices.DocDate,
                    MONTH(PurchaseInvoices_purchaseinvoices.DocDate) as Month,
                    PurchaseInvoices_documentlines.`ItemDescription` AS ItemName,
                    PurchaseInvoices_documentlines.ItemCode AS ItemCode,
                    IFNULL(SUM(
                        CASE
                            WHEN PurchaseInvoices_purchaseinvoices.DiscountPercent > 0 THEN
                                (PurchaseInvoices_documentlines.LineTotal - (PurchaseInvoices_documentlines.LineTotal * PurchaseInvoices_purchaseinvoices.DiscountPercent / 100))
                            ELSE
                                (PurchaseInvoices_documentlines.LineTotal)
                        END
                    ), 0) AS TotalPrice,
                    SUM(PurchaseInvoices_documentlines.Quantity) AS TotalQty
                FROM `PurchaseInvoices_documentlines`
                LEFT JOIN Item_item ON Item_item.ItemCode = PurchaseInvoices_documentlines.ItemCode
                LEFT JOIN PurchaseInvoices_purchaseinvoices ON PurchaseInvoices_purchaseinvoices.id = PurchaseInvoices_documentlines.InvoiceID
                WHERE 
                    PurchaseInvoices_purchaseinvoices.CancelStatus = 'csNo' 
                    AND PurchaseInvoices_documentlines.ItemCode = '{ItemCode}'
                    {fromToDate}
            """
            print(itemTotalSales)
            mycursor.execute(itemTotalSales)
            itemTotaldata = mycursor.fetchall()
            OverRollTotalPrice = 0
            if len(itemTotaldata) > 0:
                OverRollTotalPrice = itemTotaldata[0]['TotalPrice']
                
            contaxt = {
                "ItemName" :itemObj.ItemName,
                "ItemCode" :ItemCode,
                "TotalPrice" : OverRollTotalPrice,
                "TotalQty" : totalQty,
                "BPList"   :ordList,
            }    
            allItems.append(contaxt)
            return Response({"message": "Success", "status": 200, "data":allItems})
        else:
            return Response({"message": "Invalid ItemCode", "status": 201, "data":[]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(["POST"])
def ap_bp_item_invoices(request):
    try:
        allItems = []
        CardCode = request.data['CardCode']
        ItemCode = request.data['ItemCode']
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        if Item.objects.filter(ItemCode = ItemCode).exists():
            itemObj = Item.objects.filter(ItemCode = ItemCode).first()
            invIds = []
            if str(FromDate) != "":
                invIds = list(PurchaseInvoices.objects.filter(CancelStatus="csNo", CardCode = CardCode, DocDate__gte = FromDate, DocDate__lte = ToDate).values_list('id', flat=True).distinct())
            else:
                invIds = list(PurchaseInvoices.objects.filter(CancelStatus="csNo", CardCode = CardCode).values_list('id', flat=True).distinct())
                
            invItemObjs = PurchaseInvoices_documentlines.objects.filter(InvoiceID__in = invIds, ItemCode = ItemCode).order_by("id").values('InvoiceID', 'Quantity', 'UnitPrice', 'LineTotal')
            UnitPrice  = 0
            totalPrice = 0
            totalQty   = 0
            ordList = []
            for itmObj in invItemObjs:
                invObj = PurchaseInvoices.objects.filter(pk = itmObj['InvoiceID']).first()

                DiscountPercent = float(invObj.DiscountPercent)
                
                LineTotal  = float(itmObj['LineTotal'])
                if DiscountPercent > 0:
                    LineTotal = LineTotal - ((LineTotal * DiscountPercent) / 100 )

                UnitPrice  = itmObj['UnitPrice']
                Quantity   = itmObj['Quantity']

                # DocTotal   = int(UnitPrice) * int(Quantity)
                # totalPrice = totalPrice + (int(UnitPrice) * int(Quantity))
                
                totalPrice = totalPrice + float(LineTotal)
                totalQty   = totalQty + int(Quantity)

                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                allPaymentsListBP = []
                if str(FromDate) != "":
                    allPaymentsListBP = VendorPaymentsInvoices.objects.filter(VendorPaymentsId = invObj.DocEntry, DocDate__gte = FromDate, DocDate__lte = ToDate).values_list('SumApplied', flat=True)
                else:
                    allPaymentsListBP = VendorPaymentsInvoices.objects.filter(VendorPaymentsId = invObj.DocEntry).values_list('SumApplied', flat=True)

                # print("allPaymentsListBP", allPaymentsListBP)
                tempPayment = 0
                for item in allPaymentsListBP:
                    tempPayment += float(item)

                PaymentStatus = "Unpaid"
                if invObj.DocumentStatus == "bost_Close":
                    PaymentStatus = "Paid"
                elif len(allPaymentsListBP) != 0:
                    PaymentStatus = "Partially Paid"
                else:
                    PaymentStatus = "Unpaid"
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                ordContaxt = {
                    "InvoiceId":itmObj['InvoiceID'],
                    "DocEntry":invObj.DocEntry,
                    "UnitPrice": UnitPrice,
                    "Quantity": Quantity,
                    "DocTotal": LineTotal,
                    "CreateDate": invObj.DocDate,
                    "PaymentStatus": PaymentStatus,
                }
                ordList.append(ordContaxt)
            # end for
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
            contaxt = {
                "ItemName":itemObj.ItemName,
                "ItemCode":ItemCode,
                "CardName": bpobj.CardName,
                "CardCode": bpobj.CardCode,
                "EmailAddress": bpobj.EmailAddress,
                "Phone1": bpobj.Phone1,
                "GSTIN": GSTIN,
                "BPAddress": BPAddress,
                "GroupName": GroupName,
                "CreditLimit": CreditLimit,
                "CreditLimitDayes": creditLimitDayes,
                "TotalPrice": totalPrice,
                "TotalQty": totalQty,
                "SaleOrder":ordList,
            }    
            allItems.append(contaxt)
            return Response({"message": "Success", "status": 200, "data":allItems})
        else:
            return Response({"message": "Invalid ItemCode", "status": 201, "data":[]})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})


