from rest_framework import serializers
from .models import *

class CountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = "__all__"

class StatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = States
        fields = "__all__"
                        