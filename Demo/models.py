from django.db import models  

class Demo(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=35, blank=True)
    company = models.CharField(max_length=100)
    timestamp = models.CharField(max_length=30)
