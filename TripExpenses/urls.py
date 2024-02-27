from django.urls import path,include
from .views import *


urlpatterns = [
    path('tripexpense/trip_checkin', trip_checkin),
    path('tripexpense/trip_checkout', trip_checkout),
    path('tripexpense/one_tripexpenses', one_tripexpenses),
    path('tripexpense/all_tripexpenses', all_tripexpenses),
    path('tripexpense/all_filter_tripexpenses', all_filter_tripexpenses),
]