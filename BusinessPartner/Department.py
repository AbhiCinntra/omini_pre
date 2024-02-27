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

res = requests.get('http://103.107.67.94:50001/b1s/v1/Departments', cookies=r.cookies, verify=False)

bps = json.loads(res.text)
print(len(bps['value']))
for bp in bps['value']:
    print('-----Position---')
    print(bp['Code'])
    print(bp['Name'])
    print(bp['Description'])
    
    dep_sql = "INSERT INTO `BusinessPartner_bpdepartment` (`Code`, `Name`, `Description`) VALUES ('"+str(bp['Code'])+"', '"+str(bp['Name'])+"', '"+str(bp['Description'])+"');"

    mycursor.execute(dep_sql)
    mydb.commit()
    #print(mycursor.last_inserted_id())
