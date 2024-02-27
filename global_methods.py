from Employee.models import *
from Order.models import Order, DocumentLines as OrderDocumentLines

from datetime import date, datetime, timedelta

import re
import sys, os
import pytz
import pandas as pd

# get the standard UTC time
UTC = pytz.utc
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#@api_view(["POST"])
def tree(SalesEmployeeCode):
        emp_obj =  Employee.objects.filter(SalesEmployeeCode=SalesEmployeeCode)
        print(emp_obj[0].role)
        i=1
        while int(emp_obj[0].reportingTo) !=0:
            emp_obj = Employee.objects.filter(SalesEmployeeCode=emp_obj[0].reportingTo)
            if emp_obj[0].role == 'admin':
                i=i+0
            else:
                i=i+1
        print(str(i))
        return str(i)
    #return Response({"message":"Success", "status":200, "data":[{"Level":str(i)}]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def employeeViewAccess(SalesEmployeeCode):
    allSalesEmployeeCode=[]
    emp_obj =  Employee.objects.get(SalesEmployeeCode=SalesEmployeeCode)
    EmployeeRole = str(emp_obj.role).lower()
    unit = emp_obj.unit
    print("Employee Role: ", EmployeeRole)
    if EmployeeRole == 'admin':
        print('in 1st condition', EmployeeRole)
        emps = Employee.objects.filter(Active = "tYES").exclude(role = 'Commission Agent')
        for emp in emps:
            allSalesEmployeeCode.append(emp.SalesEmployeeCode)

    elif EmployeeRole == 'director' or EmployeeRole == 'cro':
        print('in 2ed condition', EmployeeRole)
        emps = Employee.objects.filter(Active = "tYES").exclude(role = 'Commission Agent')
        allSalesEmployeeCode=[SalesEmployeeCode]
        for emp in emps:
            allSalesEmployeeCode.append(emp.SalesEmployeeCode)

    elif EmployeeRole == 'unit head':
        print('in 3rd condition', EmployeeRole)
        allSalesEmployeeCode = getAllReportingToIds(SalesEmployeeCode)
        # emps = Employee.objects.filter(reportingTo=SalesEmployeeCode, Active = "tYES", unit = unit).exclude(role = 'Commission Agent')
        # allSalesEmployeeCode=[SalesEmployeeCode]
        # for emp in emps:
        #     allSalesEmployeeCode.append(emp.SalesEmployeeCode)

    elif EmployeeRole == 'area sales manager':
        print('in 4th condition', EmployeeRole)
        allSalesEmployeeCode = getAllReportingToIds(SalesEmployeeCode)
        # emps = Employee.objects.filter(reportingTo=SalesEmployeeCode, Active = "tYES").exclude(role = 'Commission Agent')
        # for emp in emps:
        #     allSalesEmployeeCode.append(emp.SalesEmployeeCode)
    else:
        print('in else condition', EmployeeRole)
        allSalesEmployeeCode=[SalesEmployeeCode]
    return allSalesEmployeeCode

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>> list salesperson code tree wise >>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# function to get all reporting reporting person SalesEmployeeCode
def getAllReportingToIds(EmpCode):
    data = []
    def recrusiveMethod(id):
        # print('recursive call', id)
        data.append(id)
        emp_obj =  Employee.objects.filter(reportingTo=id)
        for obj in emp_obj:
            recrusiveMethod(int(obj.SalesEmployeeCode))
        # endfor
    #endfun
    recrusiveMethod(int(EmpCode))
    return data
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# function to get all reporting reporting person id
def getAllReportingToUserId(id):
    data = []
    empObj = Employee.objects.get(pk = id)
    def recrusiveMethod(obj):
        # print('recursive call', obj.id)
        data.append(obj.id)
        emp_obj =  Employee.objects.filter(reportingTo=obj.SalesEmployeeCode)
        for obj in emp_obj:
            recrusiveMethod(obj)
        # endfor
    #endfun
    recrusiveMethod(empObj)
    return data

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>> find Todays total quntity of item sales by unit >>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# by unit
def findTodaysUnitSales(Unit):
    Unit = str(Unit).lower()
    totalSalesInKG = 0
    currentDate = date.today()
    if Order.objects.filter(Unit__icontains = Unit, CreateDate = str(currentDate), ApprovalStatus = 'Approved').exists():

        # get all order ites belongs to given unit
        orderIds = list(Order.objects.filter(Unit__icontains = Unit, CreateDate = str(currentDate), ApprovalStatus = 'Approved').values_list('id', flat=True))
        
        # get all UnitWeight by order id
        orderItems = OrderDocumentLines.objects.filter(OrderID__in = orderIds).values('UnitWeight','Quantity')
        
        # sum of all UnitWeight
        for i in orderItems:
            if (str(i['UnitWeight']).strip()) != '':
                # print("Weight: ", i['UnitWeight'], "Qty: ", i['Quantity'])
                totalSalesInKG = (totalSalesInKG + (float(i['UnitWeight']) * int(i['Quantity'])))
            # endif
        # endfor
    # endif
    return totalSalesInKG
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# by BusinessPartner
def findTodaysUnitSalesByBP(Unit, CardCode):
    Unit = str(Unit).lower()
    totalSalesInKG = 0
    currentDate = date.today()
    if Order.objects.filter(Unit__icontains = Unit, CreateDate = str(currentDate), ApprovalStatus = 'Approved', CardCode = CardCode).exists():

        # get all order ites belongs to given unit
        orderIds = list(Order.objects.filter(Unit__icontains = Unit, CreateDate = str(currentDate), ApprovalStatus = 'Approved', CardCode = CardCode).values_list('id', flat=True))
        
        # get all UnitWeight by order id
        orderItems = OrderDocumentLines.objects.filter(OrderID__in = orderIds).values('UnitWeight','Quantity')
        
        # sum of all UnitWeight
        for i in orderItems:
            if (str(i['UnitWeight']).strip()) != '':
                # print("Weight: ", i['UnitWeight'], "Qty: ", i['Quantity'])
                totalSalesInKG = (totalSalesInKG + (float(i['UnitWeight']) * int(i['Quantity'])))
            # endif
        # endfor
    # endif
    return totalSalesInKG

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def get_mm_yy(txt):
  mm = int(re.findall("-([0-9]+)-", txt)[0].strip("-"))
  yy = int(re.findall("([0-9]{4})", txt)[0][2:4])

  month_arr = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
  return str(month_arr[mm-1])+" "+str(yy)

# def groupby(data, field_list, gpby, sumby):
# 	#MonthSalesList = pd.DataFrame(data, columns=['DocTotal', 'Month'])
# 	df = pd.DataFrame(data, columns=field_list)
# 	DataGroup = df.groupby(gpby, as_index=False)[sumby].sum()
# 	DataGroupList = DataGroup.to_dict('records')
# 	return DataGroupList
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def groupby(data, field_list, gpby, sumby):
    print("field_list", field_list)
    
    df = pd.DataFrame(data, columns=field_list)
    
    # Convert 'Month' column to datetime
    # df['CreateDate'] = pd.to_datetime(df['CreateDate'], format='%Y-%m-%d')

    # Sort DataFrame by 'Month'
    df = df.sort_values(by=gpby)

    # Group by and sum
    DataGroup = df.groupby(gpby, as_index=False)[sumby].sum()
    print("DataGroup", DataGroup)
    
    # Convert to a list of dictionaries
    DataGroupList = DataGroup.to_dict('records')
    
    return DataGroupList


# get zone by salespersoncode
def getZoneByEmployee(SalesPersonCode):
    zoneList = []
    if Employee.objects.filter(SalesEmployeeCode = SalesPersonCode).exists():
        empObj = Employee.objects.get(SalesEmployeeCode = SalesPersonCode)
        tmpZone = empObj.Zone
        if str(tmpZone) != "":
            zoneList = tmpZone.split(",")
        
        return zoneList
    else:
        return zoneList
    
from django.conf import settings
import mysql.connector

def getDBConnection():
    mydb = mysql.connector.connect(
        host=settings.DATABASES['default']['HOST'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        database=settings.DATABASES['default']['NAME']
    )
    mycursor = mydb.cursor(buffered=True, dictionary=True)
    return mycursor