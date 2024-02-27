from django.db import models  

class Quotation(models.Model):
    TaxDate           = models.CharField(max_length=30, blank=True)
    DocDueDate        = models.CharField(max_length=30, blank=True)
    ContactPersonCode = models.CharField(max_length=5, blank=True)
    DiscountPercent   = models.CharField(max_length=5, blank=True)
    DocDate           = models.CharField(max_length=30, blank=True)
    CardCode          = models.CharField(max_length=30, blank=True)
    Comments          = models.CharField(max_length=150, blank=True)
    SalesPersonCode   = models.CharField(max_length=5, blank=True)
    DocumentStatus    = models.CharField(max_length=50, blank=True)
    DocCurrency       = models.CharField(max_length=50, blank=True)
    DocTotal          = models.CharField(max_length=50, blank=True)
    CardName          = models.CharField(max_length=150, blank=True)
    VatSum            = models.CharField(max_length=50, blank=True)
    CreationDate      = models.CharField(max_length=50, blank=True)
    DocEntry          = models.CharField(max_length=5, blank=True)
    U_QUOTNM          = models.CharField(max_length=100, blank=True)
    U_OPPID           = models.CharField(max_length=5, blank=True)
    U_OPPRNM          = models.CharField(max_length=100, blank=True)
    U_FAV             = models.CharField(max_length=10, blank=True)
    U_APPROVEID       = models.IntegerField(default=0)
    U_APPROVENM       = models.CharField(max_length=30, blank=True)
    CreateDate        = models.CharField(max_length=30, blank=True)
    CreateTime        = models.CharField(max_length=30, blank=True)
    UpdateDate        = models.CharField(max_length=30, blank=True)
    UpdateTime        = models.CharField(max_length=30, blank=True)
    PaymentType       = models.CharField(max_length=100, blank=True)
    DeliveryMode      = models.CharField(max_length=100, blank=True)
    DeliveryTerm      = models.CharField(max_length=100, blank=True)
    AdditionalCharges = models.CharField(max_length=100, blank=True)
    TermCondition     = models.CharField(max_length=100, blank=True)
    DeliveryCharge    = models.CharField(max_length=100, blank=True)
    Unit              = models.CharField(max_length=100, blank=True)
    U_LAT             = models.CharField(max_length=100, blank=True)
    U_LONG            = models.CharField(max_length=100, blank=True)
    Link              = models.CharField(max_length=100, blank=True, default='')
    PayTermsGrpCode   = models.CharField(max_length=100, blank=True)
    FreeDelivery      = models.CharField(max_length=2, blank=True, default=0)
    CreatedBy         = models.CharField(max_length=5, blank=True, default=0)

class AddressExtension(models.Model):
    QuotationID       = models.CharField(max_length=5, blank=True)
    BillToBuilding    = models.CharField(max_length=100, blank=True)
    ShipToState       = models.CharField(max_length=100, blank=True)
    BillToCity        = models.CharField(max_length=100, blank=True)
    ShipToCountry     = models.CharField(max_length=100, blank=True)
    BillToZipCode     = models.CharField(max_length=100, blank=True)
    ShipToStreet      = models.CharField(max_length=100, blank=True)
    BillToState       = models.CharField(max_length=100, blank=True)
    ShipToZipCode     = models.CharField(max_length=100, blank=True)
    BillToStreet      = models.CharField(max_length=100, blank=True)
    ShipToBuilding    = models.CharField(max_length=100, blank=True)
    ShipToCity        = models.CharField(max_length=100, blank=True)
    BillToCountry     = models.CharField(max_length=100, blank=True)
    U_SCOUNTRY        = models.CharField(max_length=100, blank=True)
    U_SSTATE          = models.CharField(max_length=100, blank=True)
    U_SHPTYPB         = models.CharField(max_length=100, blank=True)
    U_BSTATE          = models.CharField(max_length=100, blank=True)
    U_BCOUNTRY        = models.CharField(max_length=100, blank=True)
    U_SHPTYPS         = models.CharField(max_length=100, blank=True)
    ShipToDistrict    = models.CharField(max_length=100, blank=True)
    BillToDistrict    = models.CharField(max_length=100, blank=True)

class DocumentLines(models.Model):
    LineNum           = models.IntegerField(default=0)
    QuotationID       = models.CharField(max_length=5, blank=True)
    Quantity          = models.IntegerField(default=0)
    UnitPrice         = models.FloatField(default=0)
    DiscountPercent   = models.FloatField(default=0)
    ItemCode          = models.CharField(max_length=10, blank=True)
    ItemDescription   = models.CharField(max_length=150, blank=True)
    TaxCode           = models.CharField(max_length=10, blank=True)
    # new key
    FreeText		  = models.CharField(max_length=500, blank=True)
    UomNo			  = models.CharField(max_length=100, blank=True)
    UnitWeight        = models.CharField(max_length=10, blank=True)
    TaxRate           = models.CharField(max_length=10, blank=True, default=0)
    UnitPriceown     = models.CharField(max_length=20, blank=True, default=0)
