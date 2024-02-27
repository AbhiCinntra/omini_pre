import requests, json
import time
import math
import mysql.connector
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
	settings.custome_error_logs('cron start', module_name='branch')

	sapData = requests.get(settings.SAPURL+'/BusinessPlaces/$count', cookies=ses.cookies, verify=False)

	print("sapData ",sapData.text)
	# count the number if loop run, each one skip 20 values
	count = math.ceil(int(sapData.text)/20)
	print(count)

	skip=0
	for i in range(count):

		res = requests.get(settings.SAPURL+'/BusinessPlaces?$skip='+str(skip), cookies=ses.cookies, verify=False)
		data = json.loads(res.text)
		# branches = data['value']
		for branche in data['value']:
			print('-----Branches---')

			BPLId = branche['BPLID']
			BPLName = str(branche['BPLName']).replace("'", "&apos;")
			Address = str(branche['Address']).replace("'", "&apos;")
			MainBPL = branche['MainBPL']
			Disabled = branche['Disabled']
			UserSign2 = ""
			UpdateDate = ""
			DflWhs = "" #branche['DflWhs']
			TaxIdNum = "" #branche['TaxIdNum']
			StreetNo = str(branche['StreetNo']).replace("'", "&apos;")
			Building = str(branche['Building'])
			ZipCode = str(branche['ZipCode'])
			City = str(branche['City']).replace("'", "&apos;")
			State = str(branche['State'])
			Country = str(branche['Country'])
			FederalTaxID = str(branche['FederalTaxID'])

			checkPaymentQuery = f"select * from Company_branch WHERE BPLId = '{BPLId}'"
			print(checkPaymentQuery)
			mycursor.execute(checkPaymentQuery)
			if mycursor.rowcount == 0:
				pay_sql = f"INSERT INTO `Company_branch`(`BPLId`, `BPLName`, `Address`, `MainBPL`, `Disabled`, `UserSign2`, `UpdateDate`, `DflWhs`, `TaxIdNum`, `StreetNo`, `Building`, `ZipCode`, `City`, `State`, `Country`, `Series`, `FederalTaxID`) VALUES ('{BPLId}','{BPLName}','{Address}','{MainBPL}','{Disabled}','{UserSign2}','{UpdateDate}','{DflWhs}','{TaxIdNum}','{StreetNo}','{Building}','{ZipCode}','{City}','{State}','{Country}', '', '{FederalTaxID}')"

				print(pay_sql)
				mycursor.execute(pay_sql)
				mydb.commit()
				indid = mycursor.lastrowid
				print(indid)
			# endif
		# endfor
		print('___')
		skip = skip+20
		print(skip)
	# endfor
	settings.custome_error_logs('cron end', module_name='branch')
except Exception as e:
    print("Exception: ", str(e))
    settings.custome_error_logs(message=str(e), module_name='branch')
