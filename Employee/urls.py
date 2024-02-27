from django.urls import path,include
from .views import *

urlpatterns = [
    path('create', create),
    path('all', all),
    path('all_filter', all_filter),
    # path('all_filter_assignto', all_filter_assignto),
    path('all_filter_reportingto', all_filter_reportingto),
    path('dashboard', dashboard),
    path('opportunity_bystage', opportunity_bystage),
    path('movingitems', movingitems),
    path('movingitems_count', movingitems_count),
    path('invoice_counter', invoice_counter),   
    path('analytics', analytics),
    path('top5bp', top5bp),
    path('top5itembyamount', top5itembyamount),
    path('one',one),
    path('login',login),
    path('update', update),
    path('delete', delete),  
    
    path('empExpen', empExpen),  #added by millan on 10-November-2022 for getting employee expenses
    
    path('monthlySalesEmp', monthlySalesEmp), #added by millan on 11-11-2022 for calculating monthly sales of an employee based on salespersoncode
    path('employee_target', employee_target), 
    path('target_anu_ach', target_anu_ach), 
    
    #added by millan on 14-11-2022 for target
    path('target_create', target_create),
    path('target_all', target_all),
    path('targetqtm_create', targetqtm_create),
    path('targetyr_create', targetyr_create),
    path('targetqty_close', targetqty_close),
    path('targetyr_close', targetyr_close),
    path('targetqtm_all', targetqtm_all),
    path('targetyr_all', targetyr_all),
    path('targetyr_all_filter', targetyr_all_filter),
    #added by millan on 14-11-2022 for target

    path('proSoldEmp', proSoldEmp),
    path('allroles', allroles),
    path('allunits', allunits),
    path('location_sharing_toggle', location_sharing_toggle),
]
