from rest_framework import serializers
from .models import Industries

class IndustriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Industries
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"
        