from django.urls import path,include
from .views import *

urlpatterns = [
    #path('create', create),
    path('all', all),
    path('all_filter', all_filter),
	path('one', one),
	path('pending', pending),
	path('pending_orderwise', pending_orderwise),
	path('pending_bybp', pending_bybp),
	path('pending_byorder', pending_byorder),
    #path('update', update),

    # new apis
    #path('sync_invoice', syncInvoice),
]
