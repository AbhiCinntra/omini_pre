from django.db import models

# Create your models here.
class Warehouse(models.Model):
    BusinessPlaceID = models.CharField(max_length=30, blank=True)
    Location        = models.CharField(max_length=30, blank=True)
    WarehouseCode   = models.CharField(max_length=50, blank=True)
    WarehouseName   = models.CharField(max_length=250, blank=True)
    Block           = models.CharField(max_length=250, blank=True)
    State           = models.CharField(max_length=250, blank=True)
    City            = models.CharField(max_length=200, blank=True)
    Country         = models.CharField(max_length=100, blank=True)
    County          = models.CharField(max_length=100, blank=True)
    Street          = models.CharField(max_length=250, blank=True)
    ZipCode         = models.CharField(max_length=50, blank=True)
    Inactive        = models.CharField(max_length=30, blank=True)
    CreatedDate     = models.CharField(max_length=30, blank=True)
    UpdatedDate     = models.CharField(max_length=30, blank=True)
    