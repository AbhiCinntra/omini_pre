import json
from django.shortcuts import render, redirect

from rest_framework.decorators import api_view   
from rest_framework.response import Response

from BusinessPartner.models import BPAddresses, BusinessPartner
from BusinessPartner.serializers import BPAddressesSerializer
from Company.models import Branch
from .serializers import *

from urllib.parse import unquote

from Invoice.models import *
from PurchaseInvoices.models import *

import requests, json

# Create your views here. 

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['GET'])
def all(request):
    try:
        entryObj = JournalEntries.objects.all().order_by('-id')[:20]
        result = showJournalEntries(entryObj)
        # entryJson = JournalEntriesSerializer(entryObj, many=True)
        return Response({"message":"successful","status":"200","data":result})
    except  Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def one(request):
    try:
        id = request.data['id']
        entryObj = JournalEntries.objects.filter(JdtNum = id)
        # entryObj = JournalEntries.objects.filter(pk = id)
        result = showJournalEntries(entryObj)
        # entryJson = JournalEntriesSerializer(entryObj, many=True)
        return Response({"message":"successful","status":"200","data":result})
    except  Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@api_view(['POST'])
def bp_wise(request):
    try:
        CardCode = request.data['CardCode']
        FromDate = request.data['FromDate']
        ToDate = request.data['ToDate']
        alldata = []
        totalDebit = 0
        totalCredit = 0
        if BusinessPartner.objects.filter(CardCode = CardCode).exists():
            bpObj = BusinessPartner.objects.filter(CardCode = CardCode).first()
            bpAddress = BPAddresses.objects.filter(BPCode = CardCode)
            bpAddressJson = BPAddressesSerializer(bpAddress, many=True)

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            #          Linked Vender
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            LinkedBusinessPartner = bpObj.LinkedBusinessPartner
            cardCodeList = [CardCode]
            cardCodeListIn = f"'{CardCode}'"
            if LinkedBusinessPartner != 'None':
                cardCodeList.append(LinkedBusinessPartner)
                cardCodeListIn = f"'{CardCode}', '{LinkedBusinessPartner}'"

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            #          Opening Balance
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            OpeningBalance = 0
            if str(FromDate) != "":
                # OB_Query = f"SELECT SUM(`Debit`-`Credit`) as OB, `id` FROM `JournalEntries_journalentrylines` WHERE `ShortName` in({cardCodeListIn}) AND  `ReferenceDate1` < '{FromDate}'"
                OB_Query = f"SELECT SUM(JeLine.Debit-JeLine.Credit) as OB, JeLine.id as id FROM `JournalEntries_journalentrylines` JeLine INNER JOIN JournalEntries_journalentries as JE ON JE.id = JeLine.JournalEntriesId WHERE JE.U_Cancel = 'N' AND JeLine.ShortName in({cardCodeListIn}) AND  JeLine.ReferenceDate1 < '{FromDate}'"
                # print('aaa',OB_Query)
                OB_Data = JournalEntryLines.objects.raw(OB_Query)
                if len(OB_Data) > 0:
                    if str(OB_Data[0].OB) != "None":
                        OpeningBalance = OB_Data[0].OB

            ClosingBalance = OpeningBalance
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            #          Journal Balance
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            entryObjs = []
            if str(FromDate) != "":
                entryObjs = JournalEntryLines.objects.filter(ShortName__in = cardCodeList, ReferenceDate1__gte = FromDate, ReferenceDate1__lte = ToDate).order_by("ReferenceDate1", "id")
            else:
                entryObjs = JournalEntryLines.objects.filter(ShortName__in = cardCodeList).order_by("ReferenceDate1", "id")
            BPLID = 0
            if len(entryObjs) > 0:
                for obj in entryObjs:
                    BPLID = obj.BPLID
                    
                    # journalEntries header details
                    entObj = JournalEntries.objects.get(pk = obj.JournalEntriesId)
                    Original = entObj.Original
                    JdtNum = entObj.JdtNum
                    DocType = entObj.DocType
                    JEID = entObj.id
                    OriginalJournal = entObj.OriginalJournal

                    if str(entObj.U_Cancel) == "N":
                        docId = 0
                        if OriginalJournal == "ttARInvoice":
                            if Invoice.objects.filter(DocEntry = Original).values("id", "DocEntry").exists():
                                tmpObj = Invoice.objects.filter(DocEntry = Original).values("id", "DocEntry").first()
                                # docId = tmpObj['id']
                                docId = tmpObj['DocEntry']
                        elif OriginalJournal == "ttReceipt":
                            if IncomingPayments.objects.filter(DocEntry = Original).values("id", "DocEntry").exists():
                                tmpObj = IncomingPayments.objects.filter(DocEntry = Original).values("id", "DocEntry").first()
                                # docId = tmpObj['id']
                                docId = tmpObj['DocEntry']
                        elif OriginalJournal == "ttARCredItnote":
                            if CreditNotes.objects.filter(DocEntry = Original).values("id", "DocEntry").exists():
                                tmpObj = CreditNotes.objects.filter(DocEntry = Original).values("id", "DocEntry").first()
                                # docId = tmpObj['id']
                                docId = tmpObj['DocEntry']
                        elif OriginalJournal == "ttAPInvoice":
                            if PurchaseInvoices.objects.filter(DocEntry = Original).values("id", "DocEntry").exists():
                                tmpObj = PurchaseInvoices.objects.filter(DocEntry = Original).values("id", "DocEntry").first()
                                # docId = tmpObj['id']
                                docId = tmpObj['DocEntry']
                        elif OriginalJournal == "ttVendorPayment":
                            if VendorPayments.objects.filter(DocEntry = Original).values("id", "DocEntry").exists():
                                tmpObj = VendorPayments.objects.filter(DocEntry = Original).values("id", "DocEntry").first()
                                # docId = tmpObj['id']
                                docId = tmpObj['DocEntry']
                        elif OriginalJournal == "ttAPCreditNote":
                            if PurchaseCreditNotes.objects.filter(DocEntry = Original).values("id", "DocEntry").exists():
                                tmpObj = PurchaseCreditNotes.objects.filter(DocEntry = Original).values("id", "DocEntry").first()
                                # docId = tmpObj['id']
                                docId = tmpObj['DocEntry']
                                
                        # print('ssssa',float(obj.Debit))
                        totalDebit = totalDebit + float(obj.Debit)
                        totalCredit = totalCredit + float(obj.Credit)
                        ClosingBalance = ClosingBalance + float(obj.Debit) - float(obj.Credit)
                        BPLName = ""
                        Address = ""
                        State = ""
                        TaxIdNum = ""
                        FederalTaxID = ""
                        if Branch.objects.filter(BPLId=BPLID).exists():
                            branch_obj = Branch.objects.filter(BPLId=BPLID).first()
                            BPLName = branch_obj.BPLName
                            Address = unquote(branch_obj.Address)
                            State = branch_obj.State
                            TaxIdNum = branch_obj.TaxIdNum
                            FederalTaxID = branch_obj.FederalTaxID
                        entry = {
                            "id": JdtNum,
                            "JdtNum": JdtNum,
                            "DocType": DocType,
                            "Original": Original,
                            "OriginalJournal": OriginalJournal,
                            "DocId": docId,
                            "Debit": obj.Debit,
                            "Credit": obj.Credit,
                            "Balance": round(ClosingBalance, 2),
                            "DueDate": obj.ReferenceDate1,
                            "Reference1": obj.Reference1,
                            "EntryType": unquote(obj.LineMemo),
                            "AccountName": obj.AccountName,
                            "Reference2": obj.Reference2,
                            "BPLName": BPLName,
                            "Address": Address,
                            "State": State,
                            "TaxIdNum": TaxIdNum,
                            "Branch_GSTIN": FederalTaxID,
                        }
                        alldata.append(entry)
                    # endif
                # endfor
            # endif
                
            contaxt = {
                "CardCode": CardCode,
                "CardName": unquote(bpObj.CardName),
                "OpeningBalance": round(OpeningBalance, 2),
                "ClosingBalance": round(ClosingBalance, 2),
                "TotalDebit": totalDebit,
                "TotalCredit": totalCredit,
                "BPAddresses": bpAddressJson.data,
                # "BPLName": BPLName,
                # "Address": Address,
                # "State": State,
                # "TaxIdNum": TaxIdNum,
                # "Branch_GSTIN": FederalTaxID,
                "JournalEntryLines":alldata
            }
            return Response({"message":"successful","status":"200","data":[contaxt]})
        else:
            return Response({"message":"Invalid CardCode?","status":"201","data":[]})
    except  Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 
# 
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def showJournalEntries(objs):
    allEntries = []
    for obj in objs:
        entryJson = JournalEntriesSerializer(obj, many=False)
        finalObj = json.loads(json.dumps(entryJson.data))

        BPLID = 0
        if JournalEntryLines.objects.filter(JournalEntriesId = obj.id).exists():
            linesObj = JournalEntryLines.objects.filter(JournalEntriesId = obj.id).order_by('-id')
            BPLID = linesObj[0].BPLID
            linesJson = JournalEntryLinesSerializer(linesObj, many=True)
            finalObj['JournalEntryLines'] = linesJson.data
        else:
            finalObj['JournalEntryLines'] = []
        
        ################################addedd################################
        if Branch.objects.filter(BPLId=BPLID).exists():
            branch_obj = Branch.objects.filter(BPLId=BPLID).first()
            finalObj["BPLName"] = branch_obj.BPLName
            finalObj["Address"] = unquote(branch_obj.Address)
            finalObj["State"] = branch_obj.State
            finalObj["TaxIdNum"] = branch_obj.TaxIdNum
            finalObj["Branch_GSTIN"] = branch_obj.FederalTaxID
        else:
            finalObj["BPLName"] = ""
            finalObj["Address"] = ""
            finalObj["State"] = ""
            finalObj["TaxIdNum"] = ""
            finalObj["Branch_GSTIN"] = ""
        ################################addedd################################

        allEntries.append(finalObj)
    return allEntries


from django.db import connection

@api_view(['GET'])
def sync_reconcilation(request):
    try:
        startDate = '2021-03-31'
        endDate = '2024-04-30'
        sapUrl = f"http://65.2.148.88:8000/Ledure/General/Reconcilation_New.xsjs?DBName=RG_Industries_Live_&From={startDate}&ToDate={endDate}"
        print(sapUrl)
        sacAPIRsponse = requests.get(sapUrl, verify=False)
        rsponseJson = json.loads(sacAPIRsponse.text)
        # print(rsponseJson)
        rsponseData = rsponseJson['value']
        # print("len", len(rsponseData))
        # return True

        allQuery = ""
        if len(rsponseData) != 0:
            for obj in rsponseData:
                print(obj['TransId'])
                Line_ID  = obj['Line_ID']
                BPName   = obj['BPName']
                TransId  = obj['TransId']
                # Debit    = obj['Debit']
                # Credit   = obj['Credit']
                ReconSum = obj['ReconSum']

                updateJE = f"UPDATE `JournalEntries_journalentrylines` INNER JOIN JournalEntries_journalentries ON JournalEntries_journalentries.id = JournalEntries_journalentrylines.JournalEntriesId  SET `ReconSum` = '{ReconSum}' WHERE JournalEntries_journalentries.JdtNum = {TransId} AND JournalEntries_journalentrylines.Line_ID = 0 AND JournalEntries_journalentrylines.ShortName = '{BPName}';"
                # print(updateJE)
                # allQuery = allQuery + updateJE
                with connection.cursor() as cursor:
                    cursor.execute(updateJE)
                    connection.commit()
                
                # obj = JournalEntryLines.objects.raw(updateJE)
                # print(obj)
        else:
            print(rsponseData)
        
        return Response({"message": "successful", "status": "200", "data": rsponseData})
    except  Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})



