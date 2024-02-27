import requests, json
import time
import math
import mysql.connector

from datetime import datetime
from datetime import date, datetime, timedelta
import calendar

import sys, os
import urllib.parse

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
    settings.custome_error_logs('cron start', module_name='ap_order')
        
    lastDocEntry = 0
    # lastDocEntry = 10189
    mycursor.execute("SELECT * FROM `PurchaseOrders_purchaseorders` ORDER BY `id` desc LIMIT 1")
    entryData = mycursor.fetchall()
    if len(entryData) > 0:
        lastDocEntry = entryData[0]['DocEntry']

    skip=0
    # for i in range(count):
    while skip != "": 
        # res = requests.get(data['sapurl']+'/PurchaseOrders?$filter=UpdateDate ge '+str(currentDate)+'&$skip='+str(skip)+'', cookies=r.cookies, verify=False)
        sapAPIUrl = f"/PurchaseOrders?$orderby = DocEntry asc&$filter = DocEntry gt {lastDocEntry}&$skip = {skip}"
        #print(sapAPIUrl)
        res = requests.get(settings.SAPURL+sapAPIUrl, cookies=ses.cookies, verify=False)
        # #print(res.text)
        opts = json.loads(res.text)
        for opt in opts['value']:

            DocEntry = opt['DocEntry']
            print("Top DocEntry: ", DocEntry)
            # OrderID = str(opt['U_PORTAL_NO']) # local order id
        
            docSelectQuery = f"select * from PurchaseOrders_purchaseorders WHERE DocEntry = '{DocEntry}'"
            #print(docSelectQuery)
            mycursor.execute(docSelectQuery)
            mycursor.fetchall()
            if mycursor.rowcount != 1:
                        
                d = datetime.strptime(str(opt['DocTime']), "%H:%M:%S")
                DocTime = d.strftime("%I:%M:%S %p")

                e = datetime.strptime(str(opt['UpdateTime']), "%H:%M:%S")
                UpdateTime = e.strftime("%I:%M:%S %p")  

                discountPercent = 0
                if str(opt['DiscountPercent']) != 'None':
                    discountPercent = float(opt['DiscountPercent'])
                    if discountPercent < 0:
                        discountPercent = 0
                
                CardCode = opt['CardCode']
                DeliveryCharge = 0
                AdditionalCharges = 0
                if len(opt['DocumentAdditionalExpenses']) !=0:
                    for val in opt['DocumentAdditionalExpenses']:
                        AdditionalCharges = AdditionalCharges + float(val['LineTotal'])

                # str(discountPercent)
                DocTotal = opt['DocTotal']
                CardName = str(opt['CardName']).replace("'","").replace("\\", "")
                Comments = str(opt['Comments']).replace("'","").replace("\\", "")
                BPLID    = str(opt['BPL_IDAssignedToInvoice'])
                BPLName  = str(opt['BPLName'])
                WTAmount = str(opt['WTAmount'])
                U_E_INV_NO  = '' # str(opt['U_E_INV_NO'])
                U_E_INV_Date = '' # str(opt['U_E_INV_Date'])
                U_TransporterID = '' # str(opt['U_TransporterID'])
                U_TransporterName = '' # str(opt['U_TransporterName'])
                U_UNE_LRDate = '' # str(opt['U_UNE_LRDate'])
                U_VehicalNo = '' # str(opt['U_VehicalNo'])
                U_UNE_LRNo  = '' # str(opt['U_UNE_LRNo'])
                U_UNE_IRN   = '' # str(opt['U_UNE_IRN'])
                NumAtCard = str(opt['NumAtCard']).replace("'","").replace("\\", "")
                IGST      = 0.0
                CGST      = 0.0
                SGST      = 0.0
                GSTRate   = 0.0
                IRNNo     = ""
                CNNo      = ""
                Address   = str(opt['Address']).replace("'","").replace('"', "")
                Address2  = str(opt['Address2']).replace("'","").replace('"', "")
                VATRegNum = str(opt['VATRegNum']).replace("'","").replace("\\", "")
                DocNum    = str(opt['DocNum'])
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                # seriesNameURL = f"http://103.107.67.172:8000/Ledure/General/SeriesName.xsjs?DBName=LEDURE_LIVE_300323&DocEntry={DocEntry}&ObjType=18"
                # print(seriesNameURL)
                # seriesNameResponse = requests.get(seriesNameURL, cookies=r.cookies, verify=False)
                # seriesNameJson = json.loads(seriesNameResponse.text)
                # seriesNameData = seriesNameJson['value']
                # if len(seriesNameData) > 0:
                #     IRNNo = seriesNameData[0]['IRNNo']
                #     CNNo = f"{seriesNameData[0]['SeriesName']}/{DocNum}"

                ord_sql = "INSERT INTO `PurchaseOrders_purchaseorders`(`DocNum`, `TaxDate`, `DocDueDate`, `ContactPersonCode`, `DiscountPercent`, `DocDate`, `CardCode`, `Comments`,`BPLID`,`BPLName`,`WTAmount`,`U_E_INV_NO`,`U_E_INV_Date`, `SalesPersonCode`, `DocumentStatus`, `DocCurrency`, `DocTotal`, `CardName`, `VatSum`, `CreationDate`, `DocEntry`, `CreateDate`, `CreateTime`, `UpdateDate`, `UpdateTime`, `DeliveryCharge`,`AdditionalCharges`, `PaymentGroupCode`,`Series`,`CancelStatus`, `DocType`, `IGST`, `CGST`, `SGST`, `RoundingDiffAmount`, `GSTRate`, `U_SignedQRCode`, `U_SignedInvoice`, `U_EWayBill`,`U_TransporterID`,`U_TransporterName`,`U_VehicalNo`,`NumAtCard`,`U_UNE_LRNo`,`U_UNE_LRDate`,`U_UNE_IRN`, `CNNo`, `Address`, `Address2`,`VATRegNum`) VALUES ('"+str(opt['DocNum'])+"','"+str(opt['TaxDate'])+"', '"+str(opt['DocDueDate'])+"', '"+str(opt['ContactPersonCode'])+"', '"+str(discountPercent)+"', '"+str(opt['DocDate'])+"', '"+str(opt['CardCode'])+"', '"+str(Comments)+"','"+str(BPLID)+"', '"+str(BPLName)+"','"+str(WTAmount)+"', '"+str(U_E_INV_NO)+"', '"+str(U_E_INV_Date)+"', '"+str(opt['SalesPersonCode'])+"', '"+str(opt['DocumentStatus'])+"', '"+str(opt['DocCurrency'])+"', '"+str(opt['DocTotal'])+"', '"+str(CardName)+"', '"+str(opt['VatSum'])+"', '"+str(opt['CreationDate'])+"', '"+str(opt['DocEntry'])+"', '"+str(opt['CreationDate'])+"','','', '"+str(UpdateTime)+"', '"+str(DeliveryCharge)+"', '"+str(AdditionalCharges)+"', '"+str(opt['PaymentGroupCode'])+"', '"+str(opt['Series'])+"', '"+str(opt['CancelStatus'])+"', '"+str(opt['DocType'])+"', '', '', '', '"+str(opt['RoundingDiffAmount'])+"', '', '"+str(opt['U_SignedQRCode'])+"', '"+str(opt['U_SignedInvoice'])+"', '"+str(opt['U_EWayBill'])+"', '"+str(U_TransporterID)+"', '"+str(U_TransporterName)+"', '"+str(U_VehicalNo)+"', '"+str(NumAtCard)+"', '"+str(U_UNE_LRNo)+"', '"+str(U_UNE_LRDate)+"', '"+str(IRNNo)+"', '"+str(CNNo)+"', '"+str(Address)+"', '"+str(Address2)+"', '"+str(VATRegNum)+"');"
            
                print(ord_sql)
                mycursor.execute(ord_sql)
                mydb.commit()                
                OrderID = mycursor.lastrowid
                
                add = opt['AddressExtension']                    
                ShipToStreet    = str(add['ShipToStreet']).replace("'", "\\")
                ShipToBlock     = str(add['ShipToBlock']).replace("'", "\\")
                ShipToBuilding  = str(add['ShipToBuilding']).replace("'", "\\")
                ShipToCity      = str(add['ShipToCity']).replace("'", "\\")
                ShipToZipCode   = str(add['ShipToZipCode']).replace("'", "\\")
                ShipToCounty    = str(add['ShipToCounty']).replace("'", "\\")
                ShipToState     = str(add['ShipToState']).replace("'", "\\")
                ShipToCountry   = str(add['ShipToCountry']).replace("'", "\\")
                ShipToAddress2  = str(add['ShipToAddress2']).replace("'", "\\")
                ShipToAddress3  = str(add['ShipToAddress3']).replace("'", "\\")
                BillToStreet    = str(add['BillToStreet']).replace("'", "\\")
                BillToBlock     = str(add['BillToBlock']).replace("'", "\\")
                BillToBuilding  = str(add['BillToBuilding']).replace("'", "\\")
                BillToCity      = str(add['BillToCity']).replace("'", "\\")
                BillToZipCode   = str(add['BillToZipCode']).replace("'", "\\")
                BillToCounty    = str(add['BillToCounty']).replace("'", "\\")
                BillToState     = str(add['BillToState']).replace("'", "\\")
                BillToCountry   = str(add['BillToCountry']).replace("'", "\\")
                BillToAddress2  = str(add['BillToAddress2']).replace("'", "\\")
                BillToAddress3  = str(add['BillToAddress3']).replace("'", "\\")
                PlaceOfSupply   = str(add['PlaceOfSupply']).replace("'", "\\")
                PurchasePlaceOfSupply = str(add['PurchasePlaceOfSupply']).replace("'", "\\")
                U_SCOUNTRY      = ""
                U_SSTATE        = ""
                U_SHPTYPB       = ""
                U_BSTATE        = ""
                U_BCOUNTRY      = ""
                U_SHPTYPS       = ""

                add_sql = f"INSERT INTO `PurchaseOrders_addressextension`(`OrderID`, `ShipToStreet`, `ShipToBlock`, `ShipToBuilding`, `ShipToCity`, `ShipToZipCode`, `ShipToCounty`, `ShipToState`, `ShipToCountry`, `ShipToAddress2`, `ShipToAddress3`, `BillToStreet`, `BillToBlock`, `BillToBuilding`, `BillToCity`, `BillToZipCode`, `BillToCounty`, `BillToState`, `BillToCountry`, `BillToAddress2`, `BillToAddress3`, `PlaceOfSupply`, `PurchasePlaceOfSupply`, `U_SCOUNTRY`, `U_SSTATE`, `U_SHPTYPB`, `U_BSTATE`, `U_BCOUNTRY`, `U_SHPTYPS`) VALUES ('{OrderID}','{ShipToStreet}','{ShipToBlock}','{ShipToBuilding}','{ShipToCity}','{ShipToZipCode}','{ShipToCounty}','{ShipToState}','{ShipToCountry}','{ShipToAddress2}','{ShipToAddress3}','{BillToStreet}','{BillToBlock}','{BillToBuilding}','{BillToCity}','{BillToZipCode}','{BillToCounty}','{BillToState}','{BillToCountry}','{BillToAddress2}','{BillToAddress3}','{PlaceOfSupply}','{PurchasePlaceOfSupply}','{U_SCOUNTRY}','{U_SSTATE}','{U_SHPTYPB}','{U_BSTATE}','{U_BCOUNTRY}','{U_SHPTYPS}');"
                #print(add_sql)                
                mycursor.execute(add_sql)
                mydb.commit()

                itemCount = 0
                totalPrice = DocTotal
                for line in opt['DocumentLines']:
                    #print(line['Quantity'])
                    #print(line['DiscountPercent'])
                    
                    lDiscountPercent = line['DiscountPercent']
                    if str(lDiscountPercent) == 'None':
                        lDiscountPercent = 0.0
                    
                    BaseEntry = str(line['BaseEntry']) # sap order id
                    TaxRate = str(line['TaxPercentagePerRow'])

                    # tax igst cgst sgst
                    taxDocLines = line['LineTaxJurisdictions']
                    GSTRate = 0
                    if len(taxDocLines) > 1:
                        GSTRate = float(taxDocLines[0]['TaxRate'])
                        CGST = CGST + float(taxDocLines[0]['TaxAmount'])
                        SGST = SGST + float(taxDocLines[1]['TaxAmount'])

                    FreeText = str(line['FreeText']).replace("'","\\'")
                    HSNEntry = str(line['HSNEntry'])
                    SACEntry = str(line['SACEntry'])
                    HSN = ""
                    SAC = ""

                    RemainingOpenQuantity = str(line['RemainingOpenQuantity'])
                    OpenAmount = str(line['OpenAmount'])
                    LineStatus = str(line['LineStatus'])

                    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                    # if HSNEntry != "None":
                    #     hsnAPIRsponse = requests.get(f"http://103.107.67.172:8000/Ledure/General/GetHSN.xsjs?DBName=LEDURE_LIVE_300323&AbsEntry={HSNEntry}", cookies=r.cookies, verify=False)
                    #     rsponseJson = json.loads(hsnAPIRsponse.text)
                    #     print(rsponseJson)
                    #     rsponseData = rsponseJson['value']
                    #     if len(rsponseData) > 0:
                    #         HSN = rsponseData[0]['HSN']
                    # elif SACEntry != "None":
                    #     sacAPIRsponse = requests.get(f"http://103.107.67.172:8000/Ledure/General/GetSacName.xsjs?DBName=LEDURE_LIVE_300323&AbsEntry={SACEntry}", cookies=r.cookies, verify=False)
                    #     rsponseJson = json.loads(sacAPIRsponse.text)
                    #     print(rsponseJson)
                    #     rsponseData = rsponseJson['value']
                    #     if len(rsponseData) > 0:
                    #         SAC = rsponseData[0]['SacCode']
                    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                    U_UTL_DIST = ''
                    U_UTL_SP = ''
                    U_UTL_DD = ''
                    U_UTL_SD = ''
                    U_UTL_TD = ''
                    U_UTL_MRPI = ''
                    U_RateType = ''
                    line_sql = "INSERT INTO `PurchaseOrders_documentlines`(`LineNum`, `OrderID`, `Quantity`, `UnitPrice`, `DiscountPercent`, `ItemDescription`, `ItemCode`, `TaxCode`, `BaseEntry`, `TaxRate`, `UomNo`, `LineTotal`, `U_UTL_DIST`, `U_UTL_SP`, `U_UTL_DD`, `U_UTL_SD`, `U_UTL_TD`, `U_UTL_MRPI`, `U_RateType`,`MeasureUnit`, `HSNEntry`, `SACEntry`, `HSN`, `SAC`, `RemainingOpenQuantity`, `OpenAmount`,`LineStatus`) VALUES ('"+str(line['LineNum'])+"', '"+str(OrderID)+"', '"+str(line['Quantity'])+"', '"+str(line['UnitPrice'])+"', '"+str(lDiscountPercent)+"', '"+str(line['ItemDescription'])+"', '"+str(line['ItemCode'])+"', '"+str(line['TaxCode'])+"', '"+str(BaseEntry)+"', '"+str(TaxRate)+"', '"+str(line['UoMCode'])+"', '"+str(line['LineTotal'])+"','"+str(U_UTL_DIST)+"','"+str(U_UTL_SP)+"','"+str(U_UTL_DD)+"','"+str(U_UTL_SD)+"','"+str(U_UTL_TD)+"','"+str(U_UTL_MRPI)+"','"+str(U_RateType)+"','"+str(line['MeasureUnit'])+"','"+str(HSNEntry)+"','"+str(SACEntry)+"','"+str(HSN)+"','"+str(SAC)+"','"+str(RemainingOpenQuantity)+"','"+str(OpenAmount)+"', '"+str(LineStatus)+"');"
                    #print(line_sql)
                    mycursor.execute(line_sql)
                    mydb.commit()
                    itemCount = itemCount+1
                # endfor
                sqlInvUpd = f"UPDATE `PurchaseOrders_purchaseorders` SET `IGST` = '{IGST}', `CGST` = '{CGST}', `SGST` = '{SGST}', `GSTRate` = '{GSTRate}' WHERE `id` = '{OrderID}'"
                print(sqlInvUpd)
                mycursor.execute(sqlInvUpd)
                mydb.commit()
                bpid = mycursor.lastrowid
            # endif
            else:
                CardCode = opt['CardCode']
                CancelStatus = opt['CancelStatus']
                DocumentStatus = opt['DocumentStatus']
                ord_sql = f"UPDATE `PurchaseOrders_purchaseorders` SET `DocumentStatus`='{DocumentStatus}', `CancelStatus` = '{CancelStatus}' WHERE DocEntry = '{DocEntry}'"
                print(ord_sql)
                mycursor.execute(ord_sql)
                mydb.commit()

        if 'odata.nextLink' in opts:
            nextLink = opts['odata.nextLink'] 
            nextLink = nextLink.split("skip=") 
            skip = str(nextLink[1]).strip()
        else: 
            skip = ""
            exit()
    # endwhile
    settings.custome_error_logs('cron end', module_name='ap_order')
except Exception as e:
    print(str(e))
    settings.custome_error_logs(message=str(e), module_name='ap_order')

