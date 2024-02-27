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
try:
	settings.custome_error_logs('cron start', module_name='import-category')
		
	# exit()
	# res = requests.get(data['sapurl']+'/ItemGroups/$count', headers={'Authorization': "Bearer "+data['SessionId']+""}, verify=False)
	res = requests.get(settings.SAPURL+'/ItemGroups/$count', cookies=ses.cookies, verify=False)
	print(res.text)

	pages = math.ceil(int(res.text)/20)
	print(pages)

	skip=0

	for page in range(pages):
		# res = requests.get(data['sapurl']+"/ItemGroups?$select=Number,GroupName&$orderby=Number&$skip="+str(skip), headers={'Authorization': "Bearer "+data['SessionId']+""}, verify=False)
		res = requests.get(settings.SAPURL+'/ItemGroups?$select=Number,GroupName&$orderby=Number&$skip='+str(skip), cookies=ses.cookies, verify=False)
		cats = json.loads(res.text)

		for cat in cats['value']:
			print('-----Category---')
			print(cat['Number'])
			GroupName = cat['GroupName'].replace("'", "''")
			print(GroupName)
			mycursor.execute("select * from Item_category where Number='"+str(cat['Number'])+"'")
			mycursor.fetchall()
			rc = mycursor.rowcount
			print(rc)
			if rc != 1:
				cat_sql = f"INSERT INTO `Item_category`(`CategoryName`, `Status`, `CreatedDate`, `CreatedTime`, `UpdatedDate`, `UpdatedTime`, `Number`) VALUES ('{GroupName}', 1, '','','','', '{cat['Number']}')"
				print(cat_sql)
				mycursor.execute(cat_sql)
				mydb.commit()
				catid = mycursor.lastrowid
				print(catid)
			else:
				cat_sql = f"UPDATE `Item_category` SET `CategoryName`='{GroupName}' WHERE `Number`={str(cat['Number'])}"
				print(cat_sql)
				mycursor.execute(cat_sql)
				mydb.commit()

		print('___')
		skip = skip+20
	settings.custome_error_logs('cron end', module_name='import-category')
except Exception as e:
    print(str(e))
    settings.custome_error_logs(message=str(e), module_name='import-category')