from django.urls import path,include
from .views import *

urlpatterns = [

    # pending Purchase Order
    path('all', all),
	path('one', one),
    path('all_filter', all_filter),
    path('all_filter_pagination', all_filter_pagination),

    # pending leger apis
    path('pending_purchase_order_dashboard', pending_purchase_order_dashboard),
    path('bp_pending_purchase_order', bp_pending_purchase_order),
    path('pending_items_by_purchase_order', pending_items_by_purchase_order),

]
