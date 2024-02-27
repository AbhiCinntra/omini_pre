from rest_framework import serializers
from .models import *

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"
        depth = 1

class ChatterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chatter
        fields = "__all__"

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = "__all__"

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = "__all__"
        
#added by millan on 03-October-2022
class LeadAttachmentSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = LeadAttachment
        fields = "__all__"

#added by millan on 13-October-2022
class NotesSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = "__all__"

