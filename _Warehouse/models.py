from django.db import models

invtype = (
    ("Inventory", "Inventory"),    
    ("Order", "Order"),    
    ("Transfer", "Transfer"),
    ("Other", "Other"),
    ("Undefined", "Undefined"),
)

  
class Warehouse(models.Model):
    Name = models.CharField(max_length=30, blank=True)
    Address = models.CharField(max_length=30, blank=True)
    City = models.CharField(max_length=30, blank=True)
    State = models.CharField(max_length=30, blank=True)
    Pin = models.IntegerField(default=0, blank=True)
    Country = models.CharField(max_length=50, blank=True)
    Status = models.IntegerField(default=0, blank=True)
    CreatedDate = models.CharField(max_length=30, blank=True)
    CreatedTime = models.CharField(max_length=30, blank=True)
    UpdatedDate = models.CharField(max_length=30, blank=True)
    UpdatedTime = models.CharField(max_length=30, blank=True)

class Inventory(models.Model):
    ItemCode = models.CharField(max_length=50, blank=False)
    WarehouseID = models.CharField(max_length=30, blank=True)
    Add = models.IntegerField(default=0, blank=True)
    Remove = models.IntegerField(default=0, blank=True)
    Inventory = models.IntegerField(default=0, blank=True)
    Type = models.CharField(max_length = 20, choices = invtype, default = 'Undefined')
    Emp = models.IntegerField(default=0, blank=True)
    Remark = models.CharField(max_length=30, blank=True)
    CreatedDate = models.CharField(max_length=30, blank=True)
    CreatedTime = models.CharField(max_length=30, blank=True)
