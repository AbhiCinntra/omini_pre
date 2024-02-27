from django.urls import path,include
from .views import *

urlpatterns = [
    
    #  
    path('all', all),
	path('one', one),
    path('all_filter', all_filter),
    path('all_filter_pagination', all_filter_pagination),

    # new apis
    path('ap_incoming_payments', ap_incoming_payments),
    path('all_ap_incoming_payments', all_ap_incoming_payments),

    # credit note
    path('ap_credit_note_dashboard', ap_credit_note_dashboard), 
    path('ap_credit_notes', ap_credit_notes), 
    path('bp_ap_credit_notes', bp_ap_credit_notes),
    path('ap_credit_notes_one', ap_credit_notes_one),

    # ledger apis
    path('purchase_ledger_dashboard_count', purchase_ledger_dashboard_count),
    path('filter_purchase_ledger_dashboard', filter_purchase_ledger_dashboard),
    path('purchase_ledger_dashboard', purchase_ledger_dashboard),
    path('bp_purchase_ledger', bp_purchase_ledger),

    # vender payments apis
    path('purchase_receipt_dashboard', purchase_receipt_dashboard),
    path('bp_purchase_receipt', bp_purchase_receipt),
    path('one_receipt', one_receipt),

]
