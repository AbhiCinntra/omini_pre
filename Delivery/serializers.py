from rest_framework import serializers
from .models import *

class DeliveryShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryShipmentDetails
        fields = "__all__"
        depth = 1