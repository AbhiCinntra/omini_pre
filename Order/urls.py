from django.urls import path,include
from .views import *

urlpatterns = [
    path('create', create),
    path('all', all),
	path('delivery', delivery),
	path('one',one),
    path('update',update),
    path('all_filter', all_filter),
    path('all_filter_pagination', all_filter_pagination),
    
    #added by millan on 10-11-2022 for order attachments 
    path('ord_attachment_create', ord_attachment_create),
    path('ord_attachment_delete', ord_attachment_delete),
    
    path('approve', approve),
    path('remarkshistory', remarksHistory),
    path('top5order', top5Order),
    
    path('bp_wise_sold_items', bp_wise_sold_items),
]
