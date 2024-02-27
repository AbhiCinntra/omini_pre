from django.urls import path, include
from .views import *

urlpatterns = [
    path('one', one),
    path('all', all),
    path('bp_wise', bp_wise),
    path('sync_reconcilation', sync_reconcilation),
]
