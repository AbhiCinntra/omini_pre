from django.urls import path,include
from .views import *

urlpatterns = [
    # campaign set
    path('campset/create', create_campset),
    path('campset/all', all_campset),
    path('campset/one', one_campset),
    path('campset/update', update_campset),
    path('campset/status', campaignset_satus),

    # campaign
    path('camp/create', create_camp),
    path('camp/all', all_camp),
    path('camp/one', one_camp),
    path('camp/filter_campaign', filter_campaign),
    path('camp/update', update_camp),
    path('camp/status', campaign_satus),
    
    #campaignMembers updated by millan on 08-09-2022
    path('camp/memberlist',get_member),
    
    path('camp/create_member',member_create) #added by millan on 26-09-2022 for creating member list
    
]
