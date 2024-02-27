# */2 * * * * /usr/bin/python3 /home/www/b2b/vision_sales_support_pre/bridge/Invoice/INV.py
# */2 * * * * /usr/bin/python3 /home/www/b2b/vision_sales_support_dev/bridge/Invoice/INV.py
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

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
# if True:
try:
    settings.custome_error_logs('cron start', module_name='gl_account')

    lastCode = 0
    mycursor.execute("SELECT * FROM `Company_glaccounts` ORDER BY `id` desc LIMIT 1")
    entryData = mycursor.fetchall()
    if len(entryData) > 0:
        print(entryData)
        lastCode = entryData[0]['Code']
        print(lastCode)

    skip=0
    # for i in range(count):
    while skip != "":
        # sapAPIUrl = f"/ChartOfAccounts?$filter = Code gt {lastCode}&$skip = {skip}"
        sapAPIUrl = f"/ChartOfAccounts?$skip = {skip}"
        print(sapAPIUrl)
        res = requests.get(settings.SAPURL+sapAPIUrl, cookies=ses.cookies, verify=False)
        # print(res.text)
        opts = json.loads(res.text)
        print("no of Accounts",len(opts['value']))
        for opt in opts['value']:
            print(opt)
            Code = opt['Code']
            Name = opt['Name'].replace("'","").replace('"', '')
            print("Code: ", Code)

            checkPaymentQuery = f"select * from Company_glaccounts WHERE Code = '{Code}'"
            print(checkPaymentQuery)
            mycursor.execute(checkPaymentQuery)
            if mycursor.rowcount == 0:
                add_sql = f'INSERT INTO `Company_glaccounts`(`Code`, `Name`) VALUES("{Code}", "{Name}")'
                print(add_sql) 
                mycursor.execute(add_sql)
                mydb.commit()

            # endif
        # endfor
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
    # endWhile
    settings.custome_error_logs('cron end', module_name='gl_account')
except Exception as e:
    print("Exception: ", str(e))
    settings.custome_error_logs(message=str(e), module_name='gl_account')
