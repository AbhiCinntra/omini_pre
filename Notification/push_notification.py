import requests, json
import time
import math
import mysql.connector

from pytz import timezone
from datetime import datetime as dt

# from global_fun import sendNotification
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
print("test comment")

from pyfcm import FCMNotification

def sendNotification(DeviceId, Title, Message):
    try:
        #push_service = FCMNotification(api_key="AAAA-fxz6HA:APA91bHsTYgIkWxYTRH6AwuNlx4-0H3y4yyQBYlB7S3tIXZ8-Cr0hudz3SQjAgjyU8w2t8p1mTB5D0t5OsU7jbwLKZTqRzrE9pcXtl0Gb8aIOqlCOLYHVfvLnk01RG1ZOchU8fJ3nVff") # standalone
        push_service = FCMNotification(api_key="AAAAadlvIDU:APA91bGC0hY3zWK6NmIbR_m9Nyx9FmA7k_lrt4E0nPm9y576M91qU1UWk9V4J09DQYExgyF_DnXEAf7-P6FyHze1JKbsTOnwqAoV5QUUM0J9M7sa9rB6y-ObuGKCcM0iABWz3rpd4sdq") # standalone
        print("push_service")
        print(push_service)
        
        #registration_id = "AAAAadlvIDU:APA91bGC0hY3zWK6NmIbR_m9Nyx9FmA7k_lrt4E0nPm9y576M91qU1UWk9V4J09DQYExgyF_DnXEAf7-P6FyHze1JKbsTOnwqAoV5QUUM0J9M7sa9rB6y-ObuGKCcM0iABWz3rpd4sdq"
        registration_id = DeviceId
        # message_title = "Test Notification"
        # message_body = "Hi Abhishek, your customized news for today is ready"
        message_title = Title
        message_body = Message
        print(f'title:{ message_title}, body {message_body}')
        print("registration_id")
        print(registration_id)

        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body, content_available=True)

        # To support rich notifications on iOS 10, set
        extra_kwargs = {
            'mutable_content': True
        }

        print(result)
        return "sent"
    except Exception as e:
        return str(e)

notification_list_sql = "SELECT * FROM `Notification_notification` WHERE `Push` = '0' and `CreatedDate` = '"+date+"' AND STR_TO_DATE(`SourceTime`, '%h:%i') >= STR_TO_DATE('"+time+"', '%h:%i') AND STR_TO_DATE(`SourceTime`, '%h:%i') <= ADDTIME(STR_TO_DATE('"+time+"', '%h:%i'), '0:10:00')"
print(notification_list_sql)
mycursor.execute(notification_list_sql)
notification_list = mycursor.fetchall()
print(len(notification_list))
if len(notification_list) > 0:
    for noti in notification_list:

        Id = noti['id']
        Title = noti['Title']
        Description = noti['Description']
        EmpId = noti['Emp']

        sql_query = "SELECT `FCM` FROM `Employee_employee` WHERE `id` = '"+EmpId+"'"
        mycursor.execute(sql_query)
        emp_ob = mycursor.fetchone() # to get only one row from list
        fcmId = emp_ob['FCM']
        
        result = sendNotification(DeviceId=fcmId, Title=Title, Message=Description)
        print(result)
        mycursor.execute("Update Notification_notification SET `Push`='1' where id='"+str(Id)+"'")
        mydb.commit()
