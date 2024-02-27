# */2 * * * * /usr/bin/python3 /home/www/b2b/shivtara_live/bridge/Invoice/INV.py
# */2 * * * * /usr/bin/python3 /home/www/b2b/shivtara_live/bridge/Invoice/INV.py
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
    settings.custome_error_logs('cron start', module_name='ord_status')
    
    invCount = requests.get(settings.SAPURL+"/Orders/$count", cookies=ses.cookies, verify=False).text

    # count the number if loop run, each one skip 20 values
    count = math.ceil(int(invCount)/20)
    print(count)

    skip=0
    for i in range(count):
        res = requests.get(settings.SAPURL+"/Orders?$select=DocEntry,DocNum,DocType,CardCode,CardName,DocumentStatus,UpdateDate,CancelStatus&$skip="+str(skip), cookies=ses.cookies, verify=False)
        opts = json.loads(res.text)
        # print(opts)
        for opt in opts['value']:
            DocEntry = opt['DocEntry']
            print("DocEntry: ", DocEntry)
            # OrderID = str(opt['U_PORTAL_NO']) # local order id
        
            docSelectQuery = f"select * from Order_order WHERE DocEntry = '{DocEntry}'"
            print(docSelectQuery)
            mycursor.execute(docSelectQuery)
            mycursor.fetchall()
            if mycursor.rowcount > 0:                
                CardCode = opt['CardCode']
                DocNum = opt['DocNum']
                DocumentStatus = opt['DocumentStatus']
                CancelStatus = opt['CancelStatus']
                ord_sql = f"UPDATE `Order_order` SET `DocNum` = '{DocNum}', `DocumentStatus`='{DocumentStatus}', `CancelStatus` = '{CancelStatus}' WHERE DocEntry = '{DocEntry}'"
                print(ord_sql)
                mycursor.execute(ord_sql)
                mydb.commit()             
                InvoiceID = mycursor.lastrowid
        print('___')
        skip = skip+20
        print(skip)
    settings.custome_error_logs('cron end', module_name='ord_status')
except Exception as e:
    print(str(e))
    settings.custome_error_logs(message=str(e), module_name='ord_status')