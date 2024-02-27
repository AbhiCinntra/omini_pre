from django.db import models  
from enum import Enum

from Employee.models import Employee

ftype = (
    ("Weekly", "Weekly"),
    ("Daily", "Daily"),
    ("Monthly", "Monthly"),
    ("Once", "Once"),
    ("Undefined", "Undefined")
)

mtype = (
    ("Email", "Email"),
    ("SMS", "SMS"),
    ("WhatsApp", "WhatsApp"),
    ("Undefined", "Undefined")
)

qrtype = (
    ("High", "High"),
    ("Low", "Low"),
    ("Medium", "Medium"),
    ("Poor", "Poor"),
    ("Average", "Average"),
    ("Undefined", "Undefined")
)
    
class CampaignSet(models.Model):
    CampaignSetName = models.CharField(max_length=100, blank=True)
    CampaignSetOwner = models.ForeignKey(Employee, to_field="SalesEmployeeCode", on_delete=models.CASCADE, related_name="CampaignSetOwner")
    CampaignAccess = models.CharField(max_length=250, blank=True)
    Description = models.CharField(max_length=250, blank=True)
    
    LeadSource = models.CharField(max_length=1000, blank=True)
    LeadPriority = models.CharField(max_length=250, blank=True)
    LeadStatus = models.CharField(max_length=250, blank=True)    
    LeadFromDate = models.CharField(max_length=100, blank=True)
    LeadToDate = models.CharField(max_length=100, blank=True)

    #OppDivision = models.CharField(max_length=1000, blank=True)
    OppType = models.CharField(max_length=250, blank=True)
    OppSalePerson = models.CharField(max_length=250, blank=True)    
    OppStage = models.CharField(max_length=250, blank=True)
    OppFromDate = models.CharField(max_length=100, blank=True)
    OppToDate = models.CharField(max_length=100, blank=True)
    
    BPType = models.CharField(max_length=250, blank=True)
    BPSalePerson = models.CharField(max_length=250, blank=True)        
    BPCountry = models.CharField(max_length=250, blank=True)
    BPCountryCode = models.CharField(max_length=1000, blank=True)
    BPState = models.CharField(max_length=1000, blank=True)
    BPStateCode = models.CharField(max_length=1000, blank=True)
    BPIndustry = models.TextField(max_length=1000, blank=True)
    BPFromDate = models.CharField(max_length=100, blank=True)
    BPToDate = models.CharField(max_length=100, blank=True)
    
    MemberList = models.CharField(max_length=250, blank=True)
    Status = models.IntegerField(default=1)
    CreateBy = models.ForeignKey(Employee, to_field="SalesEmployeeCode", on_delete=models.CASCADE, related_name="CreateBy")
    CreateDate = models.CharField(max_length=100, blank=True)
    CreateTime = models.CharField(max_length=100, blank=True)

    AllLead = models.IntegerField(default=0)
    AllOpp = models.IntegerField(default=0)
    AllBP = models.IntegerField(default=0)

class Campaign(models.Model):
    CampaignSetId = models.ForeignKey(CampaignSet, on_delete=models.CASCADE) 
    CampaignName = models.CharField(max_length=100, blank=True)
    CampaignOwner = models.ForeignKey(Employee, to_field="SalesEmployeeCode", on_delete=models.CASCADE, related_name="CampaignOwner")    
    StartDate = models.CharField(max_length=100, blank=True)
    EndDate = models.CharField(max_length=100, blank=True)
    Type = models.CharField(max_length = 255, default = 'Undefined') #choices = mtype, for fix choices
    Frequency = models.CharField(max_length = 255, default = 'Undefined') #choices = ftype, for fix choices
    WeekDay = models.CharField(max_length=255, blank=True, default="")
    MonthlyDate = models.TextField(max_length=255, blank=True)
    Message = models.TextField(max_length=1000, blank=True)
    
    QualityResponse = models.CharField(max_length = 255, default = 'Undefined') #choices = qrtype, for fix choices
    
    Sent = models.IntegerField(default=0)
    Delivered = models.IntegerField(default=0)
    Opened = models.IntegerField(default=0)
    Responded = models.IntegerField(default=0)
    Status = models.IntegerField(default=1)
    CreateDate = models.CharField(max_length=100, blank=True)
    CreateTime = models.CharField(max_length=100, blank=True)
    Subject = models.CharField(max_length=100, blank=True)
    RunTime = models.CharField(max_length=15, blank=True)
    Attachments = models.TextField(max_length=1000, blank=True)



class CampaignSetMembers(models.Model):
    CampSetId = models.ForeignKey(CampaignSet, on_delete=models.CASCADE, null= True)
    Name = models.CharField(max_length=100, blank=True)
    Phone = models.CharField(max_length=100, blank=True)
    Email = models.CharField(max_length=100, blank=True)

