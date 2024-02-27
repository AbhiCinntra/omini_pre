import requests, json
import time
import math
import mysql.connector

def none(inp):
	if type(inp)!=int:
		return 0;
	else:
		return inp

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

#rr = requests.get('http://103.107.67.94:50001/b1s/v1/BusinessPartners/$count', cookies=r.cookies, verify=False)
res = requests.get('http://103.107.67.94:50001/b1s/v1/States/$count', cookies=r.cookies, verify=False)
print(res.text)


count = math.ceil(int(res.text)/20)
print(count)

skip=0
for i in range(count):
    res = requests.get('http://103.107.67.94:50001/b1s/v1/States?$orderby=Code&$skip='+str(skip)+'', cookies=r.cookies, verify=False)
    opts = json.loads(res.text)
    print(len(opts['value']))

    for opt in opts['value']:
        print(opt['Code'])
        opp_sql = "INSERT INTO `Countries_states` (`Code`, `Country`, `Name`) VALUES ('"+str(opt['Code'])+"', '"+str(opt['Country'])+"', '"+str(opt['Name'])+"');"
        mycursor.execute(opp_sql)
        mydb.commit()

    print('___')
    skip = skip+20


#opts = json.loads(res.text)
#print(len(opts['value']))

