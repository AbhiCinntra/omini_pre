import requests, json
import time
import math
import mysql.connector

from datetime import datetime
from datetime import date, datetime, timedelta
import calendar

import sys, os

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
    settings.custome_error_logs('cron start', module_name='dnote')

    lastDocEntry = 0
    mycursor.execute("SELECT * FROM `DeliveryNote_deliverynote` ORDER BY `id` desc LIMIT 1")
    entryData = mycursor.fetchall()
    if len(entryData) > 0:
        lastDocEntry = entryData[0]['DocEntry']
        print(lastDocEntry)

    skip=0
    while skip != "": 
        sapAPIUrl = f"/DeliveryNotes?$filter = DocEntry gt {lastDocEntry}&$skip = {skip}"
        print(sapAPIUrl)
        # res = requests.get(data['sapurl']+sapAPIUrl, cookies=r.cookies, verify=False)
        res = requests.get(settings.SAPURL+sapAPIUrl, cookies=ses.cookies, verify=False)
        # print(res.text)
        opts = json.loads(res.text)
        for opt in opts['value']:
            DocEntry = opt['DocEntry']
            print("DocEntry: ", DocEntry)
            # OrderID = str(opt['U_PORTAL_NO']) # local order id
        
            docSelectQuery = f"select * from DeliveryNote_deliverynote WHERE DocEntry = '{DocEntry}'"
            print(docSelectQuery)
            mycursor.execute(docSelectQuery)
            mycursor.fetchall()
            if mycursor.rowcount != 1:

                BaseType = opt['DocumentLines'][0]['BaseType']
                # if str(BaseType) != 17 or str(BaseType) != 15:
                if str(BaseType) != '17':
                    print("<><><><><><><><><", str(BaseType))
                    continue
                else:
                    print(">>>>>>>>>>>>>>>>>", str(BaseType))
                        
                d = datetime.strptime(str(opt['DocTime']), "%H:%M:%S")
                DocTime = d.strftime("%I:%M:%S %p")

                e = datetime.strptime(str(opt['UpdateTime']), "%H:%M:%S")
                UpdateTime = e.strftime("%I:%M:%S %p")  

                discountPercent = str(opt['DiscountPercent'])
                if discountPercent == "None":
                    discountPercent = 0
    
                CardCode = opt['CardCode']
                
                # str(discountPercent)
                DocTotal = opt['DocTotal']
                CardName = str(opt['CardName']).replace("'","\\'")
                ord_sql = "INSERT INTO `DeliveryNote_deliverynote`(`TaxDate`, `DocDueDate`, `ContactPersonCode`, `DiscountPercent`, `DocDate`, `CardCode`, `Comments`, `SalesPersonCode`, `DocumentStatus`, `DocCurrency`, `DocTotal`, `CardName`, `VatSum`, `CreationDate`, `DocEntry`, `CreateDate`, `CreateTime`, `UpdateDate`, `UpdateTime`, `OrderID` ,`CancelStatus`) VALUES ('"+str(opt['TaxDate'])+"', '"+str(opt['DocDueDate'])+"', '"+str(opt['ContactPersonCode'])+"', '"+str(discountPercent)+"', '"+str(opt['DocDate'])+"', '"+str(opt['CardCode'])+"', '"+str(opt['Comments'])+"', '"+str(opt['SalesPersonCode'])+"', '"+str(opt['DocumentStatus'])+"', '"+str(opt['DocCurrency'])+"', '"+str(opt['DocTotal'])+"', '"+str(CardName)+"', '"+str(opt['VatSum'])+"', '"+str(opt['CreationDate'])+"', '"+str(opt['DocEntry'])+"', '"+str(opt['CreationDate'])+"','','', '"+str(UpdateTime)+"', '', '"+str(opt['CancelStatus'])+"')"
            
                print(ord_sql)
                mycursor.execute(ord_sql)
                mydb.commit()                
                DeliveryNoteID = mycursor.lastrowid
                
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

                add_sql = "INSERT INTO `DeliveryNote_addressextension`(`DeliveryNoteID`, `BillToBuilding`, `ShipToState`, `BillToCity`, `ShipToCountry`, `BillToZipCode`, `ShipToStreet`, `BillToState`, `ShipToZipCode`, `BillToStreet`, `ShipToBuilding`, `ShipToCity`, `BillToCountry`, `U_SCOUNTRY`, `U_SSTATE`, `U_SHPTYPB`, `U_BSTATE`, `U_BCOUNTRY`, `U_SHPTYPS`) VALUES ('"+str(DeliveryNoteID)+"', '"+str(BillToBuilding)+"', '"+str(add['ShipToState'])+"', '"+str(add['BillToCity'])+"', '"+str(add['ShipToCountry'])+"', '"+str(add['BillToZipCode'])+"', '"+str(ShipToStreet)+"', '"+str(add['BillToState'])+"', '"+str(add['ShipToZipCode'])+"', '"+str(BillToStreet)+"', '"+str(ShipToBuilding)+"', '"+str(add['ShipToCity'])+"', '"+str(add['BillToCountry'])+"', '"+str(U_SCOUNTRY)+"', '"+str(U_SSTATE)+"', '"+str(U_SHPTYPB)+"', '"+str(U_BSTATE)+"', '"+str(U_BCOUNTRY)+"', '"+str(U_SHPTYPS)+"');"
                print(add_sql)                
                mycursor.execute(add_sql)
                mydb.commit()

                itemCount = 0
                totalPrice = DocTotal
                for line in opt['DocumentLines']:
                    lDiscountPercent = str(line['DiscountPercent'])
                    if lDiscountPercent == "None":
                        lDiscountPercent = 0

                    BaseEntry = str(line['BaseEntry']) # sap order id
                    TaxRate = str(line['TaxPercentagePerRow'])

                    FreeText = str(line['FreeText']).replace("'","\\'")
                    line_sql = "INSERT INTO `DeliveryNote_documentlines`(`LineNum`, `DeliveryNoteID`, `Quantity`, `UnitPrice`, `DiscountPercent`, `ItemDescription`, `ItemCode`, `TaxCode`, `BaseEntry`, `TaxRate`, `UomNo`) VALUES ('"+str(line['LineNum'])+"', '"+str(DeliveryNoteID)+"', '"+str(line['Quantity'])+"', '"+str(line['UnitPrice'])+"', '"+str(lDiscountPercent)+"', '"+str(line['ItemDescription'])+"', '"+str(line['ItemCode'])+"', '"+str(line['TaxCode'])+"', '"+str(BaseEntry)+"', '"+str(TaxRate)+"', '"+str(line['UoMCode'])+"');"


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
    settings.custome_error_logs('cron end', module_name='dnote')
except Exception as e:
        print(str(e))
        settings.custome_error_logs(message=str(e), module_name='dnote')


