from rest_framework import serializers
from .models import *

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        depth = 1
        fields = [
            'id',
            'CodeType',
            'ItemName',
            'ItemCode',
            'CatID',
            'Description',
            'UnitPrice',
            'UoS',
            'UnitWeight',
            'HSN',
            'TaxCode',
            'Discount',
            'Status',
            'ItemsGroupCode',
            'U_GST',
            'GSTTaxCategory',
            'UoMIds'
        ]
        # fields = "__all__"
        #exclude = ['id']

class ItemWarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemWarehouse
        depth = 1
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"


class ItemPriceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPriceList
        fields = "__all__"



class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"

# ##########################################################
# ##########################################################
# #####################    Category    ###################
# ##########################################################
# ##########################################################
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
                "id",
                "Number",
                "CategoryName",
                "Status"
            ]
        #exclude = ['id']
        fields = "__all__"

# ##########################################################
# ##########################################################
# #####################    Price List    ###################
# ##########################################################
# ##########################################################

class PriceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceList
        fields = "__all__"


class UoMListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UoMList
        fields = "__all__"
