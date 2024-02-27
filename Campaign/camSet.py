from ctypes import sizeof
import requests, json
import time
import math
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
#   password="root",
  password="$Bridge@2022#",
  database="rg_industries_prod"
)

mycursor = mydb.cursor()

userList = []

# sqlSelectCamSet = "SELECT * FROM `Campaign_campaignset` WHERE `id` = 38"
sqlSelectCamSet = "SELECT `id`, `CampaignSetName`, `CampaignAccess`, `Description`, `LeadSource`, `LeadPriority`, `LeadStatus`, `LeadFromDate`, `LeadToDate`, `OppType`, `OppSalePerson`, `OppStage`, `OppFromDate`, `OppToDate`, `BPType`, `BPSalePerson`, `BPCountry`, `BPState`, `BPIndustry`, `BPFromDate`, `BPToDate`, `MemberList`, `Status`, `CreateDate`, `CreateTime`, `CampaignSetOwner_id`, `CreateBy_id`, `BPCountryCode`, `BPStateCode`, `AllBP`, `AllLead`, `AllOpp` FROM `Campaign_campaignset` WHERE Status = 1"
mycursor.execute(sqlSelectCamSet)
allRow = mycursor.fetchall()
for campaign in allRow:
    print('----- campset data -----')
    print(campaign)
    camSetId = campaign[0]

    AllBPCheck = campaign[29]
    AllLeadCheck = campaign[30]
    AllOppCheck = campaign[31]

    # ----------------------------------
    # -------Filter for Lead -----------
    # ----------------------------------
    leadFlag = False;

    if AllLeadCheck == 1:
        leadwhere = ''
        leadFlag = True;
    else:
        leadwhere = 'WHERE 1 '
        LeadSource = campaign[4].strip()
        LeadPriority = campaign[5].strip()
        LeadStatus = campaign[6].strip()
        LeadFromDate = campaign[7].strip()
        LeadToDate = campaign[8].strip()

        if LeadSource != "":
            leadwhere += 'and `source` in("'+ LeadSource.replace(',','","') +'") '
            leadFlag = True;

        if LeadPriority != "":
            leadwhere += 'and `leadType` in("'+ LeadPriority.replace(',','","') +'") '
            leadFlag = True;

        if LeadStatus != "":
            leadwhere += 'and `status` in("'+ LeadStatus.replace(',','","') +'") '
            leadFlag = True;

        if LeadFromDate != "" and LeadToDate != "":
            leadwhere += 'and `date` <= "'+ LeadFromDate + '" and `date` >= "'+  LeadToDate +'" '
            leadFlag = True;

    if leadFlag:
        sqlSelectLead = "SELECT `id`, `contactPerson`, `phoneNumber`, `email`, `leadType`, `status` FROM `Lead_lead` " + leadwhere
        print('----- lead data -----')
        print(sqlSelectLead)
        mycursor.execute(sqlSelectLead)
        allLead = mycursor.fetchall()
        # print(len(allLead))
        for contactPrson in allLead:
            userData = {
                'Name': contactPrson[1],
                'Phone': contactPrson[2],
                'Email': contactPrson[3]
            }
            userList.append(userData)
        
    
    # ----------------------------------------
    # --------- Oppertunity data -------------
    # ----------------------------------------
    oppFlag = False;

    if AllOppCheck == 1:
        oppwhere = ''
        oppFlag = True;
    else:   
        oppwhere = 'WHERE 1 '
        OppType = campaign[9].strip()
        OppSalePerson = campaign[10].strip()
        # OppStage = campaign[11].strip()
        OppFromDate = campaign[12].strip()
        OppToDate = campaign[13].strip()


        if OppType != "":
            oppwhere += 'and `U_TYPE` = "'+ OppType +'" '
            oppFlag = True;

        if OppSalePerson != "":
            oppwhere += 'and `SalesPerson` in("'+ OppSalePerson.replace(',','","') +'") '
            oppFlag = True;


        if OppFromDate != "" and OppToDate != "":
            oppwhere += 'and `StartDate` <= "'+ OppFromDate + '" and `ClosingDate` >= "'+  OppToDate +'" '
            oppFlag = True;

    if oppFlag:
        sqlSelectOpp = "SELECT DISTINCT ContactPerson, ContactPersonName,id FROM Opportunity_opportunity " + oppwhere
        print('----- opp data -----')
        print(sqlSelectOpp)
        mycursor.execute(sqlSelectOpp)
        allLead = mycursor.fetchall()
        # print(allLead)
        # print(len(allLead))
        for oppData in allLead:
            # print(oppData)
            ContactPersonId = oppData[0]
            sqlSelectBpEmp = "SELECT `id`,`FirstName`, `MobilePhone`, `E_Mail` FROM `BusinessPartner_bpemployee` WHERE `id` = "+ str(ContactPersonId)
            mycursor.execute(sqlSelectBpEmp)
            empData = mycursor.fetchall()
            for bpEmp in empData:
                # print('-----Emp data----')
                # print(data)
                userData = {
                    'Name': bpEmp[1],
                    'Phone': bpEmp[2],
                    'Email': bpEmp[3]
                }
                userList.append(userData)
            
    
    # ----------------------------------------
    # ----------- Customer data --------------
    # ----------------------------------------
    bpFlag = False

    if AllBPCheck == 1:
        bpwhere = ''
        bpFlag = True;
    else: 
        bpwhere = 'WHERE 1 '
        BPType = campaign[14].strip()
        BPSalePerson = campaign[15].strip()
        BPCountry = campaign[16].strip()
        BPState = campaign[17].strip()
        BPIndustry = campaign[18].strip()
        BPFromDate = campaign[19].strip()
        BPToDate = campaign[20].strip()

        BPCountryCode = campaign[27].strip()
        BPStateCode = campaign[28].strip()

        if BPType != "":
            bpwhere += 'and BusinessPartner_businesspartner.U_TYPE = "'+ BPType +'" '
            bpFlag = True

        if BPSalePerson != "":
            bpwhere += 'and BusinessPartner_businesspartner.SalesPersonCode in("'+ BPSalePerson.replace(',','","') +'") '
            bpFlag = True

        if BPFromDate != "" and BPToDate != "":
            bpwhere += 'and BusinessPartner_businesspartner.CreateDate <= "'+ BPFromDate + '" and BusinessPartner_businesspartner.CreateDate >= "'+  BPToDate +'" '
            bpFlag = True

        if BPIndustry != "":
            bpwhere += 'and BusinessPartner_businesspartner.Industry in("'+ BPIndustry.replace(',','","') +'") '
            bpFlag = True
        
        if BPCountry != "":
            bpwhere += 'and BusinessPartner_bpaddresses.Country = "'+ BPCountry +'" '
            bpFlag = True
        
        if BPState != "":
            bpwhere += 'and BusinessPartner_bpaddresses.State = "'+ BPState +'" '
            bpFlag = True

    if bpFlag:
        sqlSelectBP = "SELECT BusinessPartner_businesspartner.id FROM BusinessPartner_businesspartner JOIN BusinessPartner_bpaddresses ON BusinessPartner_businesspartner.id = BusinessPartner_bpaddresses.BPID " + bpwhere
        print('----- Customer data -----')
        print(sqlSelectBP)
        mycursor.execute(sqlSelectBP)
        allBp = mycursor.fetchall()
        # print(allBp)
        # print(len(allBp))
        for bp in allBp:
            # print(oppData)
            ContactPersonId = bp[0]
            sqlSelectBpEmp = "SELECT `id`,`FirstName`, `MobilePhone`, `E_Mail` FROM `BusinessPartner_bpemployee` WHERE `id` = "+ str(ContactPersonId)
            mycursor.execute(sqlSelectBpEmp)
            empData = mycursor.fetchall()
            for bpEmp in empData:
                # print('-----Emp data----')
                # print(data)
                userData = {
                    'Name': bpEmp[1],
                    'Phone': bpEmp[2],
                    'Email': bpEmp[3]
                }
                userList.append(userData)


    print('----All User----')
    # print(userList)
    for user in userList:
        Name = user['Name']
        Phone = user['Phone']
        Email = user['Email']

        if Phone != "" and Email != "":
            sqlSelectCamSet = "SELECT * FROM `Campaign_campaignsetmembers` WHERE `CampSetId_id` = '"+str(camSetId)+"' AND `Phone` = "+ str(Phone) +" And `Email` = '"+str(Email)+"'"
            # print(sqlSelectCamSet)
            mycursor.execute(sqlSelectCamSet)
            allRow = mycursor.fetchall()
            
            if not allRow:
                insertCamSetMember ="INSERT INTO `Campaign_campaignsetmembers`(`Name`, `Phone`, `Email`, `CampSetId_id`) VALUES ('"+str(Name)+"', '"+str(Phone)+"', '"+str(Email)+"', '"+str(camSetId)+"')"
                # print(insertCamSetMember)
                mycursor.execute(insertCamSetMember)
            mydb.commit() # this method will confirm and save changes in database
    
    userList = []