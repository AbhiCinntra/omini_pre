from django.db import models

class DeliveryShipmentDetails(models.Model):  
    shippingName = models.CharField(max_length=100, blank=True)
    zipCode = models.CharField(max_length=100, blank=True)
    countryId = models.CharField(max_length=20, blank=True)
    stateId = models.CharField(max_length=20, blank=True)
    shippingType = models.CharField(max_length=100, blank=True)
    shippingAddress = models.TextField(blank=True)
    createDate = models.CharField(max_length=100, blank=True)
    createTime = models.CharField(max_length=100, blank=True)
    createdBy = models.IntegerField(default=0)
    deliveryId = models.IntegerField(default=0)
    updateDate = models.CharField(max_length=100, blank=True)
    updateTime = models.CharField(max_length=100, blank=True)
    updatedBy = models.IntegerField(default=0)
