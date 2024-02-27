from rest_framework import serializers
from .models import *

class CampaignSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignSet
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"
        
class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = "__all__"


class CampaignSetMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignSetMembers
        fields = "__all__"
