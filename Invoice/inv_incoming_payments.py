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
    settings.custome_error_logs('cron start', module_name='inv_incoming_payments')

    lastDocEntry = 0
    mycursor.execute("SELECT * FROM `Invoice_incomingpayments` ORDER BY `id` desc LIMIT 1")
    entryData = mycursor.fetchall()
    if len(entryData) > 0:
        lastDocEntry = entryData[0]['DocEntry']
        print(lastDocEntry)

    skip=0
    # for i in range(count):
    while skip != "":

        sapAPIUrl = f"/IncomingPayments?$filter = DocEntry gt {lastDocEntry}&$skip = {skip}"
        print(sapAPIUrl)
        res = requests.get(settings.SAPURL+sapAPIUrl, cookies=ses.cookies, verify=False)
        # print(res.text)
        opts = json.loads(res.text)

        for opt in opts['value']:
            # try:
            DocEntry = opt['DocEntry']
            print("DocEntry: ", DocEntry)

            checkPaymentQuery = f"select * from Invoice_incomingpayments WHERE DocEntry = '{DocEntry}'"
            print(checkPaymentQuery)
            mycursor.execute(checkPaymentQuery)
            if mycursor.rowcount == 0:
                DocNum          = str(opt['DocNum'])
                DocType         = urllib.parse.quote(str(opt['DocType']))
                DocDate         = str(opt['DocDate'])
                CardCode        = urllib.parse.quote(str(opt['CardCode']))
                CardName        = urllib.parse.quote(str(opt['CardName']))
                # Address         = urllib.parse.quote(str(opt['Address']))
                Address         = ''
                DocCurrency     = urllib.parse.quote(str(opt['DocCurrency']))
                CheckAccount    = urllib.parse.quote(str(opt['CheckAccount']))
                TransferAccount = urllib.parse.quote(str(opt['TransferAccount']))
                TransferSum     = float(opt['TransferSum'])
                TransferDate    = str(opt['TransferDate'])
                Series          = str(opt['Series'])
                DocEntry        = str(opt['DocEntry'])
                DueDate         = str(opt['DueDate'])
                BPLID           = str(opt['BPLID'])
                BPLName         = urllib.parse.quote(str(opt['BPLName']))
                Comments        = urllib.parse.quote(str(opt['Remarks']))
                JournalRemarks  = str(opt['JournalRemarks'])
                TransferReference = urllib.parse.quote(str(opt['TransferReference']))
                print("CardName: ", CardName)

                # print("TransferSum", TransferSum)
                if TransferSum == 0.0:
                    print('in if')
                    # if len(opt['PaymentInvoices']) > 0:
                    #     for line in opt['PaymentInvoices']:
                    #         TransferSum = TransferSum + float(line['SumApplied'])
                    
                    if len(opt['PaymentCreditCards']) > 0:
                        for line in opt['PaymentCreditCards']:
                            TransferSum = TransferSum + float(line['CreditSum'])
                    
                    if len(opt['PaymentChecks']) > 0:
                        for line in opt['PaymentChecks']:
                            TransferSum = TransferSum + float(line['CheckSum'])
                    
                    # if len(opt['PaymentAccounts']) > 0:
                    #     for line in opt['PaymentAccounts']:
                    #         TransferSum = TransferSum + float(line['SumPaid'])
                    TransferSum = TransferSum + float(opt['CashSumSys'])

                    print("TransferSum", TransferSum)
                    # exit()
                else:
                    print("in else", TransferSum)

                    
                add_incommingPayemnt = f'INSERT INTO `Invoice_incomingpayments`(`DocEntry`, `CardCode`, `CardName`, `DocDate`, `TransferAccount`, `TransferSum`, `TransferDate`, `TransferReference`, `Address`, `BPLID`, `BPLName`, `CheckAccount`, `DocCurrency`, `DocNum`, `DocType`, `DueDate`, `Series`, `Comments`, `JournalRemarks`) VALUES("{DocEntry}", "{CardCode}", "{CardName}", "{DocDate}", "{TransferAccount}", "{TransferSum}", "{TransferDate}", "{TransferReference}", "{Address}", "{BPLID}", "{BPLName}", "{CheckAccount}", "{DocCurrency}", "{DocNum}", "{DocType}", "{DueDate}", "{Series}", "{Comments}", "{JournalRemarks}")'
                print(add_incommingPayemnt) 
                mycursor.execute(add_incommingPayemnt)
                mydb.commit()
                IncomingPaymentsId = mycursor.lastrowid

                    
                for line in opt['PaymentInvoices']:

                    # # Check Invoice Exist or not
                    # docSelectQuery = f"select * from Invoice_invoice WHERE DocEntry = '{InvoiceDocEntry}'"
                    # print(docSelectQuery)
                    # mycursor.execute(docSelectQuery)
                    # mycursor.fetchall()
                    # if mycursor.rowcount != 0:
                    LineNum = str(line['LineNum'])
                    InvoiceDocEntry = str(line['DocEntry'])
                    SumApplied = str(line['SumApplied'])
                    AppliedFC = str(line['AppliedFC'])
                    AppliedSys = str(line['AppliedSys'])
                    DiscountPercent = str(line['DiscountPercent'])
                    TotalDiscount = str(line['TotalDiscount'])
                    TotalDiscountFC = str(line['TotalDiscountFC'])
                    TotalDiscountSC = str(line['TotalDiscountSC'])
                        
                    add_incommingPayemntInvoice = f'INSERT INTO `Invoice_incomingpaymentinvoices`(`LineNum`, `InvoiceDocEntry`, `SumApplied`, `AppliedFC`, `AppliedSys`, `DiscountPercent`, `TotalDiscount`, `TotalDiscountFC`, `TotalDiscountSC`, `IncomingPaymentsId`, `DocDate`) VALUES("{LineNum}", "{InvoiceDocEntry}", "{SumApplied}", "{AppliedFC}", "{AppliedSys}", "{DiscountPercent}", "{TotalDiscount}", "{TotalDiscountFC}", "{TotalDiscountSC}", "{IncomingPaymentsId}", "{DocDate}")'
                    print(add_incommingPayemntInvoice) 
                    mycursor.execute(add_incommingPayemntInvoice)
                    mydb.commit()
                # endfor
            # endif
        # endfor
        
        if 'odata.nextLink' in opts:
            nextLink = opts['odata.nextLink']
            print(">>>>>>>>>>>>>>>>>>>>> nextLink: ", nextLink)
            nextLink = nextLink.split("skip=")
            print(nextLink)
            skip = str(nextLink[1]).strip()

        else:
            print("<<<<<<<<<<<<<<<<<<<<< nextLink: ", "")
            skip = ""
            exit()

        print("skip", skip)
    # endWhile
    settings.custome_error_logs('cron end', module_name='inv_incoming_payments')
except Exception as e:
    print(str(e))
    settings.custome_error_logs(message=str(e), module_name='inv_incoming_payments')