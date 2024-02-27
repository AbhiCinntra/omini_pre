from django.db import models  

class Countries(models.Model):
    Code = models.CharField(max_length=5, blank=True)
    Name = models.CharField(max_length=100, blank=True)
    Capital = models.CharField(max_length=100, blank=True)

class States(models.Model):
    Code = models.CharField(max_length=5, blank=True)
    Country = models.CharField(max_length=4, blank=True)
    Name = models.CharField(max_length=50, blank=True)
