import requests, json
import time
import math
import mysql.connector

import sys, os
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
	settings.custome_error_logs('cron start', module_name='inds')

	sapData = requests.get(settings.SAPURL+'/Industries/$count', cookies=ses.cookies, verify=False)
	print("sapData ", sapData.text)

	# count the number if loop run, each one skip 20 values
	count = math.ceil(int(sapData.text)/20)
	print(count)
	skip=0
	for i in range(count):
		res = requests.get(settings.SAPURL+'/Industries?$skip='+str(skip), cookies=ses.cookies, verify=False)
		inds = json.loads(res.text)

		for ind in inds['value']:
			print('-----SalePersons---')
			IndustryDescription = ind['IndustryDescription']
			IndustryName = ind['IndustryName']
			IndustryCode = ind['IndustryCode']

			mycursor.execute("select * from Industries_industries where IndustryCode='"+str(ind['IndustryCode'])+"'")
			mycursor.fetchall()
			rc = mycursor.rowcount
			if rc == 0:
				ind_sql = f"INSERT INTO `Industries_industries` (`IndustryDescription`, `IndustryName`, `IndustryCode`) VALUES ('{IndustryDescription}','{IndustryName}','{IndustryCode}')"
				print(ind_sql)
				mycursor.execute(ind_sql)
				mydb.commit()
			else:
				ind_sql = f"UPDATE `Industries_industries` SET `IndustryDescription`='{IndustryDescription}',`IndustryName`='{IndustryName}' WHERE `IndustryCode` = {IndustryCode}"
				print(ind_sql)
				mycursor.execute(ind_sql)
				mydb.commit()
		# endfor
		skip = skip + 20
	# endfor
	settings.custome_error_logs('cron end', module_name='inds')
except Exception as e:
    print("Exception: ", str(e))
    settings.custome_error_logs(message=str(e), module_name='inds')
