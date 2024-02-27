from rest_framework import serializers
from .models import *

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"
        
class MapsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maps
        fields = "__all__"

class ChatterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chatter
        fields = "__all__"
                        