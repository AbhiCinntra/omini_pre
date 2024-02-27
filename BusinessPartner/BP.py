import mysql.connector
import calendar
import requests, json
import time
import math
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

print("Today date is: ", currentDate)
print("Today day is: ", currentDay)
print("Today Current time: ", currentTime)
print("Today Current serverDateTime: ", serverDateTime)
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
    settings.custome_error_logs('cron start', module_name='bp')

    SAPUrl = settings.SAPURL+"/BusinessPartners/$count"
    print("SAPUrl", SAPUrl)
    serBPCount = requests.get(SAPUrl, cookies=ses.cookies, verify=False).text

    # count the number if loop run, each one skip 20 values
    count = math.ceil(int(serBPCount)/20)
    # print(count)

    mycursor.execute("select * from BusinessPartner_businesspartner")
    mycursor.fetchall()
    localBPCount = mycursor.rowcount


    print(f'local BP count: {localBPCount} and server BP count {serBPCount}')
    # if localBPCount < serBPCount:

    skip=0
    for i in range(count):

        # bpRes = requests.get(settings.SAPURL+"/BusinessPartners?$filter = CardType eq 'cCustomer'&$skip="+str(skip), cookies=ses.cookies, verify=False)
        bpRes = requests.get(settings.SAPURL+"/BusinessPartners?$skip="+str(skip), cookies=ses.cookies, verify=False)
        bps = json.loads(bpRes.text)
        # print(len(bps['value']))
        for bp in bps['value']:
            bpcode          = bp['CardCode']
            CreatedBy       = 1
            FreeDelivery    = 1
            Unit            = bp['BPBranchAssignment'][0]['BPLID']
            CardCode        = (bp['CardCode'])
            CardName        = str(bp['CardName']).replace("'", "&sbquo;")
            Industry        = (bp['Industry'])
            CardType        = (bp['CardType'])
            Website         = (bp['Website'])
            EmailAddress    = (bp['EmailAddress'])
            Phone1          = (bp['Phone1'])
            DiscountPercent = (bp['DiscountPercent'])
            Currency        = (bp['Currency'])
            IntrestRatePercent = (bp['IntrestRatePercent'])
            CommissionPercent = (bp['CommissionPercent'])
            Notes           = (bp['Notes'])
            PayTermsGrpCode = (bp['PayTermsGrpCode'])
            CreditLimit     = (bp['CreditLimit'])
            AttachmentEntry = (bp['AttachmentEntry'])
            SalesPersonCode = (bp['SalesPersonCode'])
            ContactPerson   = (bp['ContactPerson'])
            CreateDate      = (bp['CreateDate'])
            CreateTime      = (bp['CreateTime'])
            UpdateDate      = (bp['UpdateDate'])
            UpdateTime      = (bp['UpdateTime'])
            PriceListNum    = bp['PriceListNum']
            GroupCode       = bp['GroupCode']
            U_U_UTL_Zone    = 'India' #bp['U_U_UTL_Zone']
            U_U_UTL_DEPT    = '' #bp['U_U_UTL_DEPT']
            U_U_UTL_EXEC    = '' #bp['U_U_UTL_EXEC']
            U_U_UTL_DIRC    = '' #bp['U_U_UTL_DIRC']

            Link    = "Sales Executive"
            Valid   = str(bp['Valid']) # active status
            LinkedBusinessPartner = str(bp['LinkedBusinessPartner'])

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
                    for emp in bp['ContactEmployees']:
                        emp_sql = "INSERT INTO `BusinessPartner_bpemployee` (`Title`, `FirstName`, `MiddleName`, `LastName`, `Position`, `Address`, `MobilePhone`, `Fax`, `E_Mail`, `Remarks1`, `InternalCode`, `DateOfBirth`, `Gender`, `Profession`, `CardCode`, `U_BPID`, `U_BRANCHID`, `U_NATIONALTY`, `CreateDate`, `CreateTime`, `UpdateDate`, `UpdateTime`) VALUES ('"+str(emp['Title']).replace("'", "&sbquo;")+"', '"+str(emp['Name']).replace("'", "&sbquo;")+"', '"+str(emp['MiddleName']).replace("'", "&sbquo;")+"', '"+str(emp['LastName']).replace("'", "&sbquo;")+"', '"+str(emp['Position'])+"', '"+str(emp['Address']).replace("'", "&sbquo;")+"', '"+str(emp['MobilePhone'])+"', '"+str(emp['Fax'])+"', '"+str(emp['E_Mail'])+"', '"+str(emp['Remarks1'])+"', '"+str(emp['InternalCode'])+"', '"+str(emp['DateOfBirth'])+"', '"+str(emp['Gender'])+"', '"+str(emp['Profession'])+"','"+str(bpcode)+"', '"+str(bpid)+"', '', '', '"+str(emp['CreateDate'])+"', '"+str(emp['CreateTime'])+"', '"+str(emp['UpdateDate'])+"', '"+str(emp['UpdateTime'])+"');"
                        # print(emp_sql)
                        mycursor.execute(emp_sql)
                        mydb.commit()
            else:
                sqlBp = f"UPDATE `BusinessPartner_businesspartner` SET `CardName` = '{CardName}', `EmailAddress` = '{EmailAddress}', `Phone1` = '{Phone1}', `CreditLimit` = '{CreditLimit}', `CreditLimitLeft` = '{newLeftCreditLimit}', `CurrentAccountBalance` = '{CurrentAccountBalance}', `OpenDeliveryNotesBalance` = '{OpenDeliveryNotesBalance}', `OpenOrdersBalance` = '{OpenOrdersBalance}', `OpenChecksBalance` = '{OpenChecksBalance}', `GroupCode` = '{GroupCode}',`U_U_UTL_Zone` = '{U_U_UTL_Zone}', `U_U_UTL_DEPT` = '{U_U_UTL_DEPT}', `U_U_UTL_EXEC` = '{U_U_UTL_EXEC}',`U_U_UTL_DIRC` = '{U_U_UTL_DIRC}', `LinkedBusinessPartner`= '{LinkedBusinessPartner}'  WHERE `CardCode` = '{CardCode}'"
                # print(sqlBp)
                mycursor.execute(sqlBp)
                mydb.commit()
                bpid = mycursor.lastrowid

                if len(bp['BPAddresses']) > 0:
                    for branch in bp['BPAddresses']:
                        addrAddressName     = str(branch['AddressName']).replace("'", "&sbquo;")
                        addrAddressName2    = str(branch['AddressName2']).replace("'", "&sbquo;")
                        addrAddressName3    = str(branch['AddressName3']).replace("'", "&sbquo;")
                        addrBuildingFloorRoom = str(branch['BuildingFloorRoom']).replace("'", "&sbquo;")
                        addrStreet          = str(branch['Street']).replace("'", "&sbquo;")
                        addrBlock           = str(branch['Block']).replace("'", "&sbquo;")
                        addrCity            = str(branch['City']).replace("'", "&sbquo;")
                        addrState           = str(branch['State']).replace("'", "&sbquo;")
                        addrZipCode         = str(branch['ZipCode']).replace("'", "&sbquo;")
                        addrCounty          = str(branch['County']).replace("'", "&sbquo;")
                        addrCountry         = str(branch['Country']).replace("'", "&sbquo;")
                        addrAddressType     = str(branch['AddressType']).replace("'", "&sbquo;")
                        addrTaxOffice       = str(branch['TaxOffice']).replace("'", "&sbquo;")
                        addrGSTIN           = str(branch['GSTIN']).replace("'", "&sbquo;")
                        addrGstType         = str(branch['GstType']).replace("'", "&sbquo;")
                        addrShippingType    = ''
                        addrRowNum          = str(branch['RowNum']).replace("'", "&sbquo;")
                        
                        if int(branch['RowNum']) == 0:
                            sqlBPAddressUpdate = f"UPDATE `BusinessPartner_bpaddresses` SET `AddressName`='{addrAddressName}',`Street`='{addrStreet}',`Block`='{addrBlock}',`City`='{addrCity}',`State`='{addrState}',`ZipCode`='{addrZipCode}',`Country`='{addrCountry}',`AddressType`='{addrAddressType}',`GSTIN`='{addrGSTIN}',`GstType`='{addrGstType}' WHERE `BPCode` = '{CardCode}' AND `RowNum` = {addrRowNum}"
                            # print(sqlBPAddressUpdate)
                            mycursor.execute(sqlBPAddressUpdate)
                            mydb.commit()
                        else:
                            
                            sqlBPBranchUpdate = f"UPDATE `BusinessPartner_bpbranch` SET `AddressName`='{addrAddressName}',`AddressName2`='{addrAddressName2}',`AddressName3`='{addrAddressName3}',`BuildingFloorRoom`='{addrBuildingFloorRoom}',`Street`='{addrStreet}',`Block`='{addrBlock}',`County`='{addrCounty}',`City`='{addrCity}',`State`='{addrState}',`ZipCode`='{addrZipCode}',`Country`='{addrCountry}',`AddressType`='{addrAddressType}',`TaxOffice`='{addrTaxOffice}',`GSTIN`='{addrGSTIN}',`GstType`='{addrGstType}',`ShippingType`='{addrShippingType}' WHERE `BPCode` = '{CardCode}' AND `RowNum` = {addrRowNum}"
                            # print(sqlBPBranchUpdate)
                            mycursor.execute(sqlBPBranchUpdate)
                            mydb.commit()

                # print('-----ContactEmployees---')
                # if len(bp['ContactEmployees']) > 0:
                #     print(len(bp['ContactEmployees']))
                #     for emp in bp['ContactEmployees']:
                #         print("Title : "+str(emp['Title']))
                #         emp_sql = "INSERT INTO `BusinessPartner_bpemployee` (`Title`, `FirstName`, `MiddleName`, `LastName`, `Position`, `Address`, `MobilePhone`, `Fax`, `E_Mail`, `Remarks1`, `InternalCode`, `DateOfBirth`, `Gender`, `Profession`, `CardCode`, `U_BPID`, `U_BRANCHID`, `U_NATIONALTY`, `CreateDate`, `CreateTime`, `UpdateDate`, `UpdateTime`) VALUES ('"+str(emp['Title']).replace("'", "&sbquo;")+"', '"+str(emp['FirstName']).replace("'", "&sbquo;")+"', '"+str(emp['MiddleName']).replace("'", "&sbquo;")+"', '"+str(emp['LastName']).replace("'", "&sbquo;")+"', '"+str(emp['Position'])+"', '"+str(emp['Address']).replace("'", "&sbquo;")+"', '"+str(emp['MobilePhone'])+"', '"+str(emp['Fax'])+"', '"+str(emp['E_Mail'])+"', '"+str(emp['Remarks1'])+"', '"+str(emp['InternalCode'])+"', '"+str(emp['DateOfBirth'])+"', '"+str(emp['Gender'])+"', '"+str(emp['Profession'])+"','"+str(bpcode)+"', '"+str(bpid)+"', '', '', '"+str(emp['CreateDate'])+"', '"+str(emp['CreateTime'])+"', '"+str(emp['UpdateDate'])+"', '"+str(emp['UpdateTime'])+"');"
                #         print(emp_sql)
                #         mycursor.execute(emp_sql)
                #         mydb.commit()
                
        skip = skip+20
        print(skip)
    settings.custome_error_logs('cron end', module_name='bp')
except Exception as e:
    print(str(e))
    settings.custome_error_logs(message=str(e), module_name='bp')