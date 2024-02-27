from operator import mod
from django.db import models

# Create your models here.
class SmtpSetting(models.Model):
    Host = models.CharField(max_length = 100, blank = True)
    Port = models.CharField(max_length = 10, blank = True)
    Sender = models.CharField(max_length = 200, blank = True)
    Password = models.CharField(max_length = 255, blank = True)