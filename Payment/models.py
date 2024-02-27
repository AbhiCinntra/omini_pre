from django.db import models  

class Payment(models.Model):
    InvoiceNo = models.CharField(max_length=50, blank=True)
    TransactId = models.CharField(max_length=50, blank=True)
    TotalAmt = models.CharField(max_length=20, blank=True)
    TransactMod = models.CharField(max_length=50, blank=True)
    DueAmount = models.CharField(max_length=50, blank=True)
    PaymentDate = models.CharField(max_length=50, blank=True)
    ReceivedAmount = models.CharField(max_length=50, blank=True)
    Remarks = models.TextField(blank=True)
    createDate = models.CharField(max_length=100, blank=True)
    createTime = models.CharField(max_length=100, blank=True)
    createdBy = models.IntegerField(default=0)
    updateDate = models.CharField(max_length=100, blank=True)
    updateTime = models.CharField(max_length=100, blank=True)
    updatedBy = models.IntegerField(default=0)
    CardCode = models.CharField(max_length=20, blank=True)