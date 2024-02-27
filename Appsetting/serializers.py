from rest_framework import serializers
from .models import *

class AppsettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appsetting
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"
        depth = 1
