# 0 */2 * * * /usr/bin/python3 /home/www/b2b/rg_industries_prod/bridge/JournalEntries/sync_reconcilation.py

import requests, json
import time
import math
import mysql.connector

from datetime import datetime
from datetime import date, datetime, timedelta
import calendar

import sys, os
import urllib.parse

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
    settings.custome_error_logs('cron start', module_name='cancel_entry_update')

    # startDate = date.today() - timedelta(days=10)
    startDate = '2023-03-31'
    endDate = currentDate

    # sapUrl = f"http://103.190.95.182:8000/Ledure/General/Reconcilation_New.xsjs?DBName=RG_Industries_Live_&From={startDate}&ToDate={endDate}"
    sapUrl = f"http://103.107.67.172:8000/Ledure/Report/CancelTransaction.xsjs"
    print(sapUrl)
    sacAPIRsponse = requests.get(sapUrl, verify=False)
    rsponseJson = json.loads(sacAPIRsponse.text)
    # print(rsponseJson)
    rsponseData = rsponseJson['CancelDocument']["0"]
    print("No of CancelEntry", len(rsponseData))
    # exit()
    allQuery = ""
    if len(rsponseData) != 0:
        for obj in rsponseData:
            print(obj['TransId'])
            TransId     = obj['TransId']
            # Document    = obj['Document Type']
            ObjType     = obj['ObjType']
            DocNum      = obj['DocNum']
            DocumentDate = obj['DocumentDate']
            DocTotal    = obj['DocTotal']
            U_Cancel    = 'N' # obj['U_Cancel']

            # update cancel status of Journal Entries
            updateJE = f"UPDATE `JournalEntries_journalentries` SET `U_Cancel` = '{U_Cancel}' WHERE `JdtNum` = '{TransId}';" 
            print(updateJE)
            mycursor.execute(updateJE)
            mydb.commit()
            # continue

            # update cancel status of Invoice
            if ObjType == "13":
                updateInv = f"UPDATE `Invoice_invoice` SET `CancelStatus` = 'csYes' WHERE DocNum = '{DocNum}';" 
                print(updateInv)
                mycursor.execute(updateInv)
                mydb.commit()

            # update cancel status of credite note
            elif ObjType == "14":
                updateInv = f"UPDATE `Invoice_creditnotes` SET `CancelStatus` = 'csYes' WHERE DocNum = '{DocNum}';" 
                print(updateInv)
                mycursor.execute(updateInv)
                mydb.commit()

            # update cancel status of Purchase Invoice
            elif ObjType == "18":
                updateInv = f"UPDATE `PurchaseInvoices_purchaseinvoices` SET `CancelStatus` = 'csYes' WHERE DocNum = '{DocNum}';"
                print(updateInv)
                mycursor.execute(updateInv)
                mydb.commit()

            # update cancel status of Purchase CreditNOte
            elif ObjType == "19":
                updateInv = f"UPDATE `PurchaseInvoices_purchasecreditnotes` SET `CancelStatus` = 'csYes' WHERE DocNum = '{DocNum}';"
                print(updateInv)
                mycursor.execute(updateInv)
                mydb.commit()

            # update cancel status of Incomming Payments
            elif ObjType == "24":
                updateInv = f"UPDATE `Invoice_incomingpayments` SET `JournalRemarks` = 'Canceled' WHERE DocNum = '{DocNum}';"
                print(updateInv)
                mycursor.execute(updateInv)
                mydb.commit()
            # end else
        # end for
    # end if
    else:
        # print(rsponseData)
        settings.custome_error_logs(str(rsponseData), module_name='cancel_entry_update')
    settings.custome_error_logs('cron end', module_name='cancel_entry_update')
except Exception as e:
    print(str(e))
    settings.custome_error_logs(message=str(e), module_name='cancel_entry_update')    