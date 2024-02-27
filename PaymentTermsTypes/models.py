from django.db import models  

class PaymentTermsTypes(models.Model):
    GroupNumber = models.CharField(max_length=3, blank=True)
    PaymentTermsGroupName = models.CharField(max_length=100, blank=True)
