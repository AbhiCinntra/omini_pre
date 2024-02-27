from django.db import models  
#
class Invoice(models.Model):
    DocNum              = models.CharField(max_length=30, blank=True)
    TaxDate             = models.CharField(max_length=30, blank=True)
    DocDueDate          = models.CharField(max_length=30, blank=True)
    ContactPersonCode   = models.CharField(max_length=5, blank=True)
    DiscountPercent     = models.CharField(max_length=5, blank=True)
    DocDate             = models.CharField(max_length=30, blank=True)
    CardCode            = models.CharField(max_length=30, blank=True)
    Comments            = models.TextField(blank=True)
    SalesPersonCode     = models.CharField(max_length=5, blank=True)
    DocumentStatus      = models.CharField(max_length=50, blank=True)
    DocCurrency         = models.CharField(max_length=50, blank=True)
    DocTotal            = models.CharField(max_length=50, blank=True)
    CardName            = models.CharField(max_length=150, blank=True)
    VatSum              = models.CharField(max_length=50, blank=True)
    CreationDate        = models.CharField(max_length=50, blank=True)
    DocEntry            = models.CharField(max_length=5, blank=True)
    OrderID             = models.CharField(max_length=5, blank=True)
    AdditionalCharges   = models.CharField(max_length=100, blank=True)
    DeliveryCharge      = models.CharField(max_length=100, blank=True)
    CreateDate          = models.CharField(max_length=30, blank=True)
    CreateTime          = models.CharField(max_length=30, blank=True)
    UpdateDate          = models.CharField(max_length=30, blank=True)
    UpdateTime          = models.CharField(max_length=30, blank=True)
    PaymentGroupCode    = models.CharField(max_length=100, blank=True, default=1)
    Series              = models.CharField(max_length=100, blank=True, default='241')
    CancelStatus        = models.CharField(max_length=100, blank=True, default='csNo')
    #add extra data
    BPLID               = models.CharField(max_length=200, blank=True)
    BPLName             = models.CharField(max_length=200, blank=True)
    WTAmount            = models.CharField(max_length=200, blank=True)
    U_E_INV_NO          = models.CharField(max_length=200, blank=True)
    U_E_INV_Date        = models.CharField(max_length=200, blank=True)
    DocType             = models.CharField(max_length=100, blank=True, default="dDocument_Items") # dDocument_Service/dDocument_Items
    IGST                = models.CharField(max_length=200, blank=True, default=0)
    CGST                = models.CharField(max_length=200, blank=True, default=0)
    SGST                = models.CharField(max_length=200, blank=True, default=0)
    GSTRate             = models.CharField(max_length=200, blank=True, default=0)
    RoundingDiffAmount  = models.CharField(max_length=200, blank=True, default=0)
    U_SignedQRCode      = models.TextField(blank=True, default="")
    U_SignedInvoice     = models.TextField(blank=True, default="")
    U_EWayBill          = models.TextField(blank=True, default="")
    U_TransporterID     = models.CharField(max_length=200, blank=True, default=0)
    U_TransporterName   = models.CharField(max_length=200, blank=True, default=0)
    U_VehicalNo         = models.CharField(max_length=200, blank=True, default=0)
    NumAtCard           = models.CharField(max_length=200, blank=True, default=0)
    U_UNE_LRNo          = models.CharField(max_length=200, blank=True, default=0)
    U_UNE_LRDate        = models.CharField(max_length=200, blank=True, default=0)
    U_UNE_IRN           = models.TextField(blank=True, default="")
    OriginalRefNo       = models.TextField(blank=True, default="") #invoice ref id 
    OriginalRefDate     = models.TextField(blank=True, default="") #invoice ref date
    GSTTransactionType  = models.TextField(blank=True, default="") #invoice or Debit Note
    CNNo                = models.TextField(blank=True, default="") #invoice CN Number
    Address             = models.TextField(blank=True, default="") #bill to address
    Address2            = models.TextField(blank=True, default="") #ship to address
    VATRegNum           = models.TextField(blank=True, default="") #ship gst number
    PaidToDateSys       = models.TextField(blank=True, default="")
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#  
#                 Invocie Address Extenstion
#
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class AddressExtension(models.Model):
    InvoiceID       = models.CharField(max_length=5, blank=True)
    ShipToStreet    = models.CharField(max_length=100, blank=True)
    ShipToBlock     = models.CharField(max_length=100, blank=True)
    ShipToBuilding  = models.CharField(max_length=100, blank=True)
    ShipToCity      = models.CharField(max_length=100, blank=True)
    ShipToZipCode   = models.CharField(max_length=100, blank=True)
    ShipToCounty    = models.CharField(max_length=100, blank=True)
    ShipToState     = models.CharField(max_length=100, blank=True)
    ShipToCountry   = models.CharField(max_length=100, blank=True)
    ShipToAddress2  = models.CharField(max_length=100, blank=True)
    ShipToAddress3  = models.CharField(max_length=100, blank=True)
    BillToStreet    = models.CharField(max_length=100, blank=True)
    BillToBlock     = models.CharField(max_length=100, blank=True)
    BillToBuilding  = models.CharField(max_length=100, blank=True)
    BillToCity      = models.CharField(max_length=100, blank=True)
    BillToZipCode   = models.CharField(max_length=100, blank=True)
    BillToCounty    = models.CharField(max_length=100, blank=True)
    BillToState     = models.CharField(max_length=100, blank=True)
    BillToCountry   = models.CharField(max_length=100, blank=True)
    BillToAddress2  = models.CharField(max_length=100, blank=True)
    BillToAddress3  = models.CharField(max_length=100, blank=True)
    PlaceOfSupply   = models.CharField(max_length=100, blank=True)
    PurchasePlaceOfSupply = models.CharField(max_length=100, blank=True)
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
    InvoiceID       = models.CharField(max_length=5, blank=True)
    Quantity        = models.IntegerField(default=0)
    UnitPrice       = models.FloatField(default=0)
    DiscountPercent = models.FloatField(default=0)
    # ItemDescription = models.CharField(max_length=150, blank=True)
    ItemDescription = models.TextField(blank=True, default="")
    ItemCode        = models.CharField(max_length=10, blank=True)
    TaxCode         = models.CharField(max_length=10, blank=True)
    BaseEntry       = models.CharField(max_length=10, blank=True, default="")
    TaxRate         = models.CharField(max_length=10, blank=True, default=0)
    UomNo           = models.CharField(max_length=100, blank=True, default="")
    LineTotal       = models.CharField(max_length=100, blank=True, default="")
    # new key
    U_UTL_DIST      = models.CharField(max_length=100, blank=True, default="")
    U_UTL_SP        = models.CharField(max_length=100, blank=True, default="")
    U_UTL_DD        = models.CharField(max_length=100, blank=True, default="")
    U_UTL_SD        = models.CharField(max_length=100, blank=True, default="")
    U_UTL_TD        = models.CharField(max_length=100, blank=True, default="")
    U_UTL_MRPI      = models.CharField(max_length=100, blank=True, default="")
    U_RateType      = models.CharField(max_length=100, blank=True, default="")
    MeasureUnit     = models.CharField(max_length=100, blank=True, default="")
    SACEntry        = models.CharField(max_length=20, blank=True, default="")
    HSNEntry        = models.CharField(max_length=20, blank=True, default="")
    SAC             = models.CharField(max_length=200, blank=True, default="")
    HSN             = models.CharField(max_length=200, blank=True, default="")
    U_UTL_ITSBG     = models.CharField(max_length=200, blank=True, default = "")
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#  
#                 Invocie Incoming Payments
#
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class IncomingPayments(models.Model):
    # InvoiceDocEntry = models.CharField(max_length=10, blank=True)   
    DocNum            = models.CharField(max_length=100, blank=True)
    DocType           = models.CharField(max_length=100, blank=True)
    DocDate           = models.CharField(max_length=100, blank=True)
    CardCode          = models.CharField(max_length=100, blank=True)
    CardName          = models.CharField(max_length=200, blank=True)
    Address           = models.CharField(max_length=100, blank=True)
    DocCurrency       = models.CharField(max_length=100, blank=True)
    CheckAccount      = models.CharField(max_length=100, blank=True)
    TransferAccount   = models.CharField(max_length=100, blank=True)
    TransferSum       = models.CharField(max_length=100, blank=True)
    TransferDate      = models.CharField(max_length=100, blank=True)
    TransferReference = models.CharField(max_length=100, blank=True)
    Series            = models.CharField(max_length=100, blank=True)
    DocEntry          = models.CharField(max_length=100, blank=True)
    DueDate           = models.CharField(max_length=100, blank=True)
    BPLID             = models.CharField(max_length=100, blank=True)
    BPLName           = models.CharField(max_length=100, blank=True)
    Comments          = models.TextField(blank=True)
    JournalRemarks    = models.CharField(max_length=200, blank=True)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#
#                 Incoming Payment Invoices
#
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class IncomingPaymentInvoices(models.Model):
    IncomingPaymentsId = models.CharField(max_length=10, blank=True)
    LineNum            = models.CharField(max_length=100, blank=True)
    InvoiceDocEntry    = models.CharField(max_length=100, blank=True)
    SumApplied         = models.CharField(max_length=100, blank=True)
    AppliedFC          = models.CharField(max_length=100, blank=True)
    AppliedSys         = models.CharField(max_length=100, blank=True)
    DiscountPercent    = models.CharField(max_length=100, blank=True)
    TotalDiscount      = models.CharField(max_length=100, blank=True)
    TotalDiscountFC    = models.CharField(max_length=100, blank=True)
    TotalDiscountSC    = models.CharField(max_length=100, blank=True)
    DocDate            = models.CharField(max_length=100, blank=True)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#
#                 Invocie CreditNotesId Notes
#
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class CreditNotes(models.Model):
    DocNum              = models.CharField(max_length=30, blank=True)
    InvoiceDocEntry     = models.CharField(max_length=30, blank=True)
    TaxDate             = models.CharField(max_length=30, blank=True)
    DocDueDate          = models.CharField(max_length=30, blank=True)
    ContactPersonCode   = models.CharField(max_length=5, blank=True)
    DiscountPercent     = models.CharField(max_length=5, blank=True)
    DocDate             = models.CharField(max_length=30, blank=True)
    CardCode            = models.CharField(max_length=30, blank=True)
    Comments            = models.TextField(blank=True)
    SalesPersonCode     = models.CharField(max_length=5, blank=True)
    DocumentStatus      = models.CharField(max_length=50, blank=True)
    DocCurrency         = models.CharField(max_length=50, blank=True)
    DocTotal            = models.CharField(max_length=50, blank=True)
    CardName            = models.CharField(max_length=150, blank=True)
    VatSum              = models.CharField(max_length=50, blank=True)
    CreationDate        = models.CharField(max_length=50, blank=True)
    DocEntry            = models.CharField(max_length=5, blank=True)
    OrderID             = models.CharField(max_length=5, blank=True)
    AdditionalCharges   = models.CharField(max_length=100, blank=True)
    DeliveryCharge      = models.CharField(max_length=100, blank=True)
    CreateDate          = models.CharField(max_length=30, blank=True)
    CreateTime          = models.CharField(max_length=30, blank=True)
    UpdateDate          = models.CharField(max_length=30, blank=True)
    UpdateTime          = models.CharField(max_length=30, blank=True)
    PaymentGroupCode    = models.CharField(max_length=100, blank=True, default=1)
    Series              = models.CharField(max_length=100, blank=True, default='241')
    CancelStatus        = models.CharField(max_length=100, blank=True, default='csNo')
    #add extra data
    BPLID               = models.CharField(max_length=200, blank=True)
    BPLName             = models.CharField(max_length=200, blank=True)
    WTAmount            = models.CharField(max_length=200, blank=True)
    U_E_INV_NO          = models.CharField(max_length=200, blank=True)
    U_E_INV_Date        = models.CharField(max_length=200, blank=True)
    DocType             = models.CharField(max_length=100, blank=True, default="dDocument_Items") # dDocument_Service/dDocument_Items
    IGST                = models.CharField(max_length=200, blank=True, default=0)
    CGST                = models.CharField(max_length=200, blank=True, default=0)
    SGST                = models.CharField(max_length=200, blank=True, default=0)
    GSTRate             = models.CharField(max_length=200, blank=True, default=0)
    RoundingDiffAmount  = models.CharField(max_length=200, blank=True, default=0)
    U_SignedQRCode      = models.TextField(blank=True, default="")
    U_SignedInvoice     = models.TextField(blank=True, default="")
    U_EWayBill          = models.TextField(blank=True, default="")
    U_TransporterID     = models.CharField(max_length=200, blank=True, default=0)
    U_TransporterName   = models.CharField(max_length=200, blank=True, default=0)
    U_VehicalNo         = models.CharField(max_length=200, blank=True, default=0)
    NumAtCard           = models.CharField(max_length=200, blank=True, default=0)
    U_UNE_LRNo          = models.CharField(max_length=200, blank=True, default=0)
    U_UNE_LRDate        = models.CharField(max_length=200, blank=True, default=0)
    U_UNE_IRN           = models.TextField(blank=True, default="")
    OriginalRefNo       = models.TextField(blank=True, default="") #invoice ref id 
    OriginalRefDate     = models.TextField(blank=True, default="") #invoice ref date
    GSTTransactionType  = models.TextField(blank=True, default="") #invoice or Debit Note
    CNNo                = models.TextField(blank=True, default="") #invoice CN Number
    Address             = models.TextField(blank=True, default="") #bill to address
    Address2            = models.TextField(blank=True, default="") #ship to address
    VATRegNum           = models.TextField(blank=True, default="") #ship gst number
    PaidToDateSys       = models.TextField(blank=True, default="")
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#  
#                 CreditNotesId Address Extenstion
#
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class CreditNotesAddressExtension(models.Model):
    CreditNotesId   = models.CharField(max_length=5, blank=True)
    ShipToStreet    = models.CharField(max_length=100, blank=True)
    ShipToBlock     = models.CharField(max_length=100, blank=True)
    ShipToBuilding  = models.CharField(max_length=100, blank=True)
    ShipToCity      = models.CharField(max_length=100, blank=True)
    ShipToZipCode   = models.CharField(max_length=100, blank=True)
    ShipToCounty    = models.CharField(max_length=100, blank=True)
    ShipToState     = models.CharField(max_length=100, blank=True)
    ShipToCountry   = models.CharField(max_length=100, blank=True)
    ShipToAddress2  = models.CharField(max_length=100, blank=True)
    ShipToAddress3  = models.CharField(max_length=100, blank=True)
    BillToStreet    = models.CharField(max_length=100, blank=True)
    BillToBlock     = models.CharField(max_length=100, blank=True)
    BillToBuilding  = models.CharField(max_length=100, blank=True)
    BillToCity      = models.CharField(max_length=100, blank=True)
    BillToZipCode   = models.CharField(max_length=100, blank=True)
    BillToCounty    = models.CharField(max_length=100, blank=True)
    BillToState     = models.CharField(max_length=100, blank=True)
    BillToCountry   = models.CharField(max_length=100, blank=True)
    BillToAddress2  = models.CharField(max_length=100, blank=True)
    BillToAddress3  = models.CharField(max_length=100, blank=True)
    PlaceOfSupply   = models.CharField(max_length=100, blank=True)
    PurchasePlaceOfSupply = models.CharField(max_length=100, blank=True)
    U_SCOUNTRY      = models.CharField(max_length=100, blank=True)
    U_SSTATE        = models.CharField(max_length=100, blank=True)
    U_SHPTYPB       = models.CharField(max_length=100, blank=True)
    U_BSTATE        = models.CharField(max_length=100, blank=True)
    U_BCOUNTRY      = models.CharField(max_length=100, blank=True)
    U_SHPTYPS       = models.CharField(max_length=100, blank=True)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#
#                 CreditNotes Items
#
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class CreditNotesDocumentLines(models.Model):
    LineNum         = models.IntegerField(default=0)
    CreditNotesId   = models.CharField(max_length=5, blank=True)
    Quantity        = models.IntegerField(default=0)
    UnitPrice       = models.FloatField(default=0)
    DiscountPercent = models.FloatField(default=0)
    ItemDescription = models.CharField(max_length=150, blank=True)
    ItemCode        = models.CharField(max_length=10, blank=True)
    TaxCode         = models.CharField(max_length=10, blank=True)
    BaseEntry       = models.CharField(max_length=10, blank=True, default="")
    TaxRate         = models.CharField(max_length=10, blank=True, default=0)
    UomNo           = models.CharField(max_length=100, blank=True, default="")
    LineTotal       = models.CharField(max_length=100, blank=True, default="")
    # new key
    U_UTL_DIST      = models.CharField(max_length=100, blank=True, default="")
    U_UTL_SP        = models.CharField(max_length=100, blank=True, default="")
    U_UTL_DD        = models.CharField(max_length=100, blank=True, default="")
    U_UTL_SD        = models.CharField(max_length=100, blank=True, default="")
    U_UTL_TD        = models.CharField(max_length=100, blank=True, default="")
    U_UTL_MRPI      = models.CharField(max_length=100, blank=True, default="")
    U_RateType      = models.CharField(max_length=100, blank=True, default="")
    MeasureUnit     = models.CharField(max_length=100, blank=True, default="")
    SACEntry        = models.CharField(max_length=20, blank=True, default="")
    HSNEntry        = models.CharField(max_length=20, blank=True, default="")
    SAC             = models.CharField(max_length=200, blank=True, default="")
    HSN             = models.CharField(max_length=200, blank=True, default="")

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#
#                 Internal Reconciliation
#
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class InternalReconciliations(models.Model):
    TransId         = models.CharField(max_length=100, blank=True)
    TransRowId      = models.CharField(max_length=100, blank=True)
    ReconType       = models.CharField(max_length=100, blank=True)
    ShortName       = models.CharField(max_length=100, blank=True)
    CancelAbs       = models.CharField(max_length=100, blank=True)
    Total           = models.CharField(max_length=100, blank=True)
    ReconDate       = models.CharField(max_length=100, blank=True)
    SrcObjAbs       = models.CharField(max_length=100, blank=True)
    SrcObjTyp       = models.CharField(max_length=100, blank=True)
    IsCredit        = models.CharField(max_length=100, blank=True)
    ReconNum        = models.CharField(max_length=100, blank=True)
    ReconSum        = models.CharField(max_length=100, blank=True)
    DueDate         = models.CharField(max_length=100, blank=True)