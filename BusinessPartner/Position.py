import requests, json
import time
import math
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Sunil@123",
  database="development"
)
mycursor = mydb.cursor()
print("test comment")

with open("../bridge/db.json") as f:
    db = f.read()
    print(db)
data = json.loads(db)

r = requests.post('http://103.107.67.94:50001/b1s/v1/Login', data=json.dumps(data), verify=False)
token = json.loads(r.text)['SessionId']
print(token)

res = requests.get('http://103.107.67.94:50001/b1s/v1/EmployeePosition', cookies=r.cookies, verify=False)

bps = json.loads(res.text)
print(len(bps['value']))
for bp in bps['value']:
    print('-----Position---')
    print(bp['PositionID'])
    print(bp['Name'])
    print(bp['Description'])
    
    pos_sql = "INSERT INTO `BusinessPartner_bpposition` (`PositionID`, `Name`, `Description`) VALUES ('"+str(bp['PositionID'])+"', '"+str(bp['Name'])+"', '"+str(bp['Description'])+"');"

    mycursor.execute(pos_sql)
    mydb.commit()
    #print(mycursor.last_inserted_id())
