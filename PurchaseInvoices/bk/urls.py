from django.urls import path,include
from .views import *

urlpatterns = [
    
    path('all', all),
	path('one', one),
    path('all_filter', all_filter),
    path('all_filter_pagination', all_filter_pagination),

    # new apis
    path('ap_incoming_payments', ap_incoming_payments),
    path('all_ap_incoming_payments', all_ap_incoming_payments),

    # credit note
    path('ap_credit_notes', ap_credit_notes), 
    path('bp_ap_credit_notes', bp_ap_credit_notes),
    path('ap_credit_notes_one', ap_credit_notes_one),

    # path('payment_collection_dashboard', payment_collection_dashboard),
    # path('bp_payment_collection', bp_payment_collection),
    
    # path('credit_note_dashboard', credit_note_dashboard),
    # path('bp_credit_note', bp_credit_note),

    # path('pending_payment_collection', pending_payment_collection),
    # path('sync_invoice', syncInvoice),

    # path('one_receipt', one_receipt),
    # path('bp_wise_receipt', bp_wise_receipt),
    # path('bp_wise_sold_items', bp_wise_sold_items),
]
