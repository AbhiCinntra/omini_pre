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
    settings.custome_error_logs('cron start', module_name='inv_incoming_payments_status')

    currentDate = date.today() - timedelta(days=10)
    invCount = requests.get(settings.SAPURL+"/IncomingPayments/$count", cookies=ses.cookies, verify=False).text

    # count the number if loop run, each one skip 20 values
    count = math.ceil(int(invCount)/20)
    # print(count)
    if int(count) > 0:
        skip=0
        for i in range(count):
            baseUrl = settings.SAPURL+"/IncomingPayments?$orderby = DocEntry asc&$select=DocEntry,DocNum,DocType,CardCode,CardName,JournalRemarks&$skip="+str(skip)
            print(baseUrl)
            res = requests.get(baseUrl, cookies=ses.cookies, verify=False)
            opts = json.loads(res.text)
            # print(opts)
            for opt in opts['value']:
                DocEntry = opt['DocEntry']
                print("DocEntry: ", DocEntry)
                docSelectQuery = f"select * from Invoice_incomingpayments WHERE DocEntry = '{DocEntry}'"
                print(docSelectQuery)
                mycursor.execute(docSelectQuery)
                mycursor.fetchall()
                if mycursor.rowcount > 0:                
                    CardCode = opt['CardCode']
                    JournalRemarks = opt['JournalRemarks']
                    ord_sql = f"UPDATE `Invoice_incomingpayments` SET `JournalRemarks`='{JournalRemarks}' WHERE DocEntry = '{DocEntry}'"
                    print(ord_sql)
                    mycursor.execute(ord_sql)
                    mydb.commit()             
                    # InvoiceID = mycursor.lastrowid

            print('___')
            skip = skip+20
            print(skip)
    settings.custome_error_logs('cron end', module_name='inv_incoming_payments_status')
except Exception as e:
    print(str(e))
    settings.custome_error_logs(message=str(e), module_name='inv_incoming_payments_status')