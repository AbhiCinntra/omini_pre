from django.urls import path,include
from .views import *
urlpatterns = [
    path('opportunity/create', create),
    path('opportunity/all', all),
    path('opportunity/all_opp', all_opp),
    path('opportunity/all_filter', all_filter),
    path('opportunity/one', one),
    path('opportunity/update', update),
    path('opportunity/change_stage', change_stage),
    path('opportunity/complete', complete),
    path('opportunity/fav', fav),
    path('stage/all', all_stage),
    path('stage/one', one_stage),
    path('stage/stage_detail', stage_detail),
    path('stage/create', create_stage),
    path('line/all', all_line),
    path('line/one', one_line),

    # opportunity type
    path('opportunity/createtype', createtype),
    path('opportunity/alltype', alltype),
    
    #added by millan on 10-11-2022 for opportunity attachments 
    path('opportunity/opp_attachment_create', opp_attachment_create),
    path('opportunity/opp_attachment_delete', opp_attachment_delete),
    
]
