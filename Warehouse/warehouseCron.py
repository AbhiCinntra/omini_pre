import requests, json
import time
import math
import mysql.connector
import sys, os

# file_path = os.path.dirname(__file__)
file_path = str("/home/www/b2b/rg_industries_prod/bridge/")
# file_path = str("F:/python-projects/rg_industries_prod/bridge/Item/")
print(">>>>>>>>>>>>>>>>>>>>>>>>>")
print("file_path: ", file_path)
dir = file_path.split("bridge")[0]+"bridge"
sys.path.append(dir)
from bridge import settings
ses = ""
if __name__ == '__main__':
	ses = settings.SAPSESSIONNEW("core")
else:
	ses = settings.SAPSESSIONNEW("api")

mydb = mysql.connector.connect(
  host=settings.DATABASES['default']['HOST'],
  user=settings.DATABASES['default']['USER'],
  password=settings.DATABASES['default']['PASSWORD'],
  database=settings.DATABASES['default']['NAME']
)

mycursor = mydb.cursor()

sapData = requests.get(settings.SAPURL+'/Warehouses/$count', cookies=ses.cookies, verify=False)
print("sapData ", sapData.text)

# count the number if loop run, each one skip 20 values
count = math.ceil(int(sapData.text)/20)
print(count)
skip=0
for i in range(count):
  res = requests.get(settings.SAPURL+'/Warehouses?$skip='+str(skip), cookies=ses.cookies, verify=False)
  inds = json.loads(res.text)
    
  for ind in inds['value']:
    print('-----Warehouse-----')
    BusinessPlaceID = ind['BusinessPlaceID']
    Location = ind['Location']
    WarehouseCode = ind['WarehouseCode']
    WarehouseName = ind['WarehouseName']
    Block = ind['Block']
    State = ind['State']
    City = ind['City']
    Country = ind['Country']
    County = ind['County']
    Street = ind['Street']
    ZipCode = ind['ZipCode']
    Inactive = ind['Inactive']
    CreatedDate = ""
    UpdatedDate = ""

    mycursor.execute("select * from `Warehouse_warehouse` WHERE WarehouseCode='"+str(WarehouseCode)+"'")
    mycursor.fetchall()
    rc = mycursor.rowcount
    if rc != 1:
      war_sql = f"INSERT INTO `Warehouse_warehouse`(`BusinessPlaceID`, `Location`, `WarehouseCode`, `WarehouseName`, `Block`, `State`, `City`, `Country`, `County`, `Street`, `ZipCode`, `Inactive`, `CreatedDate`, `UpdatedDate`) VALUES ('{BusinessPlaceID}', '{Location}', '{WarehouseCode}', '{WarehouseName}', '{Block}', '{State}', '{City}', '{Country}', '{County}', '{Street}', '{ZipCode}', '{Inactive}', '{CreatedDate}', '{UpdatedDate}');"
      print(war_sql)
      mycursor.execute(war_sql)
      mydb.commit()
      
    else:
      war_sql = f"UPDATE `Warehouse_warehouse` SET `BusinessPlaceID` = '{BusinessPlaceID}',`Location` = '{Location}', `WarehouseName` = '{WarehouseName}', `Block` = '{Block}', `State` = '{State}', `City` = '{City}', `Country` = '{Country}', `County` = '{County}', `Street` = '{Street}', `ZipCode` = '{ZipCode}', `Inactive` = '{Inactive}' WHERE `WarehouseCode` = '{WarehouseCode}'"
      print(war_sql)
      mycursor.execute(war_sql)
      mydb.commit()
  skip = skip + 20