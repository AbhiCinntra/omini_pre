import requests, json
import time
import math
import mysql.connector

from datetime import datetime
from datetime import date, datetime, timedelta
import calendar

import sys, os

from requests.adapters import HTTPAdapter, Retry

currentDate = date.today()
currentDay = calendar.day_name[currentDate.weekday()]  # this will return the day of a week
currentTime = datetime.today().strftime("%I:%M %p")
currentDateTime = f"{currentDate} {currentTime}"
serverDateTime = datetime.now()
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#                   import settings file
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
import sys, os
from pathlib import Path
project_base_dir = Path(__file__).resolve().parent.parent
setting_final_path = os.path.join(project_base_dir, 'bridge')
# print("final_path", setting_final_path)
sys.path.append(setting_final_path)
import settings
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
ses = ""
if __name__ == '__main__':
	ses = settings.SAPSESSIONNEW("core")
else:
	ses = settings.SAPSESSIONNEW("api")
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
mydb = mysql.connector.connect(
  host=settings.DATABASES['default']['HOST'],
  user=settings.DATABASES['default']['USER'],
  password=settings.DATABASES['default']['PASSWORD'],
  database=settings.DATABASES['default']['NAME']
)
mycursor = mydb.cursor(buffered=True, dictionary=True)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
try:
    settings.custome_error_logs('cron start', module_name='ord')

    lastDocEntry = 0
    mycursor.execute("SELECT * FROM `Order_order` ORDER BY `id` desc LIMIT 1")
    entryData = mycursor.fetchall()
    if len(entryData) > 0:
        lastDocEntry = entryData[0]['DocEntry']
        print(lastDocEntry)

    skip=0
    # for i in range(count):
    while skip != "":        
        sapAPIUrl = f"/Orders?$orderby = DocEntry asc &$filter = DocEntry gt {lastDocEntry}&$skip = {skip}"
        print(sapAPIUrl)
        res = requests.get(settings.SAPURL+sapAPIUrl, cookies=ses.cookies, headers={"Prefer":"odata.maxpagesize=500"}, verify=False)
        # print(res.text)
        opts = json.loads(res.text)
        for opt in opts['value']:
            DocEntry = opt['DocEntry']
            print("DocEntry: ", DocEntry)
            # OrderID = str(opt['U_PORTAL_NO']) # local order id
        
            docSelectQuery = f"select * from Order_order WHERE DocEntry = '{DocEntry}'"
            print(docSelectQuery)
            mycursor.execute(docSelectQuery)
            mycursor.fetchall()
            if mycursor.rowcount != 1:

                d = datetime.strptime(str(opt['DocTime']), "%H:%M:%S")
                DocTime = d.strftime("%I:%M:%S %p")

                e = datetime.strptime(str(opt['UpdateTime']), "%H:%M:%S")
                UpdateTime = e.strftime("%I:%M:%S %p")  

                discountPercent = opt['DiscountPercent']
                if str(discountPercent) == 'None':
                    discountPercent = 0

                
                CardCode = opt['CardCode']
                DeliveryCharge = 0
                AdditionalCharges = 0
                if len(opt['DocumentAdditionalExpenses']) !=0:
                    DeliveryCharge = opt['DocumentAdditionalExpenses'][0]['LineTotal']
                    # AdditionalCharges = opt['DocumentAdditionalExpenses'][1]['LineTotal']


                TaxDate = opt['TaxDate']
                DocDueDate = opt['DocDueDate']
                ContactPersonCode = opt['ContactPersonCode']
                DiscountPercent = discountPercent
                DocDate = opt['DocDate']
                CardCode = opt['CardCode']
                Comments = opt['Comments']
                SalesPersonCode = opt['SalesPersonCode']
                DocumentStatus = opt['DocumentStatus']
                DocCurrency = opt['DocCurrency']
                DocTotal = opt['DocTotal']
                CardName = str(opt['CardName']).replace("'","\\'")
                VatSum = opt['VatSum']
                CreationDate = opt['CreationDate']
                DocEntry = opt['DocEntry']
                DocNum = opt['DocNum']
                CreateDate = opt['CreationDate']
                CreateTime = ""
                UpdateDate = opt['UpdateDate']
                UpdateTime = ""
                U_OPPID = ""
                U_OPPRNM = ""
                U_QUOTID = ""
                U_QUOTNM = ""
                CancelStatus = opt['CancelStatus']
                NetTotal = 0.0
                AdditionalCharges = AdditionalCharges
                DeliveryCharge = DeliveryCharge
                DeliveryMode = ""
                DeliveryTerm = ""
                PaymentType = ""
                TermCondition = ""
                Unit = opt['BPL_IDAssignedToInvoice']
                U_LAT = ""
                U_LONG = ""
                Link = ""
                PayTermsGrpCode = opt['PaymentGroupCode']
                ApprovalStatus = ""
                ApproverId = ""
                FreeDelivery = ""
                CreatedBy = opt['SalesPersonCode']
                ord_sql = f'INSERT INTO `Order_order`(`TaxDate`, `DocDueDate`, `ContactPersonCode`, `DiscountPercent`, `DocDate`, `CardCode`, `Comments`, `SalesPersonCode`, `DocumentStatus`, `DocCurrency`, `DocTotal`, `CardName`, `VatSum`, `CreationDate`, `DocEntry`, `CreateDate`, `CreateTime`, `UpdateDate`, `UpdateTime`, `U_OPPID`, `U_OPPRNM`, `U_QUOTID`, `U_QUOTNM`, `CancelStatus`, `NetTotal`, `AdditionalCharges`, `DeliveryCharge`, `DeliveryMode`, `DeliveryTerm`, `PaymentType`, `TermCondition`, `Unit`, `U_LAT`, `U_LONG`, `Link`, `PayTermsGrpCode`, `ApprovalStatus`, `ApproverId`, `FreeDelivery`, `CreatedBy`, `DocNum`) VALUES ("{TaxDate}","{DocDueDate}","{ContactPersonCode}","{DiscountPercent}","{DocDate}","{CardCode}","{Comments}","{SalesPersonCode}","{DocumentStatus}","{DocCurrency}","{DocTotal}","{CardName}","{VatSum}","{CreationDate}","{DocEntry}","{CreateDate}","{CreateTime}","{UpdateDate}","{UpdateTime}","{U_OPPID}","{U_OPPRNM}","{U_QUOTID}","{U_QUOTNM}","{CancelStatus}","{NetTotal}","{AdditionalCharges}","{DeliveryCharge}","{DeliveryMode}","{DeliveryTerm}","{PaymentType}","{TermCondition}","{Unit}","{U_LAT}","{U_LONG}","{Link}","{PayTermsGrpCode}","{ApprovalStatus}","{ApproverId}","{FreeDelivery}","{CreatedBy}", "{DocNum}")'
            
                print(ord_sql)
                mycursor.execute(ord_sql)
                mydb.commit()                
                OrderID = mycursor.lastrowid
                
                add = opt['AddressExtension']
                U_SCOUNTRY  = ""
                U_SSTATE    = ""
                U_SHPTYPB   = ""
                U_BSTATE    = ""
                U_BCOUNTRY  = ""
                U_SHPTYPS   = ""

                ShipToBuilding = str(add['ShipToBuilding']).replace("'","\\'").replace('"', '')
                BillToBuilding = str(add['BillToBuilding']).replace("'","\\'").replace('"', '')
                ShipToStreet = str(add['ShipToStreet']).replace("'","\\'").replace('"', '')
                BillToStreet = str(add['BillToStreet']).replace("'","\\'").replace('"', '')

                # BillToBuilding = add['BillToBuilding']
                ShipToState = str(add['ShipToState']).replace("'","\\'").replace('"', '')
                BillToCity = str(add['BillToCity']).replace("'","\\'").replace('"', '')
                ShipToCountry = str(add['ShipToCountry']).replace("'","\\'").replace('"', '')
                BillToZipCode = str(add['BillToZipCode']).replace("'","\\'").replace('"', '')
                BillToState = str(add['BillToState']).replace("'","\\'").replace('"', '')
                ShipToZipCode = str(add['ShipToZipCode']).replace("'","\\'").replace('"', '')
                ShipToCity = str(add['ShipToCity']).replace("'","\\'").replace('"', '')
                BillToCountry = str(add['BillToCountry']).replace("'","\\'").replace('"', '')
                U_SCOUNTRY  = ""
                U_SSTATE    = ""
                U_SHPTYPB   = ""
                U_BSTATE    = ""
                U_BCOUNTRY  = ""
                U_SHPTYPS   = ""
                BillToDistrict = ""
                ShipToDistrict = ""

                add_sql = f'INSERT INTO `Order_addressextension`(`OrderID`, `BillToBuilding`, `ShipToState`, `BillToCity`, `ShipToCountry`, `BillToZipCode`, `ShipToStreet`, `BillToState`, `ShipToZipCode`, `BillToStreet`, `ShipToBuilding`, `ShipToCity`, `BillToCountry`, `U_SCOUNTRY`, `U_SSTATE`, `U_SHPTYPB`, `U_BSTATE`, `U_BCOUNTRY`, `U_SHPTYPS`, `BillToDistrict`, `ShipToDistrict`) VALUES ("{OrderID}", "{BillToBuilding}", "{ShipToState}", "{BillToCity}", "{ShipToCountry}", "{BillToZipCode}", "{ShipToStreet}", "{BillToState}", "{ShipToZipCode}", "{BillToStreet}", "{ShipToBuilding}", "{ShipToCity}", "{BillToCountry}", "{U_SCOUNTRY}", "{U_SSTATE}", "{U_SHPTYPB}", "{U_BSTATE}", "{U_BCOUNTRY}", "{U_SHPTYPS}", "{BillToDistrict}", "{ShipToDistrict}")'
                print(add_sql)                
                mycursor.execute(add_sql)
                mydb.commit()

                itemCount = 0
                totalPrice = DocTotal
                for line in opt['DocumentLines']:
                    print(line['Quantity'])
                    print(line['DiscountPercent'])
                    
                    # lDiscountPercent = 0.0
                    # if line['DiscountPercent'] == None or line['DiscountPercent'] == 0:
                    #     lDiscountPercent = 0.0
                    # else:
                    #     lDiscountPercent = float(line['DiscountPercent'])
                    
                    lDiscountPercent = line['DiscountPercent']
                    if str(lDiscountPercent) == 'None':
                        lDiscountPercent = 0
                    
                    BaseEntry      = str(line['BaseEntry']) # sap order id
                    TaxRate        = str(line['TaxPercentagePerRow'])
                    FreeText       = str(line['FreeText']).replace("'","\\'")
                    LineNum        = line['LineNum']
                    Quantity       = line['Quantity']
                    UnitPrice      = line['UnitPrice']
                    DiscountPercent = lDiscountPercent
                    ItemDescription = str(line['ItemDescription']).replace("'","\\'").replace('"', ' ')
                    ItemCode       = line['ItemCode']
                    TaxCode        = line['TaxCode']
                    FreeText       = str(line['FreeText']).replace("'","\\'").replace('"', ' ')
                    UnitWeight     = ""
                    UomNo          = ""
                    TaxRate        = str(line['TaxPercentagePerRow'])
                    UnitPriceown   = line['UnitPrice']
                    RemainingOpenQuantity = line['RemainingOpenQuantity']
                    OpenAmount     = line['OpenAmount']
                    LineTotal      = line['LineTotal']
                    LineStatus     = line['LineStatus']

                    Price          = line['Price']
                    PriceAfterVAT  = line['PriceAfterVAT']

                    line_sql = f'INSERT INTO `Order_documentlines`(`LineNum`, `OrderID`, `Quantity`, `UnitPrice`, `DiscountPercent`, `ItemDescription`, `ItemCode`, `TaxCode`, `FreeText`, `UnitWeight`, `UomNo`, `TaxRate`, `UnitPriceown`, `RemainingOpenQuantity`, `OpenAmount`, `LineTotal`, `LineStatus`, `Price`, `PriceAfterVAT`) VALUES ("{LineNum}", "{OrderID}", "{Quantity}", "{UnitPrice}", "{DiscountPercent}", "{ItemDescription}", "{ItemCode}", "{TaxCode}", "{FreeText}", "{UnitWeight}", "{UomNo}", "{TaxRate}", "{UnitPriceown}", "{RemainingOpenQuantity}","{OpenAmount}", "{LineTotal}", "{LineStatus}", "{Price}", "{PriceAfterVAT}")'

                    print(line_sql)
                    mycursor.execute(line_sql)
                    mydb.commit()
                    itemCount = itemCount+1
                

        if 'odata.nextLink' in opts:
            nextLink = opts['odata.nextLink']
            print(">>>>>>>>>>>>>>>>>>>>> nextLink: ", nextLink)
            nextLink = nextLink.split("skip=")
            print(nextLink)
            skip = str(nextLink[1]).strip()

        else:
            print("<<<<<<<<<<<<<<<<<<<<< nextLink: ", "")
            skip = ""
            exit()

        print("skip", skip)
    # endwhile
    settings.custome_error_logs('cron end', module_name='ord')
except Exception as e:
    print(str(e))
    settings.custome_error_logs(message=str(e), module_name='ord')