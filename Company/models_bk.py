from django.db import models  

class Company(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=250, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    email = models.CharField(max_length=35, blank=True)
    state = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    pincode = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=100, blank=True)
    
    natureOfIndustry = models.CharField(max_length=100, blank=True)
    ERP = models.CharField(max_length=100, blank=True)
    serverIP = models.CharField(max_length=100, blank=True)
    port = models.IntegerField(default=0)
    user = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=100, blank=True)

    license_limit = models.IntegerField(default=1)
    active = models.IntegerField(default=1)
    timestamp = models.CharField(max_length=30)


class Branch(models.Model):
    BPLId      = models.CharField(max_length=5, blank=False)
    BPLName    = models.CharField(max_length=250, blank=True)
    Address    = models.CharField(max_length=250, blank=True)
    MainBPL    = models.CharField(max_length=5, blank=True)
    Disabled   = models.CharField(max_length=5, blank=True)
    UserSign2  = models.CharField(max_length=5, blank=True)
    UpdateDate = models.CharField(max_length=50, blank=True)
    DflWhs     = models.CharField(max_length=50, blank=True)
    TaxIdNum   = models.CharField(max_length=100, blank=True)
    StreetNo   = models.CharField(max_length=100, blank=True)
    Building   = models.CharField(max_length=100, blank=True)
    ZipCode    = models.CharField(max_length=100, blank=True)
    City       = models.CharField(max_length=100, blank=True)
    State      = models.CharField(max_length=100, blank=True)
    Country    = models.CharField(max_length=100, blank=True)
    Series     = models.CharField(max_length=50, blank=True)
