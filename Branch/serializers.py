from rest_framework import serializers
from .models import Branch

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"
        