from django.db import models  

class Employee(models.Model):
    companyID       = models.CharField(max_length=100, blank=True)
    SalesEmployeeCode = models.CharField(max_length=100, blank=True, unique=True)
    SalesEmployeeName = models.CharField(max_length=100, blank=True)
    EmployeeID      = models.CharField(max_length=100, blank=True)
    userName        = models.CharField(max_length=100, blank=True)
    password        = models.CharField(max_length=100, blank=True)
    firstName       = models.CharField(max_length=100, blank=True)
    middleName      = models.CharField(max_length=100, blank=True)
    lastName        = models.CharField(max_length=100, blank=True)
    Email           = models.CharField(max_length=100, blank=True)
    Mobile          = models.CharField(max_length=100, blank=True)
    role            = models.CharField(max_length=100, blank=True)
    position        = models.CharField(max_length=100, blank=True)
    branch          = models.CharField(max_length=100, blank=True)
    Active          = models.CharField(max_length=20, blank=True)
    passwordUpdatedOn= models.CharField(max_length=30, blank=True)
    lastLoginOn     = models.CharField(max_length=30, blank=True)
    logedIn         = models.CharField(max_length=20, blank=True)
    reportingTo     = models.CharField(max_length=20, blank=True)
    FCM             = models.CharField(max_length=250, blank=True)
    timestamp       = models.CharField(max_length=30, blank=True)
    unit            = models.CharField(max_length=250, blank=True)
    # new keys
    CompName        = models.CharField(max_length=250, blank=True, default="")
    Website         = models.CharField(max_length=250, blank=True, default="")
    Address         = models.CharField(max_length=250, blank=True, default="")
    GST             = models.CharField(max_length=250, blank=True, default="")
    ACCNo           = models.CharField(max_length=250, blank=True, default="")
    Ifsc            = models.CharField(max_length=250, blank=True, default="")
    U_LAT           = models.CharField(max_length=250, blank=True, default="")
    U_LONG          = models.CharField(max_length=250, blank=True, default="")
    LocationSharing = models.CharField(max_length=250, blank=True, default="0")
    Zone            = models.TextField(blank=True, default="")
    
class Targetyr(models.Model):
    Department = models.CharField(max_length=50, blank=True)
    StartYear = models.IntegerField(default=0)
    EndYear = models.IntegerField(default=0)
    SalesPersonCode = models.ForeignKey(Employee, to_field="SalesEmployeeCode", on_delete = models.CASCADE, blank=True, null=True)
    reportingTo = models.ForeignKey(Employee, to_field="SalesEmployeeCode", related_name="reportingToTargetyr", on_delete = models.CASCADE, blank=True, null=True)    
    YearTarget = models.BigIntegerField(default=0)
    status = models.IntegerField(default=0)
    CreatedDate = models.CharField(max_length=20, blank=True)
    UpdatedDate = models.CharField(max_length=20, blank=True)

    
class Targetqty(models.Model):
    SalesPersonCode = models.ForeignKey(Employee, to_field="SalesEmployeeCode", on_delete = models.CASCADE, blank=True, null=True)
    reportingTo = models.ForeignKey(Employee, to_field="SalesEmployeeCode", related_name="reportingToTargetqty", on_delete = models.CASCADE, blank=True, null=True)
    
    YearTarget = models.ForeignKey(Targetyr, on_delete=models.CASCADE)
    q1 = models.BigIntegerField(default=0)
    q2 = models.BigIntegerField(default=0)
    q3 = models.BigIntegerField(default=0)
    q4 = models.BigIntegerField(default=0)
    status = models.IntegerField(default=0)
    CreatedDate = models.CharField(max_length=20, blank=True)
    UpdatedDate = models.CharField(max_length=20, blank=True)
    
class Target(models.Model):
    amount = models.FloatField(default=0)
    monthYear = models.CharField(max_length=50, blank=True)
    qtr = models.IntegerField(default=0)
    YearTarget = models.ForeignKey(Targetyr, related_name="YearTargetTarget", on_delete=models.CASCADE)
    SalesPersonCode = models.ForeignKey(Employee, to_field="SalesEmployeeCode", on_delete = models.CASCADE, blank=True, null=True)
    sale = models.FloatField(default=0)
    sale_diff = models.FloatField(default=0)
    CreatedDate = models.CharField(max_length=20, blank=True)
    UpdatedDate = models.CharField(max_length=20, blank=True)     

class Roles(models.Model):
    Name = models.CharField(max_length=255, blank=True)

class Units(models.Model):
    Code = models.CharField(max_length=255, blank=True)
    Name = models.CharField(max_length=255, blank=True)
