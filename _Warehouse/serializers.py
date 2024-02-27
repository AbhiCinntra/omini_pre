from rest_framework import serializers
from .models import *

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"
