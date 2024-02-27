from django.db import models  
from Employee.models import *
class Lead(models.Model):
    date = models.CharField(max_length=60, blank=True)
    location = models.CharField(max_length=100, blank=True)
    companyName = models.CharField(max_length=100, blank=True)
    numOfEmployee = models.IntegerField(default='0')
    turnover = models.CharField(max_length=100, blank=True)
    source = models.CharField(max_length=100, blank=True)
    contactPerson = models.CharField(max_length=50, blank=True)
    designation = models.CharField(max_length=50, blank=True)
    phoneNumber = models.CharField(max_length=20, blank=True)
    message = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=50, blank=True)
    leadType = models.CharField(max_length=50, blank=True)
    productInterest = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=100, blank=True)
    assignedTo = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='assignedTo')
    employeeId = models.ForeignKey(Employee, on_delete=models.CASCADE)
    #employeeId = models.IntegerField(default='0')
    junk = models.IntegerField(default='0')
    timestamp = models.CharField(max_length=60, blank=True)
    # new keys
    projectAmount = models.CharField(max_length=10, blank=True, default="")
    customerType  = models.CharField(max_length=100, blank=True, default="") # 
    stages        = models.CharField(max_length=100, blank=True, default="New") # new, qualified, disqualified

class Chatter(models.Model):
    Message = models.CharField(max_length=250, blank=True)
    Lead_Id = models.CharField(max_length=10, blank=True)
    Emp_Id = models.CharField(max_length=10, blank=True)
    Emp_Name = models.CharField(max_length=50, blank=True)
    UpdateDate = models.CharField(max_length=100, blank=True)
    UpdateTime = models.CharField(max_length=100, blank=True)

class Type(models.Model):
    Name = models.CharField(max_length=50, blank=True)
    CreatedDate = models.CharField(max_length=50, blank=True)
    CreatedTime = models.CharField(max_length=50, blank=True)

class Source(models.Model):
    Name = models.CharField(max_length=50, blank=True)
    CreatedDate = models.CharField(max_length=50, blank=True)
    CreatedTime = models.CharField(max_length=50, blank=True)

#added by millan on 06-10-2022
class LeadAttachment(models.Model):
    File = models.CharField(max_length=150, blank=True)
    CreateDate = models.CharField(max_length=100, blank=True)
    CreateTime = models.CharField(max_length=100, blank=True)
    UpdateDate = models.CharField(max_length=100, blank=True)
    UpdateTime = models.CharField(max_length=100, blank=True)
    LeadId = models.IntegerField(default=0)
    CreatedBy = models.IntegerField(default=0)
    UpdatedBy = models.IntegerField(default=0)
    Size = models.CharField(max_length=100, blank=True)
    
#added by millan on 13-10-2022
class Notes(models.Model):
    LeadId = models.IntegerField(default=0)
    Title = models.CharField(max_length=255, blank=True)
    Remarks = models.TextField(blank=True)
    CreateDate = models.CharField(max_length=100, blank=True)
    CreateTime = models.CharField(max_length=100, blank=True)
    CreatedBy = models.IntegerField(default=0)