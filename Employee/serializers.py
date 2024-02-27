from rest_framework import serializers
from .models import *

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"

#added by millan on 15-11-2022 for employee target
class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = "__all__"
        #depth=1
                
class TargetqtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Targetqty
        fields = "__all__"
        depth=1

class TargetyrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Targetyr
        fields = "__all__"
        depth=1                  

class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = "__all__"
        depth=1                  

class UnitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Units
        fields = "__all__"
        depth=1                  