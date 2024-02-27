from ctypes import sizeof
from datetime import date, datetime
import calendar
import time
import mysql.connector

import sys
sys.path.append('/home/www/b2b/rg_industries_prod/bridge/')
# sys.path.append('../../bridge')
from global_fun import sendWhatsAppMsg

currentDate = date.today()
currentDay = calendar.day_name[currentDate.weekday()]  # this will return the day of a week
currentTime = datetime.today().strftime("%I:%M %p")

print("Today date is: ", currentDate)
print("Today day is: ", currentDay)
print("Today Current time: ", currentTime)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
#   password="root",
  password="$Bridge@2022#",
  database="rg_industries_prod"
)

mycursor = mydb.cursor()


# -------------------
# Email Campaign Body  
# -------------------
def sendCampaignToMember(subject, Message, members, Attachments, campId):
    for member in members:
        Name = member['Name']
        Phone = member['Phone']
        if Phone !="":
            # print('in mail functions')
            # res = sendWhatsAppMsg(Phone, urllib.parse.quote(Message))
            # whatsappMessage = f"Greetings of the Day! %0A%0ARespected Sir/Mam *{Name.strip().replace('&', '%26')}* %0A%0A{Message.strip()} %0A%0ARegards %0ABlair Remedies"
            whatsappMessage = f"Greetings of the Day! %0A%0ARespected Sir/Mam *{Name.strip().replace('&', '%26')}* %0A%0A{Message.strip().replace('#', '%23')} %0A%0ARegards %0ABlair Remedies"
            
            res = sendWhatsAppMsg(number = Phone, msg = whatsappMessage, Attachments = Attachments)
            print(res)
    
            if Frequency == 'Once':
                # update send status 1 in campaign
                sqlUpdateCampaign = "UPDATE `Campaign_campaign` SET `Sent` = 1 WHERE `id` = "+ str(campId)
                mycursor.execute(sqlUpdateCampaign)
                mydb.commit()

        time.sleep(5)

# -------------------
# Email Function
# -------------------
# def sendMail(toEmail, subject, message):
#     try:
#         # ServerHost = "smtp.zoho.in"
#         # ServerPort = 465          
#         # Sender = 'info@haks.co.in'
#         # Password = "Way2success120."

#         ServerHost = "smtp.gmail.com"
#         ServerPort = 465  # For starttls
#         Sender = "abhishek.kaithwas@cinntra.com"
#         Password = "TechAbhi@123!"

#         # Create message
#         msg = MIMEText(message, "HTML")
#         msg['Subject'] = subject
#         msg['From'] = Sender
#         msg['To'] = toEmail

#         # Create server object with SSL option
#         server = smtplib.SMTP_SSL(ServerHost, ServerPort)

#         # Perform operations via server
#         server.login(Sender, Password)
#         server.sendmail(Sender, [toEmail], msg.as_string())
#         server.quit()

#         return 'sent'
#     except Exception as e:
#         print(str(e))
#         return str(e)


# def sendText(number, msg):

#     insetanceId = "621f17f4cd00c56ad254fd4f"
#     url = f"https://wasmsapi.com/api/sendText?token={insetanceId}&phone=+91{number}&message={msg}"
#     print(url)
#     loginResponse = requests.post(url, verify=False, timeout=10)
#     return json.loads(loginResponse.text)

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
    sqlSelectCam = "SELECT `id`, `CampaignName`, `StartDate`, `EndDate`, `Type`, `Frequency`, `WeekDay`, `MonthlyDate`, `Message`, `Subject`, `RunTime`, `Attachments` FROM `Campaign_campaign` WHERE `RunTime` = '"+str(currentTime)+"' AND `Status` = 1 AND `Sent` = 0 AND `Type` = 'WhatsApp' AND `StartDate` <= '"+str(currentDate)+"' AND `EndDate` >= '"+str(currentDate)+"' AND `CampaignSetId_id` = "+ str(camSetId)
    print(sqlSelectCam)
    mycursor.execute(sqlSelectCam)
    allCampaign = mycursor.fetchall()
    if len(allCampaign) != 0:
        for campaign in allCampaign:
            # print(campaign)
            camp_id = campaign[0]
            
            Frequency = campaign[5]
            mailbody = campaign[8]
            WeekDay = campaign[6]
            MonthlyDate = campaign[7]
            mailSubject = campaign[9]
            RunTime = campaign[10]
            Attachments = campaign[11]

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

