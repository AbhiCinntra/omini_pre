from django.db import models

# Create your models here.
class Pagination(models.Model):
    MaxSize = models.CharField(max_length=50, blank=True)
    Status = models.CharField(max_length=50, default="Active", blank=True)