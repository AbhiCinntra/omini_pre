from django.db import models

# Create your models here.
class TripExpenses(models.Model):
    # checkin
    BPType          = models.CharField(max_length=200, blank=True)
    BPName          = models.CharField(max_length=200, blank=True)
    CardCode        = models.CharField(max_length=200, blank=True)
    SalesPersonCode = models.CharField(max_length=200, blank=True)
    ModeOfTransport = models.CharField(max_length=200, blank=True, default="")
    CheckInDate     = models.CharField(max_length=200, blank=True, default="")
    CheckInTime     = models.CharField(max_length=200, blank=True, default="")
    CheckInLat      = models.CharField(max_length=200, blank=True, default="")
    CheckInLong     = models.CharField(max_length=200, blank=True, default="")
    CheckInAttach   = models.CharField(max_length=200, blank=True, default="")
    CheckInRemarks  = models.TextField(blank=True, default="")
    # checkout
    CheckOutDate    = models.CharField(max_length=200, blank=True, default="")
    CheckOutTime    = models.CharField(max_length=200, blank=True, default="")
    CheckOutLat     = models.CharField(max_length=200, blank=True, default="")
    CheckOutLong    = models.CharField(max_length=200, blank=True, default="")
    CheckOutAttach  = models.CharField(max_length=200, blank=True, default="")
    CheckOutRemarks = models.TextField(blank=True, default="")
    TotalDistanceAuto = models.CharField(max_length=200, blank=True, default="")
    TotalDistanceManual = models.CharField(max_length=200, blank=True, default="")
    TotalExpenses   = models.CharField(max_length=100, blank=True, default="")
    CheckInStatus   = models.CharField(max_length=100, blank=True, default="Start")