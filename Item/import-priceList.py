import requests, json
import time
import math
import mysql.connector

import sys, os
# dir = os.getcwd()
# dir = dir.split("bridge")[0]+"bridge"
# sys.path.append(dir)
# from bridge import settings
# # data = settings.SAPSESSIONNEW("core")
# data = settings.SAPSESSION("core")
# print("SAPSESSION", data)


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
# mycursor = mydb.cursor()
mycursor = mydb.cursor(dictionary=True, buffered=True)

# res = requests.get(data['sapurl']+'/PriceLists/$count', headers={'Authorization': "Bearer "+data['SessionId']+""}, verify=False)
res = requests.get(settings.SAPURL+'/PriceLists/$count', cookies=ses.cookies, verify=False)
print(res.text)

pages = math.ceil(int(res.text)/20)
print(pages)

skip=0

for page in range(pages):
  # res = requests.get(data['sapurl']+"/PriceLists?$skip="+str(skip), headers={'Authorization': "Bearer "+data['SessionId']+""}, verify=False)
  res = requests.get(settings.SAPURL+'/PriceLists?$skip='+str(skip), cookies=ses.cookies, verify=False)
  cats = json.loads(res.text)

  for cat in cats['value']:
    # print('-----Category---')
    mycursor.execute("SELECT * FROM `Item_pricelist` WHERE PriceListNo='"+str(cat['PriceListNo'])+"'")
    mycursor.fetchall()
    rc = mycursor.rowcount
    # print(rc)
    
    PriceListNo = cat['PriceListNo']
    PriceListName = cat['PriceListName']
    DefaultPrimeCurrency = cat['DefaultPrimeCurrency']
    FixedAmount = cat['FixedAmount']
    if rc != 1:

      cat_sql = f"INSERT INTO `Item_pricelist`(`PriceListNo`, `PriceListName`, `Currency`, `FixedAmount`, `Active`) VALUES ('{PriceListNo}','{PriceListName}','{DefaultPrimeCurrency}','{FixedAmount}', 'tYES');"
      print(cat_sql)
      mycursor.execute(cat_sql)
      mydb.commit()
    else:
      cat_sql = f'UPDATE `Item_pricelist` SET `PriceListName`="{PriceListName}", `Currency`="{DefaultPrimeCurrency}", `FixedAmount`="{FixedAmount}" WHERE `PriceListNo` = {PriceListNo}'
      print(cat_sql)
      mycursor.execute(cat_sql)
      mydb.commit()

  print('___')
  skip = skip+20
