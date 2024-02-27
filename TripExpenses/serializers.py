from rest_framework import serializers
from .models import *

class TripExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripExpenses
        fields = "__all__"
        depth = 1