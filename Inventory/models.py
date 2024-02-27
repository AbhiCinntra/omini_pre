from django.db import models  

class Product(models.Model):
    ItemName = models.CharField(max_length=30, blank=True)
    ItemCode = models.CharField(max_length=30, blank=True)
    Description = models.CharField(max_length=30, blank=True)
    UnitPrice = models.FloatField(default=0, blank=True)
    Currency = models.CharField(max_length=30, blank=True)
    HSN = models.CharField(max_length=30, blank=True)
    Tax = models.FloatField(default=0, blank=True)
    Discount = models.FloatField(default=0, blank=True)
    Status = models.IntegerField(default=0, blank=True)      
    CreateDate = models.CharField(max_length=30, blank=True)
    CreateTime = models.CharField(max_length=30, blank=True)
    UpdateDate = models.CharField(max_length=30, blank=True)
    UpdateTime = models.CharField(max_length=30, blank=True)

class Warehouse(models.Model):
    Name = models.CharField(max_length=30, blank=True)
    Address = models.CharField(max_length=30, blank=True)
    City = models.CharField(max_length=30, blank=True)
    State = models.CharField(max_length=30, blank=True)
    Pin = models.IntegerField(max_length=30, blank=True)
    Country = models.CharField(max_length=0, blank=True)
    Status = models.IntegerField(default=0, blank=True)
    CreatedDate = models.CharField(max_length=30, blank=True)
    CreatedDate = models.CharField(max_length=30, blank=True)

class Inventory(models.Model):
    ItemID = models.IntegerField(max_length=30, blank=True)
    WarehouseID = models.CharField(max_length=30, blank=True)
    Add = models.IntegerField(default=0, blank=True)
    Remove = models.IntegerField(default=0, blank=True)
    Inventory = models.IntegerField(default=0, blank=True)
    CreatedDate = models.CharField(max_length=30, blank=True)
    CreatedTime = models.CharField(max_length=30, blank=True)
