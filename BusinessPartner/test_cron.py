
import json
import requests
import mysql.connector
from datetime import date, datetime
import calendar

currentDate = date.today()
currentDay = calendar.day_name[currentDate.weekday()]  # this will return the day of a week
currentTime = datetime.today().strftime("%I:%M %p")
currentDateTime = f"{currentDate} {currentTime}"
serverDateTime = datetime.now()

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#                   import settings file
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
import sys
from pathlib import Path
import os
project_base_dir = Path(__file__).resolve().parent.parent
setting_final_path = os.path.join(project_base_dir, 'bridge')
print("final_path", setting_final_path)
sys.path.append(setting_final_path)
import settings
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
sap_session_obj = ""
if __name__ == '__main__':
	sap_session_obj = settings.SAPSESSIONNEW("core")
else:
	sap_session_obj = settings.SAPSESSIONNEW("api")
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# get db connection
# mycursor = getDBConnection()
mydb = mysql.connector.connect(
    host=settings.DATABASES['default']['HOST'],
    user=settings.DATABASES['default']['USER'],
    password=settings.DATABASES['default']['PASSWORD'],
    database=settings.DATABASES['default']['NAME']
)
mycursor = mydb.cursor(buffered=True, dictionary=True)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def BusinessPartnerSync():
    try:
        settings.custome_error_logs('cron start', module_name='test_cron')
        # bpObj = BusinessPartner.objects.all().latest()
        currentDate = '2020-01-01'
        baseUrl = f"/BusinessPartners?$filter = CreateDate ge '{str(currentDate)}'"
        res = requests.get(settings.SAPURL+baseUrl, cookies=sap_session_obj.cookies, headers={"Prefer":"odata.maxpagesize=100"}, verify=False)
        print("res", res)
        opts = json.loads(res.text)
        print("opts", opts)
        for bp in opts['value']:  
            print('CardCode', bp['CardCode'])

        settings.custome_error_logs('cron end', module_name='test_cron')
    except Exception as e:
        print(str(e))
        settings.custome_error_logs(message=str(e), module_name='test_cron')

BusinessPartnerSync()