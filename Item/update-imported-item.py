import requests, json
import time
import math
import mysql.connector
from datetime import date, datetime as dt, timedelta
currentDate = date.today()

import sys, os
# dir = os.getcwd()
# dir = dir.split("bridge")[0]+"bridge"
# sys.path.append(dir)
# from bridge import settings
# data = settings.SAPSESSION("core")

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

# res = requests.get(data['sapurl']+'/Items/$count', headers={'Authorization': "Bearer "+data['SessionId']+""}, verify=False)
res = requests.get(settings.SAPURL+'/Items/$count', cookies=ses.cookies, verify=False)
print(res.text)

pages = math.ceil(int(res.text)/20)
print(pages)

skip=0

for page in range(pages):

    # res = requests.get(data['sapurl']+'/Items?$skip='+str(skip)+'', cookies=r.cookies, verify=False)
    res = requests.get(settings.SAPURL+'/Items?$skip='+str(skip), cookies=ses.cookies, verify=False)
    items = json.loads(res.text)
    for item in items['value']:
        print('-----Update Item---')
        print(item['ItemName'])
        ItemName = item['ItemName'].replace("'", "''")
        price = str(0)
        
        # item price list by price list category
        ItemPricesList = item['ItemPrices']

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        ActiveStatus = "tYES"
        Frozen = item['Frozen']
        if str(Frozen) == 'tYES': # Frozen tYes means item in-active
            ActiveStatus = "tNO"
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        
        itemSelectQuery = f"select ItemCode from Item_item where ItemCode='{item['ItemCode']}'"
        print(itemSelectQuery)
        mycursor.execute(itemSelectQuery)
        mycursor.fetchall()
        rc = mycursor.rowcount
        print("localItemCount", rc)
        if rc >= 1:
            CodeType = "Manual"
            ItemName = item['ItemName']
            ItemCode = item['ItemCode']
            Inventory = item['QuantityOnStock']
            Description = item['ItemName']
            UnitPrice = 0
            Currency = "INR"
            HSN = ""
            TaxCode = ''
            Discount = "0"
            Status = ActiveStatus
            CreatedDate = item['CreateDate']
            CreatedTime = item['CreateTime']
            UpdatedDate = item['UpdateDate']
            UpdatedTime = item['UpdateTime']
            UnitWeight = item['SalesUnitWeight']
            SalesItemsPerUnit = item['SalesItemsPerUnit']
            CatID_id = 0
            UoS = item['SalesUnit']
            Packing = ""
            ItemsGroupCode = item['ItemsGroupCode']
            U_GST = item['U_GST']
            GSTTaxCategory = item['GSTTaxCategory']
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            
            selectCategory = f"SELECT `id`, `Number`, `CategoryName` FROM `Item_category` WHERE `Number` = '{ItemsGroupCode}'"
            mycursor.execute(selectCategory)
            catRow = mycursor.fetchall()
            rc = mycursor.rowcount
            if int(rc) != 0:
                print(catRow)
                CatID_id = catRow[0]['id']
            
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            ItemUnitOfMeasurementCollection = item['ItemUnitOfMeasurementCollection']
            UoMIds = []
            for uom in ItemUnitOfMeasurementCollection:
                if uom["UoMType"] == "iutPurchasing":
                    UoMIds.append(uom['UoMEntry'])
            print("UoMIds: ", UoMIds)
            # UoMIds = ",".join(UoMIds)
            UoMIds = ",".join(str(id) for id in UoMIds)
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            item_sql = f'UPDATE `Item_item` SET `ItemName`="{ItemName}",`Inventory`="{Inventory}", `Status`="{Status}", `CreatedDate` = "{CreatedDate}", `CreatedTime`="{CreatedTime}", `UpdatedDate`="{UpdatedDate}",`UpdatedTime`="{UpdatedTime}",`UoS`="{UoS}", `U_GST`="{U_GST}", `UnitWeight`="{UnitWeight}", `GSTTaxCategory` = "{GSTTaxCategory}", `SalesItemsPerUnit` = "{SalesItemsPerUnit}", `UoMIds` = "{UoMIds}" WHERE `ItemCode` = "{ItemCode}"'
            print(item_sql)
            mycursor.execute(item_sql)
            mydb.commit()
            
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # ItemPriceList
            print("Insert Item Price List")
            for prices in ItemPricesList:
                lv_PriceList = prices['PriceList']
                lv_Currency = prices['Currency']
                lv_Price = prices['Price']
                # item_pricelist_sql = f'INSERT INTO `Item_itempricelist`(`ItemCode`, `PriceList`, `Currency`, `Price`) VALUES ("{ItemCode}", "{lv_PriceList}", "{lv_Currency}", "{lv_Price}")'     
                item_pricelist_sql = f'UPDATE `Item_itempricelist` SET `Currency`="{lv_Currency}",`Price`="{lv_Price}" WHERE `ItemCode` = "{ItemCode}" AND `PriceList` = "{lv_PriceList}"'    
                print(item_pricelist_sql)
                mycursor.execute(item_pricelist_sql)
                mydb.commit()

        #itemid = mycursor.lastrowid
    print('___')
    skip = skip+20
