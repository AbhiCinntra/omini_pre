import requests, json
import time
import math
import mysql.connector

import sys, os

# file_path = os.path.dirname(__file__)
# file_path = str("F:/python-projects/shivtara_live/bridge/Item/")
file_path = str("/home/www/b2b/rg_industries_prod/bridge/Item/")
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

mycursor = mydb.cursor(dictionary=True, buffered=True)

# res = requests.get(data['sapurl']+'/UnitOfMeasurements/$count', headers={'Authorization': "Bearer "+data['SessionId']+""}, verify=False)
res = requests.get(settings.SAPURL+'/UnitOfMeasurements/$count', cookies=ses.cookies, verify=False)
print(res.text)

pages = math.ceil(int(res.text)/20)
print(pages)

skip=0

for page in range(pages):
    # res = requests.get(data['sapurl']+"/UnitOfMeasurements?$skip="+str(skip), headers={'Authorization': "Bearer "+data['SessionId']+""}, verify=False)
    res = requests.get(settings.SAPURL+'/UnitOfMeasurements?$skip='+str(skip), cookies=ses.cookies, verify=False)

    uoms = json.loads(res.text)

    for uom in uoms['value']:
        AbsEntry = uom['AbsEntry']
        Code = uom['Code']
        Name = uom['Name']
        VolumeUnit = uom['VolumeUnit']
        Weight1 = uom['Weight1']
        Weight1Unit = uom['Weight1Unit']
        
        selectQuery = f'select * from `Item_uomlist` where `AbsEntry` = "{AbsEntry}"'
        print(selectQuery)
        mycursor.execute(selectQuery)
        mycursor.fetchall()
        rc = mycursor.rowcount
        print(rc)
        if rc != 1:
          cat_sql = f'INSERT INTO `Item_uomlist`(`AbsEntry`, `Code`, `Name`, `VolumeUnit`, `Weight1`, `Weight1Unit`) VALUES ("{AbsEntry}", "{Code}", "{Name}", "{VolumeUnit}", "{Weight1}", "{Weight1Unit}")'
          print(cat_sql)
          mycursor.execute(cat_sql)
          mydb.commit()
        else:
          cat_sql = f'UPDATE `Item_uomlist` SET `Name`="{Name}", `VolumeUnit`="{VolumeUnit}", `Weight1`="{Weight1}",`Weight1Unit`="{Weight1Unit}" WHERE `AbsEntry` = {AbsEntry}'
          print(cat_sql)
          mycursor.execute(cat_sql)
          mydb.commit()
            

    print('___')
    skip = skip+20
