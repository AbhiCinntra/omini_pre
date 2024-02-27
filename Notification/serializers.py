from rest_framework import serializers
from .models import *

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"
        
