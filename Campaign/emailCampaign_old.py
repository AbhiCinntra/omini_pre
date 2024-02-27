from ctypes import sizeof
from datetime import date, datetime
import calendar
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import os
import smtplib
import requests, json
import time
import math
import mysql.connector

from urllib.parse import urlparse

currentDate = date.today()
currentDay = calendar.day_name[currentDate.weekday()]  # this will return the day of a week
currentTime = datetime.today().strftime("%I:%M %p")

import sys
sys.path.append('/home/www/b2b/standalone_pre/bridge/')
# sys.path.append('../../bridge')
from global_fun import sendMail

print("Today date is: ", currentDate)
print("Today day is: ", currentDay)
print("Today Current time: ", currentTime)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="$Bridge@2022#",
#   password="root",
  database="standalone_pre"
)

mycursor = mydb.cursor()

# -------------------
# Email Campaign Body  
# -------------------
def sendCampaignToMember(subject, Message, members, Attachments, campId):
    for member in members:
        email = member['Email']
        if email !="":
            # print('in mail functions')
            # print(email, subject, Message)
            res = sendMail(email, subject, Message, Attachments)
            print(res)
    
            if Frequency == 'Once':
                # update send status 1 in campaign
                sqlUpdateCampaign = "UPDATE `Campaign_campaign` SET `Sent` = 1 WHERE `id` = "+ str(campId)
                mycursor.execute(sqlUpdateCampaign)
                mydb.commit()

userList = []

# sqlSelectCamSet = "SELECT * FROM `Campaign_campaignset` WHERE `id` = 38"
sqlSelectCamSet = "SELECT * FROM `Campaign_campaignset` WHERE Status = 1"
mycursor.execute(sqlSelectCamSet)
allRow = mycursor.fetchall()
for campaign in allRow:
    camSetId = campaign[0]
    print(camSetId)

    # -----------------------
    # campain set member list
    # -----------------------
    allMembersArr = []
    sqlSelectMember = "SELECT * FROM `Campaign_campaignsetmembers` WHERE `CampSetId_id` = "+ str(camSetId)
    mycursor.execute(sqlSelectMember)
    allMembers = mycursor.fetchall()
    if len(allMembers) != 0:
        for member in allMembers:
            userData = {
                'Name': member[1],
                'Phone': member[2],
                'Email': member[3]
            }
            allMembersArr.append(userData)


    # -----------------------
    # --- campain list ------
    # -----------------------
    mailSubject = ""
    mailbody = ""

    print('---Campaign---')
    sqlSelectCam = "SELECT * FROM `Campaign_campaign` WHERE `RunTime` = '"+str(currentTime)+"' AND `Status` = 1 AND `Sent` = 0 AND `Type` = 'Email' AND `StartDate` <= '"+str(currentDate)+"' AND `EndDate` >= '"+str(currentDate)+"' AND `CampaignSetId_id` = "+ str(camSetId)
    # sqlSelectCam = "SELECT * FROM `Campaign_campaign` WHERE `Status` = 1 AND `Sent` = 0 AND `Type` = 'Email' AND `StartDate` <= '"+str(currentDate)+"' AND `EndDate` >= '"+str(currentDate)+"' AND `CampaignSetId_id` = "+ str(camSetId)
    print(sqlSelectCam)
    mycursor.execute(sqlSelectCam)
    allCampaign = mycursor.fetchall()
    if len(allCampaign) != 0:
        for campaign in allCampaign:
            # print(campaign)
            camp_id = campaign[0]
            
            Frequency = campaign[5]
            mailbody = campaign[6]
            MonthlyDate = campaign[17]
            WeekDay = campaign[18]
            mailSubject = campaign[19]
            RunTime = campaign[20]
            Attachments = campaign[21]

            if Frequency == 'Daily':
                if RunTime == currentTime:
                    sendCampaignToMember(mailSubject, mailbody, allMembersArr, Attachments, camp_id)

            elif Frequency == 'Weekly':
                days = WeekDay.split(",")
                if currentDay in days:
                    sendCampaignToMember(mailSubject, mailbody, allMembersArr, Attachments, camp_id)

            elif Frequency == 'Monthly':
                dates = MonthlyDate.split(",")
                if currentDate in dates:
                    sendCampaignToMember(mailSubject, mailbody, allMembersArr, Attachments, camp_id)

            elif Frequency == 'Once':
                sendCampaignToMember(mailSubject, mailbody, allMembersArr, Attachments, camp_id)

