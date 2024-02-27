from django.urls import path,include
from .views import *
from BusinessPartner import views, viewsBPBranch, viewsBPEmployee, viewsBPDepartment, viewsBPPosition


urlpatterns = [
    path('businesspartner/create', create),
    path('businesspartner/all', all),
    path('businesspartner/all_bp', all_bp),
    path('businesspartner/one', one),
    path('businesspartner/update', update),
    path('businesspartner/delete', delete),
    path('businesspartner/all_filter', all_filter),
    path('businesspartner/update_lat_long', update_lat_long),

    # for dms
    path('businesspartner/verify_distributor', verify_distributor),

    path('businesspartner/syncbp', syncBP),
    
    # BP Branch
    path('businesspartner/branch/create', viewsBPBranch.create),
    path('businesspartner/branch/one', viewsBPBranch.one),
    path('businesspartner/branch/all', viewsBPBranch.all),
    path('businesspartner/branch/update', viewsBPBranch.update),
    path('businesspartner/branch/delete', viewsBPBranch.delete),
    path('businesspartner/employee/create', viewsBPEmployee.create),
    path('businesspartner/employee/one', viewsBPEmployee.one),
    path('businesspartner/employee/all', viewsBPEmployee.all),
    path('businesspartner/employee/update', viewsBPEmployee.update),
    path('businesspartner/employee/delete', viewsBPEmployee.delete),
    
    path('businesspartner/department/create', viewsBPDepartment.create),
    path('businesspartner/department/one', viewsBPDepartment.one),
    path('businesspartner/department/all', viewsBPDepartment.all),
    path('businesspartner/department/update', viewsBPDepartment.update),
    path('businesspartner/department/delete', viewsBPDepartment.delete),
    
    path('businesspartner/position/create', viewsBPPosition.create),
    path('businesspartner/position/one', viewsBPPosition.one),
    path('businesspartner/position/all', viewsBPPosition.all),
    path('businesspartner/position/update', viewsBPPosition.update),
    path('businesspartner/position/delete', viewsBPPosition.delete),

    # BP type
    path('businesspartner/createtype', createtype),
    path('businesspartner/alltype', alltype),
    
    # added by millan to get only 5 fields from Customer on 08-September-2022    
    path('businesspartner/get_bp', get_bp),
    
    #added by millan for business_partner attachments 
    path('businesspartner/bp_attachments', bp_attachments),
    path('businesspartner/bp_attachment_create', bp_attachment_create),
    path('businesspartner/bp_attachment_update', bp_attachment_update),
    path('businesspartner/bp_attachment_delete', bp_attachment_delete),
    
    path('businesspartner/monthlySales', monthlySales), #added by millan on 06-10-2022
    path('businesspartner/top5Activity',top5Activity),   

    # sync
    path('businesspartner/updatebpcreditlimit',updatebpcreditlimit), # update all BP
    path('businesspartner/updatebpcreditlimitbybp',updatebpcreditlimitbybp), # update one by one

    path('businesspartner/all_filter_pagination', all_filter_pagination),
    path('businesspartner/all_data', all_data),
    path('businesspartner/all_data_pagination', all_data_pagination),
    path('businesspartner/all_bp_zones', all_bp_zones),
    path('businesspartner/all_bp_filter', all_bp_filter),
    path('businesspartner/bp_debit_credit', bp_debit_credit),
    path('businesspartner/all_bp_groupcode', all_bp_groupcode),
    path('businesspartner/bp_overview', bp_overview),

    # new url
    path('businesspartner/filter_ledger_dashboard', filter_ledger_dashboard),
    path('businesspartner/ledger_dashboard_count', ledger_dashboard_count),
    path('businesspartner/ledger_dashboard', ledger_dashboard),
    path('businesspartner/bp_ledger', bp_ledger),

    path('businesspartner/filter_receivable_dashboard', filter_receivable_dashboard),
    path('businesspartner/receivable_dashboard', receivable_dashboard),
    path('businesspartner/bp_receivable', bp_receivable),

    path('businesspartner/receipt_dashboard', receipt_dashboard),
    path('businesspartner/bp_receipt', bp_receipt),
    
    # purchase invoices 
    path('businesspartner/bp_purchase_invoices', bp_purchase_invoices),
    
    # Chart APIs urls 
    path('businesspartner/monthly_sales_chart', monthly_sales_chart),
    path('businesspartner/monthly_receipts_chart', monthly_receipts_chart),
    path('businesspartner/monthly_receivable_chart', monthly_receivable_chart),
    path('businesspartner/monthly_pending_chart', monthly_pending_chart),
    path('businesspartner/monthly_receivable_group_chart', monthly_receivable_group_chart),
    path('businesspartner/monthly_receivable_group_chart_filter', monthly_receivable_group_chart_filter),

    # new urls
    path('businesspartner/filter_due_payment_dashboard', filter_due_payment_dashboard),
    path('businesspartner/due_payment_dashboard_count', due_payment_dashboard_count),
    path('businesspartner/due_payment_dashboard', due_payment_dashboard),
    path('businesspartner/bp_due_payment', bp_due_payment),
    

    #Payable API's
    path('businesspartner/filter_payable_dashboard', filter_payable_dashboard),
    path('businesspartner/payable_dashboard', payable_dashboard),
    path('businesspartner/bp_payable', bp_payable),

    path('businesspartner/filter_due_payable_payment_dashboard', filter_due_payable_payment_dashboard),
    path('businesspartner/due_payable_payment_dashboard_count', due_payable_payment_dashboard_count),
    path('businesspartner/due_payable_payment_dashboard', due_payable_payment_dashboard),
    path('businesspartner/bp_payable_due_payment', bp_payable_due_payment),

    #Purchase Chart API's
    path('businesspartner/monthly_purchase_chart', monthly_purchase_chart),
    path('businesspartner/monthly_purchase_receipts_chart', monthly_purchase_receipts_chart),
    path('businesspartner/monthly_payable_chart', monthly_payable_chart),
    path('businesspartner/monthly_pending_purchase_chart', monthly_pending_purchase_chart),
    path('businesspartner/monthly_payable_group_chart', monthly_payable_group_chart),
    path('businesspartner/monthly_payable_group_chart_filter', monthly_payable_group_chart_filter),

]