from django.urls import path,include
from .views import *

urlpatterns = [
    path('create', create),
    path('all', all),
    path('all_filter', all_filter),
    path('one',one),
    path('update',update),
    path('delete',delete),
    path('fav',fav),
    path('approve',approve),
    
    #added by millan on 10-11-2022 for quotation attachments 
    path('quot_attachment_create', quot_attachment_create),
    path('quot_attachment_delete', quot_attachment_delete),
]
