from django.db import models  
from enum import Enum

stype = (
    ("Lead", "Lead"),
    ("Opportunity", "Opportunity"),
    ("Quotation", "Quotation"),
    ("Order", "Order"),
    ("Undefined", "Undefined"),
)
atype = (
    ("Task", "Task"),    
    ("Event", "Event"),
    ("Followup", "Followup"),
    ("Undefined", "Undefined"),
)
    
class Activity(models.Model):
    SourceID = models.IntegerField(default=0)
    Subject = models.CharField(max_length=100, blank=True)
    Comment = models.CharField(max_length=250, blank=True)
    Name = models.CharField(max_length=100, blank=True)
    RelatedTo = models.CharField(max_length=100, blank=True)
    Emp = models.IntegerField(default=0)
    Title = models.CharField(max_length=100, blank=True)
    Description = models.TextField(max_length=1000, blank=True)
    From = models.CharField(max_length=10, blank=True)
    To = models.CharField(max_length=10, blank=True)
    Time = models.CharField(max_length=10, blank=True)
    Allday = models.CharField(max_length=200, blank=True)
    Location = models.CharField(max_length=100, blank=True)
    Host = models.CharField(max_length=100, blank=True)
    Participants = models.CharField(max_length=250, blank=True)
    Document = models.CharField(max_length=250, blank=True)
    Repeated = models.CharField(max_length=100, blank=True)
    Priority = models.CharField(max_length=100, blank=True)
    ProgressStatus = models.CharField(max_length=100, blank=True)
    #SourceType = models.CharField(max_length=100, blank=True)
    leadType = models.CharField(max_length=50, blank=True, default="")    
    Type = models.CharField(max_length = 20, choices = atype, default = 'Undefined')
    SourceType = models.CharField(max_length = 20, choices = stype, default = 'Undefined')
    Status = models.IntegerField(default=0)
    CreateDate = models.CharField(max_length=100, blank=True)
    CreateTime = models.CharField(max_length=100, blank=True)


class Maps(models.Model):
    Lat            = models.CharField(max_length=100, blank=True)
    Long           = models.CharField(max_length=100, blank=True)
    Address        = models.CharField(max_length=100, blank=True)
    Emp_Id         = models.CharField(max_length=10, blank=True)
    Emp_Name       = models.CharField(max_length=50, blank=True)
    UpdateDate     = models.CharField(max_length=100, blank=True)
    UpdateTime     = models.CharField(max_length=100, blank=True)
    type           = models.CharField(max_length=100, blank=True)
    shape          = models.CharField(max_length=100, blank=True)
    remark         = models.CharField(max_length=500, blank=True)
    ResourceId     = models.CharField(max_length=100, blank=True)
    SourceType     = models.CharField(max_length=100, blank=True)
    ContactPerson  = models.CharField(max_length=100, blank=True)
    Attach         = models.CharField(max_length=100, blank=True)
    Attach         = models.CharField(max_length=100, blank=True)
    # new keys
    ExpenseCost    = models.CharField(max_length=100, blank=True)
    ExpenseDistance= models.CharField(max_length=100, blank=True)
    ExpenseType    = models.CharField(max_length=100, blank=True)
    ExpenseAttach  = models.CharField(max_length=100, blank=True)
    ExpenseRemark  = models.CharField(max_length=100, blank=True)

class Chatter(models.Model):
    Message = models.CharField(max_length=250, blank=True)
    SourceID = models.CharField(max_length=10, blank=True)
    SourceType = models.CharField(max_length = 20, choices = stype, default = 'Undefined')
    Emp = models.CharField(max_length=10, blank=True)
    Emp_Name = models.CharField(max_length=50, blank=True)
    Mode = models.CharField(max_length = 50, blank=True)
    UpdateDate = models.CharField(max_length=100, blank=True)
    UpdateTime = models.CharField(max_length=100, blank=True)

