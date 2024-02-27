from django.urls import path,include
from .views import *

urlpatterns = [
    path('create', create),
    path('update', update),
    path('delete', delete),
    path('all', all),
    path('all_filter', all_filter),
    path('all_filter_by_date', all_filter_by_date),
    path('one', one),
    path('status', status),
    
    path('maps', maps),
    path('map_one', map_one),
    path('map_all', map_all),
    path('map_filter', map_filter),
    path('chatter', chatter),
    path('chatter_all', chatter_all),
    path('followup', followup),
    path('map_filter_last_location', map_emps_last_location),
    path('map_emps_locations_by_month', map_emps_locations_by_month),
]
