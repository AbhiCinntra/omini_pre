import mysql.connector
import calendar
import requests, json
from datetime import date, datetime
import sys, os

def none(inp):
    inp = str(inp)
    if inp.lower()=="none":
        return "";
    else:
        return inp

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
  host = settings.DATABASES['default']['HOST'],
  user = settings.DATABASES['default']['USER'],
  password = settings.DATABASES['default']['PASSWORD'],
  database = settings.DATABASES['default']['NAME']
)
mycursor = mydb.cursor(buffered=True, dictionary=True)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
try:
    settings.custome_error_logs('cron start', module_name='sync_bp_every_five_minute')
    
    lastEntryNumber = 0
    mycursor.execute("SELECT * FROM `JournalEntries_journalentries` ORDER BY `id` desc LIMIT 1")
    entryData = mycursor.fetchall()
    if len(entryData) > 0:
        lastEntryNumber = entryData[0]['JdtNum']
        # print(lastEntryNumber)
    skip=0
    while skip != "":
        tempPrint = 0

        baseUrl = f"/BusinessPartners?$filter = CreateDate ge '{str(currentDate)}'"
        res = requests.get(settings.SAPURL+baseUrl, cookies=ses.cookies, headers={"Prefer":"odata.maxpagesize=100"}, verify=False)
        # print(res.text)
        opts = json.loads(res.text)
        for bp in opts['value']:
            print('-----Business Partner---', str(bp['CardCode']))
            bpcode = bp['CardCode']
            CreatedBy = 1
            FreeDelivery = 1
            Unit       = bp['BPBranchAssignment'][0]['BPLID']
            CardCode   = (bp['CardCode'])
            CardName   = str(bp['CardName']).replace("'", "&sbquo;")
            Industry   = (bp['Industry'])
            CardType   = (bp['CardType'])
            Website    = (bp['Website'])
            EmailAddress = (bp['EmailAddress'])
            Phone1     = (bp['Phone1'])
            DiscountPercent = (bp['DiscountPercent'])
            Currency   = (bp['Currency'])
            IntrestRatePercent = (bp['IntrestRatePercent'])
            CommissionPercent = (bp['CommissionPercent'])
            Notes      = (bp['Notes'])
            PayTermsGrpCode = (bp['PayTermsGrpCode'])
            CreditLimit = (bp['CreditLimit'])
            AttachmentEntry = (bp['AttachmentEntry'])
            SalesPersonCode = (bp['SalesPersonCode'])
            ContactPerson = (bp['ContactPerson'])
            CreateDate = (bp['CreateDate'])
            CreateTime = (bp['CreateTime'])
            UpdateDate = (bp['UpdateDate'])
            UpdateTime = (bp['UpdateTime'])
            PriceListNum = bp['PriceListNum']
            GroupCode = bp['GroupCode']
            U_U_UTL_Zone = bp['U_U_UTL_Zone']
            U_U_UTL_DEPT = bp['U_U_UTL_DEPT']
            U_U_UTL_EXEC = bp['U_U_UTL_EXEC']
            U_U_UTL_DIRC = bp['U_U_UTL_DIRC']
            LinkedBusinessPartner = str(bp['LinkedBusinessPartner'])
            
            Link = "Sales Executive"
            Valid = str(bp['Valid']) # active status

            # if Valid == 'tNO':
            #     # print('inactive BP')
            #     continue

            updatedCreditLimit      = float(bp['CreditLimit'])
            CurrentAccountBalance   = bp['CurrentAccountBalance']
            OpenDeliveryNotesBalance = bp['OpenDeliveryNotesBalance']
            OpenOrdersBalance       = bp['OpenOrdersBalance']
            OpenChecksBalance       = bp['OpenChecksBalance'] # not in currently used
            totalCreditLimitUsed    = float(float(CurrentAccountBalance) + float(OpenDeliveryNotesBalance) + float(OpenOrdersBalance))
            newLeftCreditLimit      = float(updatedCreditLimit - totalCreditLimitUsed)

            sql_select_bp = f"SELECT `id` FROM BusinessPartner_businesspartner WHERE CardCode = '{bpcode}'"
            print(sql_select_bp)
            mycursor.execute(sql_select_bp)
            bpData = mycursor.fetchall()
            if mycursor.rowcount != 1:
                
                sqlBp = f"INSERT INTO `BusinessPartner_businesspartner`(`CardCode`, `CardName`, `Industry`, `CardType`, `Website`, `EmailAddress`, `Phone1`, `DiscountPercent`, `Currency`, `IntrestRatePercent`, `CommissionPercent`, `Notes`, `PayTermsGrpCode`, `CreditLimit`, `AttachmentEntry`, `SalesPersonCode`, `ContactPerson`, `BPAddresses`, `U_PARENTACC`, `U_BPGRP`, `U_CONTOWNR`, `U_RATING`, `U_TYPE`, `U_ANLRVN`, `U_CURBAL`, `U_ACCNT`, `U_INVNO`, `U_LAT`, `U_LONG`, `CreateDate`, `CreateTime`, `UpdateDate`, `UpdateTime`, `U_LEADID`, `U_LEADNM`, `CustomerType`, `DeliveryMode`, `GroupType`, `PaymantMode`, `PriceCategory`, `Turnover`, `ACNumber`, `BankName`, `BeneficiaryName`, `IfscCode`, `TCS`, `Link`, `Unit`, `CreditLimitLeft`, `FreeDelivery`, `CreatedBy`, `CreatedFromSap`, `CurrentAccountBalance`,`OpenDeliveryNotesBalance`,`OpenOrdersBalance`,`OpenChecksBalance`, `GroupCode`,`U_U_UTL_Zone`,`U_U_UTL_DEPT`,`U_U_UTL_EXEC`,`U_U_UTL_DIRC`, `LinkedBusinessPartner`) VALUES ('{CardCode}','{CardName}','{Industry}','{CardType}','{Website}','{EmailAddress}','{Phone1}','{DiscountPercent}','{Currency}','{IntrestRatePercent}','{CommissionPercent}','{Notes}','{PayTermsGrpCode}','{CreditLimit}','{AttachmentEntry}','{SalesPersonCode}','{ContactPerson}','','','','','','','','','','','','', '{CreateDate}','{CreateTime}','{UpdateDate}','{UpdateTime}','','','','','','','{PriceListNum}','','','','','','No','{Link}','{Unit}','{newLeftCreditLimit}','{FreeDelivery}','{CreatedBy}', '1','{CurrentAccountBalance}','{OpenDeliveryNotesBalance}','{OpenOrdersBalance}','{OpenChecksBalance}','{GroupCode}','{U_U_UTL_Zone}','{U_U_UTL_DEPT}','{U_U_UTL_EXEC}','{U_U_UTL_DIRC}', '{LinkedBusinessPartner}')"
                # print(sqlBp)
                mycursor.execute(sqlBp)
                mydb.commit()
                bpid = mycursor.lastrowid
                # print("BP ID: "+str(bpid))

                # print('-----BPAddresses---')
                if len(bp['BPAddresses']) > 0:
                    # print(len(bp['BPAddresses']))
                    for branch in bp['BPAddresses']:
                        # print("BP Address ID: "+str(branch['AddressName']))

                        if int(branch['RowNum']) == 0:
                            sqlBPAddress = "INSERT INTO `BusinessPartner_bpaddresses`(`BPID`, `BPCode`, `AddressName`, `Street`, `Block`, `City`, `State`, `ZipCode`, `Country`, `AddressType`, `RowNum`, `U_SHPTYP`, `U_COUNTRY`, `U_STATE`, `District`, `GSTIN`, `GstType`) VALUES ('"+str(bpid)+"', '"+str(branch['BPCode']).replace("'", "&sbquo;")+"', '"+str(branch['AddressName']).replace("'", "&sbquo;")+"', '"+str(none(branch['Street'])).replace("'", "&sbquo;")+"', '"+str(none(branch['Block'])).replace("'", "&sbquo;")+"', '"+str(branch['City']).replace("'", "&sbquo;")+"', '"+str(branch['State'])+"', '"+str(branch['ZipCode'])+"', '"+str(branch['Country'])+"', '"+str(branch['AddressType']).replace("'", "&sbquo;")+"', '"+str(branch['RowNum'])+"', '','','','', '"+str(branch['GSTIN'])+"', '"+str(branch['GstType'])+"')"
                            # print(sqlBPAddress)
                            mycursor.execute(sqlBPAddress)
                            mydb.commit()
                        else:
                            # print('-----BPBranch---')
                            branch_sql = "INSERT INTO `BusinessPartner_bpbranch`(`BPID`, `RowNum`, `BPCode`, `BranchName`, `AddressName`, `AddressName2`, `AddressName3`, `BuildingFloorRoom`, `Street`, `Block`, `County`, `City`, `State`, `ZipCode`, `Country`, `AddressType`, `Phone`, `Fax`, `Email`, `TaxOffice`, `GSTIN`, `GstType`, `ShippingType`, `PaymentTerm`, `CurrentBalance`, `CreditLimit`, `Lat`, `Long`, `Status`, `Default`, `U_SHPTYP`, `U_COUNTRY`, `U_STATE`, `CreateDate`, `CreateTime`, `UpdateDate`, `UpdateTime`, `District`) VALUES ('"+str(bpid)+"', '"+str(branch['RowNum'])+"', '"+str(branch['BPCode'])+"', '', '"+str(branch['AddressName']).replace("'", "&sbquo;")+"', '"+str(branch['AddressName2']).replace("'", "&sbquo;")+"', '"+str(branch['AddressName3']).replace("'", "&sbquo;")+"', '"+str(branch['BuildingFloorRoom']).replace("'", "&sbquo;")+"', '"+str(none(branch['Street'])).replace("'", "&sbquo;")+"', '"+str(none(branch['Block'])).replace("'", "&sbquo;")+"', '"+str(branch['County']).replace("'", "&sbquo;")+"', '"+str(branch['City']).replace("'", "&sbquo;")+"', '"+str(branch['State']).replace("'", "&sbquo;")+"', '"+str(branch['ZipCode'])+"', '"+str(branch['Country'])+"', '"+str(branch['AddressType']).replace("'", "&sbquo;")+"', '','','', '"+str(branch['TaxOffice']).replace("'", "&sbquo;")+"', '"+str(branch['GSTIN'])+"', '"+str(branch['GstType'])+"', '','','','','', '', 1, 0,'','','', '"+str(branch['CreateDate'])+"', '"+str(branch['CreateTime'])+"', '', '', '');"
                            # print(branch_sql)
                            mycursor.execute(branch_sql)
                            mydb.commit()

                # print('-----ContactEmployees---')
                if len(bp['ContactEmployees']) > 0:
                    # print(len(bp['ContactEmployees']))
                    for emp in bp['ContactEmployees']:
                        # print("Title : "+str(emp['Title']))
                        emp_sql = "INSERT INTO `BusinessPartner_bpemployee` (`Title`, `FirstName`, `MiddleName`, `LastName`, `Position`, `Address`, `MobilePhone`, `Fax`, `E_Mail`, `Remarks1`, `InternalCode`, `DateOfBirth`, `Gender`, `Profession`, `CardCode`, `U_BPID`, `U_BRANCHID`, `U_NATIONALTY`, `CreateDate`, `CreateTime`, `UpdateDate`, `UpdateTime`) VALUES ('"+str(emp['Title']).replace("'", "&sbquo;")+"', '"+str(emp['Name']).replace("'", "&sbquo;")+"', '"+str(emp['MiddleName']).replace("'", "&sbquo;")+"', '"+str(emp['LastName']).replace("'", "&sbquo;")+"', '"+str(emp['Position'])+"', '"+str(emp['Address']).replace("'", "&sbquo;")+"', '"+str(emp['MobilePhone'])+"', '"+str(emp['Fax'])+"', '"+str(emp['E_Mail'])+"', '"+str(emp['Remarks1'])+"', '"+str(emp['InternalCode'])+"', '"+str(emp['DateOfBirth'])+"', '"+str(emp['Gender'])+"', '"+str(emp['Profession'])+"','"+str(bpcode)+"', '"+str(bpid)+"', '', '', '"+str(emp['CreateDate'])+"', '"+str(emp['CreateTime'])+"', '"+str(emp['UpdateDate'])+"', '"+str(emp['UpdateTime'])+"');"
                        # print(emp_sql)
                        mycursor.execute(emp_sql)
                        mydb.commit()
                    # endFor
                # endIf
            # endIf
        # end for

        if 'odata.nextLink' in opts:
            nextLink = opts['odata.nextLink']
            nextLink = nextLink.split("skip=")
            skip = str(nextLink[1]).strip()
        else:
            skip = ""
    # end while
    settings.custome_error_logs('cron end', module_name='sync_bp_every_five_minute')
except Exception as e:
        print(str(e))
        settings.custome_error_logs(message=str(e), module_name='sync_bp_every_five_minute')