from rest_framework import serializers
from .models import *

class DiscountPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountPolicy
        depth = 1
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"
