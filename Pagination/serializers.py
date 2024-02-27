from rest_framework import serializers
from .models import *

class PagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagination
        fields = ["MaxSize"]

class PageGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagination
        fields = "__all__"

