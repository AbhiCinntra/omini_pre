from django.db import models  
class Appsetting(models.Model):
    Key = models.CharField(max_length=50, blank=True)
    Data = models.CharField(max_length=500, blank=True)
