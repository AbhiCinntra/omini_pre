from rest_framework import serializers
from .models import *

class JournalEntriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntries
        fields = "__all__"
        depth = 1

class JournalEntryLinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntryLines
        fields = "__all__"
        depth = 1