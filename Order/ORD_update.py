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

print('>>>>>>>>>>>> ledure_pre <<<<<<<<<<<<<<<<<<<<')
mydb = mysql.connector.connect(
    host='localhost',
    # user='root',
    # password='root',
    user='admin',
    password='Cinntra@1234',  
    database='rg_industries_prod'
)
mycursor = mydb.cursor(dictionary=True, buffered=True)

print("<><><><><><><><><><><>><><><><><><")
print("===== Login SAP ====")
data = { "CompanyDB": "RG_Industries_Live_", "UserName": "manager", "Password": "RG@123456", "SessionId": "a8e91956-7c8c-11ee-8000-0a427ed74412", "at": "2023-11-06 15:40:06", "sapurl": "https://103.190.95.182:50000/b1s/v1" }
r = requests.post(data['sapurl']+'/Login', data=json.dumps(data), verify=False)
print(r)
tempDate = date.today() - timedelta(days=5)

lastDocEntry = 0
selectQu = f"SELECT * FROM `Order_order` WHERE `DocumentStatus` = 'bost_Open' AND DocEntry >= {lastDocEntry}"
mycursor.execute(selectQu)
openOrdersList = mycursor.fetchall()
if len(openOrdersList) > 0:
    skip=0
    # while skip != "":     
    for ord in openOrdersList:   
        DocEntry = ord['DocEntry']
        print("DocEntry: ", DocEntry)
        sapAPIUrl = f"/Orders?$filter = DocEntry eq {DocEntry}&$skip = {skip}"
        # sapAPIUrl = f"/Orders?$filter = DocumentStatus eq 'bost_Open' and DocEntry ge {lastDocEntry}&$skip = {skip}"
        # sapAPIUrl = f"/Orders?$filter=DocumentStatus ne 'bost_Open' and UpdateDate ge {str(tempDate)}&$skip = {skip}"
        print(sapAPIUrl)
        res = requests.get(data['sapurl']+sapAPIUrl, cookies=r.cookies, verify=False)
        # print(res.text)
        opts = json.loads(res.text)
        for opt in opts['value']:
            DocEntry = opt['DocEntry']        
            docSelectQuery = f"select * from Order_order WHERE DocEntry = '{DocEntry}'"
            print(docSelectQuery)
            mycursor.execute(docSelectQuery)
            ordDetails = mycursor.fetchall()
            if mycursor.rowcount == 1:
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                # 
                #                                       Update Order
                #   
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                OrderID = ordDetails[0]['id']    
                d = datetime.strptime(str(opt['DocTime']), "%H:%M:%S")
                DocTime = d.strftime("%I:%M:%S %p")

                e = datetime.strptime(str(opt['UpdateTime']), "%H:%M:%S")
                UpdateTime = e.strftime("%I:%M:%S %p")

                # discountPercent = str(opt['DiscountPercent'])
                # if str(discountPercent) == 'None':
                #     discountPercent = 0.0

                discountPercent = opt['DiscountPercent']
                if str(discountPercent) == 'None':
                    discountPercent = 0

                
                CardCode = opt['CardCode']
                DeliveryCharge = 0
                AdditionalCharges = 0

                if len(opt['DocumentAdditionalExpenses']) !=0:
                    DeliveryCharge = opt['DocumentAdditionalExpenses'][0]['LineTotal']
                    AdditionalCharges = opt['DocumentAdditionalExpenses'][1]['LineTotal']

                # str(discountPercent)
                TaxDate         = opt['TaxDate']
                DocDueDate      = opt['DocDueDate']
                ContactPersonCode = opt['ContactPersonCode']
                DiscountPercent = discountPercent
                DocDate         = opt['DocDate']
                CardCode        = opt['CardCode']
                Comments        = str(opt['Comments']).replace("'","\\'").replace('"', '')
                SalesPersonCode = opt['SalesPersonCode']
                DocumentStatus  = opt['DocumentStatus']
                DocCurrency     = opt['DocCurrency']
                DocTotal        = opt['DocTotal']
                CardName        = str(opt['CardName']).replace("'","\\'").replace('"', '')
                VatSum          = opt['VatSum']
                CreationDate    = opt['CreationDate']
                DocEntry        = opt['DocEntry']
                DocNum          = opt['DocNum']
                CreateDate      = opt['CreationDate']
                CreateTime      = ""
                UpdateDate      = opt['UpdateDate']
                CancelStatus    = opt['CancelStatus']
                NetTotal        = 0.0
                AdditionalCharges = AdditionalCharges
                DeliveryCharge  = DeliveryCharge
                Unit            = opt['BPL_IDAssignedToInvoice']
                PayTermsGrpCode = opt['PaymentGroupCode']
                CreatedBy       = opt['SalesPersonCode']
                
                ord_sql = f"UPDATE `Order_order` SET `DocNum` = '{DocNum}', `TaxDate` = '{TaxDate}',`DocDueDate` = '{DocDueDate}',`ContactPersonCode` = '{ContactPersonCode}',`DiscountPercent` = '{DiscountPercent}',`DocDate` = '{DocDate}', `Comments` = '{Comments}',`DocumentStatus` = '{DocumentStatus}',`DocCurrency` = '{DocCurrency}',`DocTotal` = '{DocTotal}',`VatSum` = '{VatSum}',`UpdateDate` = '{UpdateDate}',`UpdateTime` = '{UpdateTime}',`CancelStatus` = '{CancelStatus}', `NetTotal` = '{NetTotal}', `AdditionalCharges` = '{AdditionalCharges}', `DeliveryCharge` = '{DeliveryCharge}', `Unit` = '{Unit}',`PayTermsGrpCode` = '{PayTermsGrpCode}' WHERE `DocEntry` = '{DocEntry}'"
                print(ord_sql)
                mycursor.execute(ord_sql)
                mydb.commit()
                
                # add            = opt['AddressExtension']
                # ShipToBuilding = str(add['ShipToBuilding']).replace("'","\\'")
                # BillToBuilding = str(add['BillToBuilding']).replace("'","\\'")
                # ShipToStreet   = str(add['ShipToStreet']).replace("'","\\'")
                # BillToStreet   = str(add['BillToStreet']).replace("'","\\'")
                # ShipToState    = add['ShipToState']
                # BillToCity     = add['BillToCity']
                # ShipToCountry  = add['ShipToCountry']
                # BillToZipCode  = add['BillToZipCode']
                # BillToState    = add['BillToState']
                # ShipToZipCode  = add['ShipToZipCode']
                # ShipToCity     = add['ShipToCity']
                # BillToCountry  = add['BillToCountry']

                # update_address = f"UPDATE `Order_addressextension` SET `BillToBuilding` = '{BillToBuilding}',`ShipToState` = '{ShipToState}',`BillToCity` = '{BillToCity}',`ShipToCountry` = '{ShipToCountry}',`BillToZipCode` = '{BillToZipCode}',`ShipToStreet` = '{ShipToStreet}',`BillToState` = '{BillToState}',`ShipToZipCode` = '{ShipToZipCode}',`BillToStreet` = '{BillToStreet}',`ShipToBuilding` = '{ShipToBuilding}',`ShipToCity` = '{ShipToCity}',`BillToCountry` = '{BillToCountry}' WHERE `OrderID` = '{OrderID}'"
                
                # print(update_address)                
                # mycursor.execute(update_address)
                # mydb.commit()

                itemCount = 0
                totalPrice = DocTotal
                for line in opt['DocumentLines']:
                    print(line['Quantity'])
                    print(line['DiscountPercent'])
                    
                    # lDiscountPercent = str(line['DiscountPercent'])
                    # if str(lDiscountPercent) == 'None':
                    #     lDiscountPercent = 0.0
                    lDiscountPercent = line['DiscountPercent']
                    if str(lDiscountPercent) == 'None':
                        lDiscountPercent = 0

                    BaseEntry       = str(line['BaseEntry']) # sap order id
                    TaxRate         = str(line['TaxPercentagePerRow'])
                    FreeText        = str(line['FreeText']).replace("'","\\'").replace('"', '')
                    LineNum         = line['LineNum']
                    Quantity        = line['Quantity']
                    UnitPrice       = line['UnitPrice']
                    DiscountPercent = lDiscountPercent
                    ItemDescription = str(line['ItemDescription']).replace("'","\\'").replace('"', '')
                    ItemCode        = line['ItemCode']
                    TaxCode         = line['TaxCode']
                    UnitPriceown    = line['UnitPrice']
                    UnitWeight      = ""
                    UomNo           = ""
                    RemainingOpenQuantity = line['RemainingOpenQuantity']
                    OpenAmount      = line['OpenAmount']
                    LineTotal       = line['LineTotal']
                    LineStatus      = line['LineStatus']

                    docLineQuery = f"select * from Order_documentlines WHERE `OrderID` = '{OrderID}' AND `LineNum` = '{LineNum}'"
                    print(docLineQuery)
                    mycursor.execute(docLineQuery)
                    if mycursor.rowcount > 0:
                        line_sql = f"UPDATE `Order_documentlines` SET `Quantity` = '{Quantity}',`UnitPrice` = '{UnitPrice}',`DiscountPercent` = '{DiscountPercent}',`ItemDescription` = '{ItemDescription}',`ItemCode` = '{ItemCode}',`TaxCode` = '{TaxCode}',`FreeText` = '{FreeText}',`TaxRate` = '{TaxRate}',`UnitPriceown` = '{UnitPriceown}', `RemainingOpenQuantity` = '{RemainingOpenQuantity}', `OpenAmount` = '{OpenAmount}', `LineTotal` = '{LineTotal}', `LineStatus` = '{LineStatus}' WHERE `OrderID` = '{OrderID}' AND `LineNum` = '{LineNum}'"
                        print(line_sql)
                        mycursor.execute(line_sql)
                        mydb.commit()
                        itemCount = itemCount + 1
                    else:
                        line_sql = f"INSERT INTO `Order_documentlines`(`LineNum`, `OrderID`, `Quantity`, `UnitPrice`, `DiscountPercent`, `ItemDescription`, `ItemCode`, `TaxCode`, `FreeText`, `UnitWeight`, `UomNo`, `TaxRate`, `UnitPriceown`, `RemainingOpenQuantity`, `OpenAmount`, `LineTotal`, `LineStatus`) VALUES ('{LineNum}', '{OrderID}', '{Quantity}', '{UnitPrice}', '{DiscountPercent}', '{ItemDescription}', '{ItemCode}', '{TaxCode}', '{FreeText}', '{UnitWeight}', '{UomNo}', '{TaxRate}', '{UnitPriceown}', '{RemainingOpenQuantity}', '{OpenAmount}', '{LineTotal}', '{LineStatus}')"
                        print(line_sql)
                        mycursor.execute(line_sql)
                        mydb.commit()

                # end for
            # end if
            else:
                continue
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                # 
                #                                           Insert Order
                #   
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                d = datetime.strptime(str(opt['DocTime']), "%H:%M:%S")
                DocTime = d.strftime("%I:%M:%S %p")

                e = datetime.strptime(str(opt['UpdateTime']), "%H:%M:%S")
                UpdateTime = e.strftime("%I:%M:%S %p")  
                
                discountPercent = opt['DiscountPercent']
                if str(discountPercent) == 'None':
                    discountPercent = 0.0

                CardCode = opt['CardCode']
                DeliveryCharge = 0
                AdditionalCharges = 0
                if len(opt['DocumentAdditionalExpenses']) !=0:
                    DeliveryCharge = opt['DocumentAdditionalExpenses'][0]['LineTotal']
                    AdditionalCharges = opt['DocumentAdditionalExpenses'][1]['LineTotal']

                # str(discountPercent)
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
                ord_sql = f"INSERT INTO `Order_order`(`TaxDate`, `DocDueDate`, `ContactPersonCode`, `DiscountPercent`, `DocDate`, `CardCode`, `Comments`, `SalesPersonCode`, `DocumentStatus`, `DocCurrency`, `DocTotal`, `CardName`, `VatSum`, `CreationDate`, `DocEntry`, `CreateDate`, `CreateTime`, `UpdateDate`, `UpdateTime`, `U_OPPID`, `U_OPPRNM`, `U_QUOTID`, `U_QUOTNM`, `CancelStatus`, `NetTotal`, `AdditionalCharges`, `DeliveryCharge`, `DeliveryMode`, `DeliveryTerm`, `PaymentType`, `TermCondition`, `Unit`, `U_LAT`, `U_LONG`, `Link`, `PayTermsGrpCode`, `ApprovalStatus`, `ApproverId`, `FreeDelivery`, `CreatedBy`, `DocNum`) VALUES ('{TaxDate}','{DocDueDate}','{ContactPersonCode}','{DiscountPercent}','{DocDate}','{CardCode}','{Comments}','{SalesPersonCode}','{DocumentStatus}','{DocCurrency}','{DocTotal}','{CardName}','{VatSum}','{CreationDate}','{DocEntry}','{CreateDate}','{CreateTime}','{UpdateDate}','{UpdateTime}','{U_OPPID}','{U_OPPRNM}','{U_QUOTID}','{U_QUOTNM}','{CancelStatus}','{NetTotal}','{AdditionalCharges}','{DeliveryCharge}','{DeliveryMode}','{DeliveryTerm}','{PaymentType}','{TermCondition}','{Unit}','{U_LAT}','{U_LONG}','{Link}','{PayTermsGrpCode}','{ApprovalStatus}','{ApproverId}','{FreeDelivery}','{CreatedBy}', '{DocNum}')"
            
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

                ShipToBuilding = str(add['ShipToBuilding']).replace("'","\\'")
                BillToBuilding = str(add['BillToBuilding']).replace("'","\\'")
                ShipToStreet = str(add['ShipToStreet']).replace("'","\\'")
                BillToStreet = str(add['BillToStreet']).replace("'","\\'")

                BillToBuilding = add['BillToBuilding']
                ShipToState = add['ShipToState']
                BillToCity = add['BillToCity']
                ShipToCountry = add['ShipToCountry']
                BillToZipCode = add['BillToZipCode']
                ShipToStreet = add['ShipToStreet']
                BillToState = add['BillToState']
                ShipToZipCode = add['ShipToZipCode']
                BillToStreet = add['BillToStreet']
                ShipToBuilding = add['ShipToBuilding']
                ShipToCity = add['ShipToCity']
                BillToCountry = add['BillToCountry']
                U_SCOUNTRY  = ""
                U_SSTATE    = ""
                U_SHPTYPB   = ""
                U_BSTATE    = ""
                U_BCOUNTRY  = ""
                U_SHPTYPS   = ""
                BillToDistrict = ""
                ShipToDistrict = ""

                add_sql = f"INSERT INTO `Order_addressextension`(`OrderID`, `BillToBuilding`, `ShipToState`, `BillToCity`, `ShipToCountry`, `BillToZipCode`, `ShipToStreet`, `BillToState`, `ShipToZipCode`, `BillToStreet`, `ShipToBuilding`, `ShipToCity`, `BillToCountry`, `U_SCOUNTRY`, `U_SSTATE`, `U_SHPTYPB`, `U_BSTATE`, `U_BCOUNTRY`, `U_SHPTYPS`, `BillToDistrict`, `ShipToDistrict`) VALUES ('{OrderID}', '{BillToBuilding}', '{ShipToState}', '{BillToCity}', '{ShipToCountry}', '{BillToZipCode}', '{ShipToStreet}', '{BillToState}', '{ShipToZipCode}', '{BillToStreet}', '{ShipToBuilding}', '{ShipToCity}', '{BillToCountry}', '{U_SCOUNTRY}', '{U_SSTATE}', '{U_SHPTYPB}', '{U_BSTATE}', '{U_BCOUNTRY}', '{U_SHPTYPS}', '{BillToDistrict}', '{ShipToDistrict}')"
                print(add_sql)                
                mycursor.execute(add_sql)
                mydb.commit()

                itemCount = 0
                totalPrice = DocTotal
                for line in opt['DocumentLines']:
                    print(line['Quantity'])
                    print(line['DiscountPercent'])
                    
                    lDiscountPercent = 0.0
                    if line['DiscountPercent'] == None or line['DiscountPercent'] == 0:
                        lDiscountPercent = 0.0
                    else:
                        lDiscountPercent = float(line['DiscountPercent'])
                    
                    BaseEntry      = str(line['BaseEntry']) # sap order id
                    TaxRate        = str(line['TaxPercentagePerRow'])
                    FreeText       = str(line['FreeText']).replace("'","\\'")
                    LineNum        = line['LineNum']
                    Quantity       = line['Quantity']
                    UnitPrice      = line['UnitPrice']
                    DiscountPercent = lDiscountPercent
                    ItemDescription = str(line['ItemDescription']).replace("'","\\'")
                    ItemCode       = line['ItemCode']
                    TaxCode        = line['TaxCode']
                    FreeText       = str(line['FreeText']).replace("'","\\'")
                    UnitWeight     = ""
                    UomNo          = ""
                    TaxRate        = str(line['TaxPercentagePerRow'])
                    UnitPriceown   = line['UnitPrice']
                    RemainingOpenQuantity = line['RemainingOpenQuantity']
                    OpenAmount     = line['OpenAmount']
                    LineTotal      = line['LineTotal']
                    LineStatus     = line['LineStatus']

                    line_sql = f"INSERT INTO `Order_documentlines`(`LineNum`, `OrderID`, `Quantity`, `UnitPrice`, `DiscountPercent`, `ItemDescription`, `ItemCode`, `TaxCode`, `FreeText`, `UnitWeight`, `UomNo`, `TaxRate`, `UnitPriceown`, `RemainingOpenQuantity`, `OpenAmount`, `LineTotal`, `LineStatus`) VALUES ('{LineNum}', '{OrderID}', '{Quantity}', '{UnitPrice}', '{DiscountPercent}', '{ItemDescription}', '{ItemCode}', '{TaxCode}', '{FreeText}', '{UnitWeight}', '{UomNo}', '{TaxRate}', '{UnitPriceown}', '{RemainingOpenQuantity}','{OpenAmount}', '{LineTotal}', '{LineStatus}')"

                    print(line_sql)
                    mycursor.execute(line_sql)
                    mydb.commit()
                    itemCount = itemCount+1
        # end for             

        # if 'odata.nextLink' in opts:
        #     nextLink = opts['odata.nextLink']
        #     print(">>>>>>>>>>>>>>>>>>>>> nextLink: ", nextLink)
        #     nextLink = nextLink.split("skip=")
        #     print(nextLink)
        #     skip = str(nextLink[1]).strip()
        # else:
        #     print("<<<<<<<<<<<<<<<<<<<<< nextLink: ", "")
        #     skip = ""
        #     exit()
        # print("skip", skip)
    # endwhile
# endIf

