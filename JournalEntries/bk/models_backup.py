from django.db import models

# Create your models here.
class JournalEntries(models.Model):
    Number           = models.CharField(max_length=200, blank=True)
    JdtNum           = models.CharField(max_length=200, blank=True)
    Original         = models.CharField(max_length=200, blank=True) #source id (invoice, credit memo, incomming payment)
    OriginalJournal  = models.CharField(max_length=200, blank=True)   
    ReferenceDate    = models.CharField(max_length=200, blank=True)
    Memo             = models.TextField( blank=True)
    TransactionCode  = models.CharField(max_length=200, blank=True)
    TaxDate          = models.CharField(max_length=200, blank=True)
    U_UNE_Narration  = models.TextField( blank=True)
    CNNo             = models.TextField(blank=True, default="")
    DocType          = models.CharField(max_length=200, blank=True)
    U_Cancel         = models.CharField(max_length=200, blank=True, default="N")

class JournalEntryLines(models.Model):
    JournalEntriesId = models.CharField(max_length=30, blank=True)
    Line_ID          = models.CharField(max_length=200, blank=True)
    AccountCode      = models.CharField(max_length=200, blank=True)
    Debit            = models.CharField(max_length=200, blank=True)
    Credit           = models.CharField(max_length=250, blank=True)
    DueDate          = models.CharField(max_length=250, blank=True)
    ShortName        = models.CharField(max_length=250, blank=True)
    ContraAccount    = models.CharField(max_length=250, blank=True)
    LineMemo         = models.TextField(blank=True)
    ReferenceDate1   = models.CharField(max_length=250, blank=True) 
    Reference1       = models.CharField(max_length=250, blank=True) #Referece DocNum 
    # new keys
    AccountName      = models.CharField(max_length=200, blank=True, default="")
    Reference2       = models.CharField(max_length=250, blank=True) #Referece No
    BPLID            = models.CharField(max_length=250, blank=True) #Branch Id
    BPLName          = models.CharField(max_length=250, blank=True) #Branch Name
    ReconSum         = models.CharField(max_length=250, blank=True, default = 0)
    # CNNo             = models.TextField(blank=True, default="") #invoice CN Number