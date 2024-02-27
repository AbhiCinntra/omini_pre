# */2 * * * * /usr/bin/python3 /home/www/b2b/vision_sales_support_pre/bridge/Invoice/INV.py
# */2 * * * * /usr/bin/python3 /home/www/b2b/vision_sales_support_dev/bridge/Invoice/INV.py
# comment----###
import requests, json
import time
import math
import mysql.connector

from datetime import datetime
from datetime import date, datetime, timedelta
import calendar

import sys, os

import urllib.parse

currentDate = date.today()
currentDay = calendar.day_name[currentDate.weekday()]  # this will return the day of a week
currentTime = datetime.today().strftime("%I:%M %p")
currentDateTime = f"{currentDate} {currentTime}"
serverDateTime = datetime.now()

# import sys, os
# dir = os.getcwd()
# dir = dir.split("bridge")[0]+"bridge"
# sys.path.append(dir)
# from bridge import settings
# data = settings.SAPSESSION("core")

# mydb = mysql.connector.connect(
#   host=settings.DATABASES['default']['HOST'],
#   user=settings.DATABASES['default']['USER'],
#   password=settings.DATABASES['default']['PASSWORD'],
#   database=settings.DATABASES['default']['NAME']
# )
# mycursor = mydb.cursor(dictionary=True, buffered=True)

mydb = mysql.connector.connect(
    host='localhost',
    database='omini_pre',
    user='root',
    # password='root',
    password='$Bridge@2022#'
)
mycursor = mydb.cursor(dictionary=True, buffered=True)

# print("<><><><><><><><><><><>><><><><><><")
# print("===== Login SAP ====")
# data = { "CompanyDB": "RG_Industries_Live_", "UserName": "manager", "Password": "RG@123456", "SessionId": "a8e91956-7c8c-11ee-8000-0a427ed74412", "at": "2023-11-06 15:40:06", "sapurl": "https://103.190.95.182:50000/b1s/v1" }
# r = requests.post(data['sapurl']+'/Login', data=json.dumps(data), verify=False)
# print(r)

CronUpdateCount = 0
mycursor.execute("SELECT * FROM `BusinessPartner_receivable` ORDER BY `id` desc LIMIT 1")
entryData = mycursor.fetchall()
if len(entryData) > 0:
    # lastDocEntry = entryData[0]['DocEntry']
    CronUpdateCount = int(entryData[0]['CronUpdateCount'])
    print("CronUpdateCount", CronUpdateCount)

skip=0
# for i in range(count):
# while skip != "":
if True:
    # sapAPIUrl = f"http://103.190.95.182:8000/Ledure/Report/Aging1.xsjs"
    sapAPIUrl = f"http://103.190.95.182:8080/api/customerAging/GetCinnApiUrl?cardType=C"
    print(sapAPIUrl)
    res = requests.get(sapAPIUrl, verify=False)
    # print(res.text)
    opts = json.loads(res.text)

    CronUpdateCount = CronUpdateCount + 1
    # print("Length of objects", len(opts))
    # for opt in opts['AGING']['0']:
    for opt in opts:

        CardCode        = str(opt['Customer Code'])
        CardName        = str(opt['Customer Name']).replace("'", "")
        SalesEmployeeCode = str(opt['SalesEmployee'])
        U_U_UTL_Zone    = 'India' #str(opt['U_U_UTL_Zone'])
        GroupCode       = str(opt['GroupCode'])
        GroupName       = str(opt['GroupName']).replace("'", "")
        DocEntry        = str(opt['DocEntry'])
        DocNum          = str(opt['Document_No'])
        TransId         = str(opt['TransId'])
        TransType       = str(opt['Document Type'])
        OB              = '' #str(opt['OB'])
        Debit           = '' #str(opt['Debit'])
        Credit          = '' #str(opt['Credit'])
        CB              = '' #str(opt['CB'])
        TotalDue        = 0
        OverDueDays     = str(opt['Overdue_Days'])
        DueDaysGroup    = 0
        DocDate         = str(opt['Posting Date'])
        DueDate         = str(opt['DueDate'])

        # new keys
        ContactPerson   = str(opt['ContactPerson']).replace('"', "")
        GSTIN           = str(opt['GSTIN'])
        MobileNo        = str(opt['MobileNo'])
        EmailAddress    = str(opt['Email'])
        CreditLimit     = str(opt['CreditLimit'])
        CreditLimitDayes= str(opt['PaymentTerm'])
        BPAddresses     = str(opt['Address']).replace('"', "")
        # CronUpdateCount = 0
        Datetime        = serverDateTime
        grp1            = str(opt['0-30'])
        grp2            = str(opt['31-60'])
        grp3            = str(opt['61-90'])
        grp4            = str(opt['91-120'])
        grp5            = str(opt['120+'])
        
        # print("CardCode: ", CardCode, "TransId", TransId, "TransType", TransType)

        if float(grp1) != 0.0:
            TotalDue = grp1
            DueDaysGroup = '0'
        elif float(grp2) != 0.0:
            TotalDue = grp2
            DueDaysGroup = '30'
        elif float(grp3) != 0.0:
            TotalDue = grp3
            DueDaysGroup = '60'
        elif float(grp4) != 0.0:
            TotalDue = grp4
            DueDaysGroup = '90'
        elif float(grp5) != 0.0:
            TotalDue = grp5
            DueDaysGroup = '120'

        # if CardCode.strip() != 'None':
        if True:
            # checkPaymentQuery = f"select * from BusinessPartner_receivable WHERE CardCode = '{CardCode}' AND TransId = '{TransId}'"
            # print(checkPaymentQuery)
            # mycursor.execute(checkPaymentQuery)
            # if mycursor.rowcount == 0:
            if True:
                sqlInsertReceivalbe = f'INSERT INTO `BusinessPartner_receivable`(`CardCode`, `CardName`, `SalesEmployeeCode`, `U_U_UTL_Zone`, `GroupCode`, `GroupName`, `DocEntry`, `TransId`, `TransType`, `OB`, `Debit`, `Credit`, `CB`, `TotalDue`, `DueDaysGroup`, `DocDate`, `DueDate`, `CronUpdateCount`, `Datetime`, `ContactPerson`, `GSTIN`, `MobileNo`, `EmailAddress`, `CreditLimit`, `CreditLimitDayes`, `BPAddresses`,`DocNum`, `OverDueDays`) VALUES ("{CardCode}", "{CardName}", "{SalesEmployeeCode}", "{U_U_UTL_Zone}", "{GroupCode}", "{GroupName}", "{DocEntry}", "{TransId}", "{TransType}", "{OB}", "{Debit}", "{Credit}", "{CB}", "{TotalDue}", "{DueDaysGroup}", "{DocDate}", "{DueDate}", "{CronUpdateCount}", "{Datetime}", "{ContactPerson}", "{GSTIN}", "{MobileNo}", "{EmailAddress}", "{CreditLimit}", "{CreditLimitDayes}", "{BPAddresses}", "{DocNum}", "{OverDueDays}")'
                print(sqlInsertReceivalbe) 
                mycursor.execute(sqlInsertReceivalbe)
                mydb.commit()
                receivalbeId = mycursor.lastrowid
                
            # else:
            #     sqlUpdateReceivable = f'UPDATE `BusinessPartner_receivable` SET  `OB` = "{OB}", `Debit` = "{Debit}", `Credit` = "{Credit}", `CB` = "{CB}", `TotalDue` = "{TotalDue}", `DueDaysGroup` = "{DueDaysGroup}", `DocDate` = "{DocDate}", `DueDate` = "{DueDate}", `CronUpdateCount` = "{CronUpdateCount}" WHERE CardCode = "{CardCode}" AND TransId = "{TransId}"'
            #     print(sqlUpdateReceivable) 
            #     mycursor.execute(sqlUpdateReceivable)
            #     mydb.commit()
            #     # receivalbeId = mycursor.lastrowid
        # endif
    # endfor
# endWhile

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#   Delete Unuse data form receivable
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# sqlInsertReceivalbe = f'DELETE FROM `BusinessPartner_receivable` WHERE CronUpdateCount < ( SELECT MAX(`CronUpdateCount`) FROM ( SELECT DISTINCT `CronUpdateCount` FROM `BusinessPartner_receivable` ORDER BY id ASC LIMIT 1 OFFSET 1 ) AS subquery );'
# sqlInsertReceivalbe = f'DELETE FROM `BusinessPartner_receivable` WHERE `CronUpdateCount` < (SELECT MAX(`CronUpdateCount`) FROM BusinessPartner_receivable) - 1;'

# sqlInsertReceivalbe = f"CREATE TEMPORARY TABLE temp_table AS SELECT MAX(CronUpdateCount) - 2 AS max_cron_update_count FROM BusinessPartner_receivable; DELETE FROM BusinessPartner_receivable WHERE CronUpdateCount < (SELECT max_cron_update_count FROM temp_table); DROP TEMPORARY TABLE temp_table;"
# print(sqlInsertReceivalbe) 
# mycursor.execute(sqlInsertReceivalbe, multi=True)
# mydb.commit()

# sqlInsertReceivable = (
#     "CREATE TEMPORARY TABLE temp_table AS SELECT MAX(CronUpdateCount) - 2 AS max_cron_update_count FROM BusinessPartner_receivable; "
#     "DELETE FROM BusinessPartner_receivable WHERE CronUpdateCount < (SELECT max_cron_update_count FROM temp_table); "
#     "DROP TEMPORARY TABLE temp_table;"
# )
# print(sqlInsertReceivable)
# mycursor.execute(sqlInsertReceivable, multi=True)
# mydb.commit()
# mydb.close()