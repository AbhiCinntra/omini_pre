from rest_framework import serializers
from .models import *

class SmtpSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmtpSetting
        #fields = ['ename',"econtact"]
        fields = "__all__"