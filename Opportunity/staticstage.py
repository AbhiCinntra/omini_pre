import requests, json
import time

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Sunil@123",
  database="development"
)
mycursor = mydb.cursor()
mycursor = mydb.cursor(dictionary=True)
#print("test comment")

with open("../bridge/db.json") as f:
    db = f.read()
    print(db)
data = json.loads(db)

r = requests.post('http://103.107.67.94:50001/b1s/v1/Login', data=json.dumps(data), verify=False)
token = json.loads(r.text)['SessionId']
print(token)

#res = requests.get('http://103.107.67.94:50001/b1s/v1/SalesStages/', cookies=r.cookies, verify=False)
res = requests.get('http://103.107.67.94:50001/b1s/v1/SalesStages?$apply=aggregate(SequenceNo with max as max_live)', cookies=r.cookies, verify=False)

#print(res.text)
live = json.loads(res.text)
#print(live['value'][0]['max_live'])
max_live = live['value'][0]['max_live']

mycursor.execute("SELECT max(`SequenceNo`) as max_local FROM `Opportunity_staticstage`")
fetch = mycursor.fetchone()
#print(fetch['max_local'])
max_local = fetch['max_local']

if str(max_local)=="None":
	print("Blank")
	res = requests.get('http://103.107.67.94:50001/b1s/v1/SalesStages?$orderby=SequenceNo', cookies=r.cookies, verify=False)

	stages = json.loads(res.text)
	#print(stages)
	
	for stage in stages['value']:
		#print(stage['SequenceNo'])
		
		stage_sql = "INSERT INTO `Opportunity_staticstage` (`id`, `SequenceNo`, `Name`, `Stageno`, `ClosingPercentage`, `Cancelled`, `IsSales`, `IsPurchasing`) VALUES (NULL, '"+str(stage['SequenceNo'])+"', '"+str(stage['Name'])+"', '"+str(stage['Stageno'])+"', '"+str(stage['ClosingPercentage'])+"', '"+str(stage['Cancelled'])+"', '"+str(stage['IsSales'])+"', '"+str(stage['IsPurchasing'])+"');"
		#print(stage_sql)
		mycursor.execute(stage_sql)
		mydb.commit()
		#print('___')
		
else:	
	if(int(max_local) < max_live):
		res = requests.get('http://103.107.67.94:50001/b1s/v1/SalesStages?$filter=SequenceNo gt '+max_local+' & $orderby=SequenceNo', cookies=r.cookies, verify=False)

		stages = json.loads(res.text)
		#print(stages)
		
		for stage in stages['value']:
			#print(stage['SequenceNo'])
			
			stage_sql = "INSERT INTO `Opportunity_staticstage` (`id`, `SequenceNo`, `Name`, `Stageno`, `ClosingPercentage`, `Cancelled`, `IsSales`, `IsPurchasing`) VALUES (NULL, '"+str(stage['SequenceNo'])+"', '"+str(stage['Name'])+"', '"+str(stage['Stageno'])+"', '"+str(stage['ClosingPercentage'])+"', '"+str(stage['Cancelled'])+"', '"+str(stage['IsSales'])+"', '"+str(stage['IsPurchasing'])+"');"
			#print(stage_sql)
			mycursor.execute(stage_sql)
			mydb.commit()
			#print('___')
			
