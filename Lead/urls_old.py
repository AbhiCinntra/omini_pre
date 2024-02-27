from django.urls import path,include
from .views import *

urlpatterns = [
    path('create', create),
    path('all', all),
    path('all_filter', all_filter),
    path('one',one),
    path('update', update),
    path('delete', delete),
    path('assign', assign),
    path('mark_junk', mark_junk),
    path('all_filter_junk', all_filter_junk),
    
    path('chatter', chatter),
    path('chatter_all', chatter_all),
    
    path('type_create', type_create),
    path('type_all', type_all),
    path('type_delete', type_delete),
    
    path('source_all', source_all),
    path('source_create', source_create),
    path('source_update', source_update),
    path('source_delete', source_delete),
    
    #added by millan for lead attachments
    path('lead_attachments', lead_attachments),
    path('lead_attachment_create', lead_attachment_create),
    path('lead_attachment_update', lead_attachment_update),
    path('lead_attachment_delete', lead_attachment_delete),
    
    #added by millan for lead notes on 13-10-2022
    path('lead_notes_create', lead_notes_create),
    path('lead_notes', lead_notes)

]
