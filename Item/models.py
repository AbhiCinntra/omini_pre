from django.db import models  

class Category(models.Model):
    Number         = models.IntegerField(default = 0, unique = True)
    CategoryName   = models.CharField(max_length = 200, blank = True)
    Status         = models.IntegerField(default = 0, blank = True)      
    CreatedDate    = models.CharField(max_length = 30, blank = True)
    CreatedTime    = models.CharField(max_length = 30, blank = True)
    UpdatedDate    = models.CharField(max_length = 30, blank = True)
    UpdatedTime    = models.CharField(max_length = 30, blank = True)
    def __str__(self):
        return self.CategoryName

class SubCategory(models.Model):
    CategoryId     = models.IntegerField(default=0, unique=True)
    SubCatName     = models.CharField(max_length=200, blank=True)
    
class Item(models.Model):
    CodeType           = models.CharField(max_length = 100, blank=True)
    ItemName           = models.CharField(max_length = 250, blank=True)
    ItemCode           = models.CharField(max_length = 100, blank=True)
    CatID              = models.ForeignKey(Category, on_delete=models.CASCADE, default=0)
    Inventory          = models.CharField(max_length = 30, blank=True)
    Description        = models.CharField(max_length = 250, blank=True)
    UnitPrice          = models.CharField(max_length = 30, blank=True)
    UoS                = models.CharField(max_length = 100, blank=True)
    UnitWeight         = models.CharField(max_length = 100, blank=True)
    Packing            = models.CharField(max_length = 100, blank=True)
    Currency           = models.CharField(max_length = 30, blank=True)
    HSN                = models.CharField(max_length = 100, blank=True)
    TaxCode            = models.CharField(max_length = 100, blank=True)
    Discount           = models.CharField(max_length = 30, blank=True)
    Status             = models.CharField(max_length = 30, blank=True)
    CreatedDate        = models.CharField(max_length = 30, blank=True)
    CreatedTime        = models.CharField(max_length = 30, blank=True)
    UpdatedDate        = models.CharField(max_length = 30, blank=True)
    UpdatedTime        = models.CharField(max_length = 30, blank=True)
    ItemsGroupCode     = models.CharField(max_length = 30, blank=True, default="")
    U_GST              = models.CharField(max_length = 100, blank=True, default="")
    GSTTaxCategory     = models.CharField(max_length = 100, blank=True, default="")
    SalesItemsPerUnit  = models.CharField(max_length = 100, blank = True, default = "")
    UoMIds             = models.CharField(max_length = 100, blank = True, default = "")
    U_UTL_ITSBG        = models.CharField(max_length = 100, blank = True, default = "")
    U_UTL_ITMCT        = models.CharField(max_length = 100, blank = True, default = "")
    U_UTL_ST_ISSERVICE = models.CharField(max_length = 100, blank = True, default = "")

class Tax(models.Model):
    TaxName        = models.CharField(max_length = 30, blank=True)
    TaxCode        = models.CharField(max_length = 30, blank=True)
    CreatedDate    = models.CharField(max_length = 30, blank=True)
    CreatedTime    = models.CharField(max_length = 30, blank=True)

class ItemPriceList(models.Model):
    ItemCode       = models.CharField(max_length = 100, blank = True)
    PriceList      = models.CharField(max_length = 200, blank = True)
    Currency       = models.CharField(max_length = 200, blank = True)
    Price          = models.CharField(max_length = 20, blank = True)
    # Active       = models.CharField(max_length=20, blank=True, default="tYES")

class PriceList(models.Model):
    PriceListNo    = models.CharField(max_length = 200, blank=True)
    PriceListName  = models.CharField(max_length = 200, blank=True)
    Currency       = models.CharField(max_length = 200, blank=True)
    FixedAmount    = models.CharField(max_length = 20, blank=True)
    Active         = models.CharField(max_length = 20, blank=True, default="tYES")

class UoMList(models.Model):
    AbsEntry       = models.CharField(max_length = 10, blank = True)
    Code           = models.CharField(max_length = 200, blank = True)
    Name           = models.CharField(max_length = 200, blank = True)
    VolumeUnit     = models.CharField(max_length = 200, blank = True)
    Weight1        = models.CharField(max_length = 200, blank = True)
    Weight1Unit    = models.CharField(max_length = 200, blank = True)

class ItemWarehouse(models.Model):
    ItemCode        = models.CharField(max_length=200, blank=True)
    WarehouseCode   = models.CharField(max_length=200, blank=True)
    InStock         = models.CharField(max_length=200, blank=True)
    StandardAveragePrice = models.CharField(max_length=200, blank=True)

