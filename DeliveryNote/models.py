from django.db import models  
#
class DeliveryNote(models.Model):
    TaxDate           = models.CharField(max_length=30, blank=True)
    DocDueDate        = models.CharField(max_length=30, blank=True)
    ContactPersonCode = models.CharField(max_length=5, blank=True)
    DiscountPercent   = models.CharField(max_length=5, blank=True)
    DocDate           = models.CharField(max_length=30, blank=True)
    CardCode          = models.CharField(max_length=30, blank=True)
    Comments          = models.TextField(blank=True)
    SalesPersonCode   = models.CharField(max_length=5, blank=True)
    DocumentStatus    = models.CharField(max_length=50, blank=True)
    DocCurrency       = models.CharField(max_length=50, blank=True)
    DocTotal          = models.CharField(max_length=50, blank=True)
    CardName          = models.CharField(max_length=150, blank=True)
    VatSum            = models.CharField(max_length=50, blank=True)
    CreationDate      = models.CharField(max_length=50, blank=True)
    DocEntry          = models.CharField(max_length=5, blank=True)
    OrderID           = models.CharField(max_length=5, blank=True)
    CreateDate        = models.CharField(max_length=30, blank=True)
    CreateTime        = models.CharField(max_length=30, blank=True)
    UpdateDate        = models.CharField(max_length=30, blank=True)
    UpdateTime        = models.CharField(max_length=30, blank=True)
    # new keys
    CancelStatus      = models.CharField(max_length=100, blank=True, default='csNo')
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#  
#                 Invocie Address Extenstion
#
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class AddressExtension(models.Model):
    DeliveryNoteID  = models.CharField(max_length=5, blank=True)
    BillToBuilding  = models.CharField(max_length=100, blank=True)
    ShipToState     = models.CharField(max_length=100, blank=True)
    BillToCity      = models.CharField(max_length=100, blank=True)
    ShipToCountry   = models.CharField(max_length=100, blank=True)
    BillToZipCode   = models.CharField(max_length=100, blank=True)
    ShipToStreet    = models.CharField(max_length=100, blank=True)
    BillToState     = models.CharField(max_length=100, blank=True)
    ShipToZipCode   = models.CharField(max_length=100, blank=True)
    BillToStreet    = models.CharField(max_length=100, blank=True)
    ShipToBuilding  = models.CharField(max_length=100, blank=True)
    ShipToCity      = models.CharField(max_length=100, blank=True)
    BillToCountry   = models.CharField(max_length=100, blank=True)
    U_SCOUNTRY      = models.CharField(max_length=100, blank=True)
    U_SSTATE        = models.CharField(max_length=100, blank=True)
    U_SHPTYPB       = models.CharField(max_length=100, blank=True)
    U_BSTATE        = models.CharField(max_length=100, blank=True)
    U_BCOUNTRY      = models.CharField(max_length=100, blank=True)
    U_SHPTYPS       = models.CharField(max_length=100, blank=True)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#
#                 Invocie Items
#
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class DocumentLines(models.Model):
    LineNum         = models.IntegerField(default=0)
    DeliveryNoteID  = models.CharField(max_length=5, blank=True)
    Quantity        = models.IntegerField(default=0)
    UnitPrice       = models.FloatField(default=0)
    DiscountPercent = models.FloatField(default=0)
    ItemDescription = models.CharField(max_length=150, blank=True)
    ItemCode        = models.CharField(max_length=10, blank=True)
    TaxCode         = models.CharField(max_length=10, blank=True)
    BaseEntry       = models.CharField(max_length=10, blank=True, default="")
    TaxRate         = models.CharField(max_length=10, blank=True,default=0)
    UomNo           = models.CharField(max_length=100, blank=True, default="")
