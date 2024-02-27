from django.db import models

# Create your models here.

class DiscountPolicy(models.Model):
    DiscountName = models.CharField(max_length=200, blank=True)
    Type         = models.CharField(max_length=200, blank=True)
    SpecialInstr = models.CharField(max_length=250, blank=True)
    Attach       = models.CharField(max_length=100, blank=True)
