import requests, json
import time
import math
import mysql.connector
import sys, os

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

# count = requests.get(data['sapurl']+'/PaymentTermsTypes/$count', headers={'Authorization': "Bearer "+data['SessionId']+""}, verify=False).text
# res = requests.get(data['sapurl']+'/PaymentTermsTypes', headers={"Prefer":"odata.maxpagesize="+str(count)+"", 'Authorization': "Bearer "+data['SessionId']+""}, verify=False)
# inds = json.loads(res.text)

sapData = requests.get(settings.SAPURL+'/PaymentTermsTypes/$count', cookies=ses.cookies, verify=False)
print("sapData ", sapData.text)

# count the number if loop run, each one skip 20 values
count = math.ceil(int(sapData.text)/20)
print(count)
skip=0
for i in range(count):
  res = requests.get(settings.SAPURL+'/PaymentTermsTypes?$skip='+str(skip), cookies=ses.cookies, verify=False)
  inds = json.loads(res.text)
    
  for ind in inds['value']:
    print('-----Payment-----')
    GroupNumber = ind['GroupNumber']
    PaymentTermsGroupName = ind['PaymentTermsGroupName']

    mycursor.execute("select * from `PaymentTermsTypes_paymenttermstypes` WHERE GroupNumber='"+str(GroupNumber)+"'")
    mycursor.fetchall()
    rc = mycursor.rowcount
    if rc != 1:
      pay_sql = f"INSERT INTO `PaymentTermsTypes_paymenttermstypes` (`GroupNumber`, `PaymentTermsGroupName`) VALUES ('{GroupNumber}','{PaymentTermsGroupName}');"
      print(pay_sql)
      mycursor.execute(pay_sql)
      mydb.commit()

    else:
      ind_sql = f"UPDATE `PaymentTermsTypes_paymenttermstypes` SET `PaymentTermsGroupName`='{PaymentTermsGroupName}' WHERE `GroupNumber` = {GroupNumber}"
      print(ind_sql)
      mycursor.execute(ind_sql)
      mydb.commit()