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
try:
	settings.custome_error_logs('cron start', module_name='sp')

	# currentDate = '2023-02-10'
	serSPCount = requests.get(settings.SAPURL+'/SalesPersons/$count', cookies=ses.cookies, verify=False).text

	# count the number if loop run, each one skip 20 values
	count = math.ceil(int(serSPCount)/20)
	print(count)

	employeearr = []
	skip=0
	for t in range(count):

		res = requests.get(settings.SAPURL+'/SalesPersons?$skip='+str(skip), cookies=ses.cookies, verify=False)

		sps = json.loads(res.text)
		for sp in sps['value']:
			
			print('-----SalePersons---')
			EmployeeID = ""
			SalesEmpCode = sp['SalesEmployeeCode']
			employeearr.append(SalesEmpCode)
			print("SalesEmpCode", SalesEmpCode)

			companyID = ""
			SalesEmployeeCode = sp['SalesEmployeeCode']
			# if str(SalesEmployeeCode) == '-1':
			# 	continue

			SalesEmployeeName = sp['SalesEmployeeName']
			EmployeeID = sp['EmployeeID']
			userName = sp['SalesEmployeeName']
			password = "123"
			firstName = sp['SalesEmployeeName']
			middleName = ""
			lastName = ""
			Email = sp['Email']
			Mobile = sp['Mobile']
			role = ""
			position = ""
			branch = ""
			Active = sp['Active']
			passwordUpdatedOn = ""
			lastLoginOn = ""
			logedIn = ""
			reportingTo = -1
			FCM = ""
			timestamp = ""
			unit = ""
			ACCNo = ""
			Address = ""
			CompName = ""
			GST = ""
			Ifsc = ""
			U_LAT = ""
			U_LONG = ""
			Website = ""
			LocationSharing = ""
			Zone = ""
			sqlSelect = f"SELECT `id` FROM Employee_employee WHERE SalesEmployeeCode = {SalesEmpCode}"
			print(sqlSelect)
			mycursor.execute(sqlSelect)
			empObj = mycursor.fetchall()
			if len(empObj) == 0:
							
				sp_sql = f"INSERT INTO `Employee_employee`(`companyID`, `SalesEmployeeCode`, `SalesEmployeeName`, `EmployeeID`, `userName`, `password`, `firstName`, `middleName`, `lastName`, `Email`, `Mobile`, `role`, `position`, `branch`, `Active`, `passwordUpdatedOn`, `lastLoginOn`, `logedIn`, `reportingTo`, `FCM`, `timestamp`, `unit`, `ACCNo`, `Address`, `CompName`, `GST`, `Ifsc`, `U_LAT`, `U_LONG`, `Website`, `LocationSharing`, `Zone`) VALUES ('{companyID}','{SalesEmployeeCode}','{SalesEmployeeName}','{EmployeeID}','{userName}','{password}','{firstName}','{middleName}','{lastName}','{Email}','{Mobile}','{role}','{position}','{branch}','{Active}','{passwordUpdatedOn}','{lastLoginOn}','{logedIn}','{reportingTo}','{FCM}','{timestamp}','{unit}','{ACCNo}','{Address}','{CompName}','{GST}','{Ifsc}','{U_LAT}','{U_LONG}','{Website}','{LocationSharing}','{Zone}');"
				print(sp_sql)
				mycursor.execute(sp_sql)
				mydb.commit()
				spid = mycursor.lastrowid
				print(spid)
			else:
				sp_sql = f"UPDATE `Employee_employee` SET `SalesEmployeeName`='{SalesEmployeeName}',`EmployeeID` = '{EmployeeID}',`userName`='{SalesEmployeeName}',`firstName`='{SalesEmployeeName}', `Email`='{Email}',`Mobile`='{Mobile}',`Active`='{Active}' WHERE SalesEmployeeCode = {SalesEmployeeCode}"
				print(sp_sql)
				mycursor.execute(sp_sql)
				mydb.commit()
				# spid = mycursor.lastrowid
				# print(spid)

		print('___')
		skip = skip+20
		print(skip)

	settings.custome_error_logs('cron end', module_name='sp')
except Exception as e:
	print(str(e))
	settings.custome_error_logs(message=str(e), module_name='sp')