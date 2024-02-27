from django.db import models  

class Notification(models.Model):
    Title = models.CharField(max_length=100, blank=True)
    Description = models.CharField(max_length=250, blank=True)
    Type = models.CharField(max_length=100, blank=True)
    SourceType = models.CharField(max_length=100, blank=True)
    SourceID = models.CharField(max_length=10, blank=True)
    Emp = models.CharField(max_length=4, blank=True)
    Read = models.CharField(max_length=1, blank=True)
    Push = models.IntegerField(default=0)
    SourceTime = models.CharField(max_length=10, blank=True)
    CreatedDate = models.CharField(max_length=10, blank=True)
    CreatedTime = models.CharField(max_length=10, blank=True)
