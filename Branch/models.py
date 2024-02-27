from django.db import models  

class Branch(models.Model):
    companyId = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=250, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    email = models.CharField(max_length=35, blank=True)
    state = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    pincode = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=100, blank=True)
    branch = models.CharField(max_length=100, blank=True)
    active = models.IntegerField(default=1)
    timestamp = models.CharField(max_length=30)
    
