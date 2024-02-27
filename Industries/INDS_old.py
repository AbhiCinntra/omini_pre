import requests, json
import time
import math
import mysql.connector

import sys, os
# dir = os.getcwd()
# dir = dir.split("bridge")[0]+"bridge"
# sys.path.append(dir)
# from bridge import settings
# data = settings.SAPSESSION("core")

# file_path = os.path.dirname(__file__)
# file_path = str("F:/python-projects/shivtara_live/bridge/Item/")
file_path = str("/home/www/b2b/shivtara_live/bridge/Item/")
print(">>>>>>>>>>>>>>>>>>>>>>>>>")
print("file_path: ", file_path)
dir = file_path.split("bridge")[0]+"bridge"
print("file_dir: ", dir)
print(">>>>>>>>>>>>>>>>>>>>>>>>>")
sys.path.append(dir)
from bridge import settings
ses = ""
if __name__ == '__main__':
	ses = settings.SAPSESSIONNEW("core")
	# print("in if")
else:
	ses = settings.SAPSESSIONNEW("api")
	# print("else")

mydb = mysql.connector.connect(
  host=settings.DATABASES['default']['HOST'],
  user=settings.DATABASES['default']['USER'],
  password=settings.DATABASES['default']['PASSWORD'],
  database=settings.DATABASES['default']['NAME']
)

mycursor = mydb.cursor()

# count = requests.get(data['sapurl']+'/Industries/$count', headers={'Authorization': "Bearer "+data['SessionId']+""}, verify=False).text
# res = requests.get(data['sapurl']+'/Industries', headers={"Prefer":"odata.maxpagesize="+str(count)+"", 'Authorization': "Bearer "+data['SessionId']+""}, verify=False)
# inds = json.loads(res.text)

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
    if rc != 1:
      ind_sql = f"INSERT INTO `Industries_industries` (`IndustryDescription`, `IndustryName`, `IndustryCode`) VALUES ('{IndustryDescription}','{IndustryName}','{IndustryCode}')"
      print(ind_sql)
      mycursor.execute(ind_sql)
      mydb.commit()
    else:
      ind_sql = f"UPDATE `Industries_industries` SET `IndustryDescription`='{IndustryDescription}',`IndustryName`='{IndustryName}' WHERE `IndustryCode` = {IndustryCode}"
      print(ind_sql)
      mycursor.execute(ind_sql)
      mydb.commit()
        
      # indid = mycursor.lastrowid
      # print(indid)
