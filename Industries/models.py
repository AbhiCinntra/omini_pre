from django.db import models  

class Industries(models.Model):
    IndustryDescription = models.CharField(max_length=200, blank=True)
    IndustryName = models.CharField(max_length=100, blank=True)
    IndustryCode = models.CharField(max_length=5, blank=True)
