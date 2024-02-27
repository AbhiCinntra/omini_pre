import requests, json
import time
import math
import mysql.connector

#notification.py

from pytz import timezone
from datetime import datetime as dt
date = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d')
time = dt.now(timezone("Asia/Kolkata")).strftime("%I:%M %p")
print(date)
print(time)

#import sys
#sys.path.append("../Mylib/")
#import config
#config = config.Config()

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
#  password=config.sql['password'],
#  database=config.sql['database']
  password="$Bridge@2022#",
  database="standalone_pre"
)

mycursor = mydb.cursor(dictionary=True)

print("SELECT `id`, `SourceID`, `Subject`, `Comment`, `Name`, `RelatedTo`, `Emp`, `Title`, `Description`, `From`, `To`, `Time`, `Allday`, `Location`, `Host`, `Participants`, `Document`, `Repeated`, `Priority`, `ProgressStatus`, `Type`, `SourceType`, `Status`, `CreateDate`, `CreateTime`, `leadType` FROM `Activity_activity` WHERE `From` = '"+date+"' AND STR_TO_DATE(`Time`, '%h:%i') >= STR_TO_DATE('"+time+"', '%h:%i') AND STR_TO_DATE(`Time`, '%h:%i') <= ADDTIME(STR_TO_DATE('"+time+"', '%h:%i'), '0:10:00')")

# mycursor.execute("SELECT * FROM `Activity_activity` WHERE `From` <= '"+date+"' and `To` >= '"+date+"'")
mycursor.execute("SELECT * FROM `Activity_activity` WHERE `From` = '"+date+"' AND STR_TO_DATE(`Time`, '%h:%i') >= STR_TO_DATE('"+time+"', '%h:%i') AND STR_TO_DATE(`Time`, '%h:%i') <= ADDTIME(STR_TO_DATE('"+time+"', '%h:%i'), '0:10:00')")
obj = mycursor.fetchall()
rrc = mycursor.rowcount
print(rrc)
if rrc != 0:
  for rc in obj:
    chk_sql = 'SELECT * FROM `Notification_notification` WHERE SourceID="'+str(rc['id'])+'" and Emp="'+str(rc['Emp'])+'" and CreatedDate="'+str(date)+'" and SourceTime ="'+str(rc['Time'])+'"' 
    print(chk_sql)
    mycursor.execute(chk_sql)
    chk_obj = mycursor.fetchall()
    print(len(chk_obj))
    if len(chk_obj) == 0:
    
      notiTitle = ""
      notiDesc = ""
      if rc['SourceID'] == 0:
        notiTitle = rc['Title']
        notiDesc = rc['Description']
      else:
        notiTitle = rc['Subject']
        notiDesc = rc['Comment']

      sql = "INSERT INTO `Notification_notification` (`Title`, `Description`, `SourceID`, `Emp`, `SourceTime`, `Type`, `SourceType`, `CreatedDate`, `CreatedTime`, `Read`, `Push`) VALUES ('"+str(notiTitle)+"', '"+str(notiDesc)+"', '"+str(rc['id'])+"', '"+str(rc['Emp'])+"', '"+str(rc['Time'])+"', '"+str(rc['Type'])+"', 'Activity', '"+date+"', '"+time+"', '0', '0');"
      print(sql)
      mycursor.execute(sql)
      mydb.commit()



# SELECT `From`,`To`,`Time`, TIMEDIFF(STR_TO_DATE(`Time`, '%h:%i'), STR_TO_DATE('12:45 AM', '%h:%i')) as ttime FROM `Activity_activity` WHERE `From` = '2022-05-11'


# SELECT `From`,`To`,`Time`, TIMEDIFF(STR_TO_DATE(`Time`, '%h:%i'), STR_TO_DATE('12:45 AM', '%h:%i')) as ttime FROM `Activity_activity` WHERE `From` = '2022-05-11' AND STR_TO_DATE(`Time`, '%h:%i') >= STR_TO_DATE('02:35 pm', '%h:%i') AND STR_TO_DATE(`Time`, '%h:%i') <= ADDTIME(STR_TO_DATE('02:35 pm', '%h:%i'), '0:05:00')