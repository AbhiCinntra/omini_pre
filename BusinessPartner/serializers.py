from rest_framework import serializers
from .models import *

class BusinessPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessPartner
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"
        depth = 1

class BPSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessPartner
        fields = ['id',"CardCode", "CardName", "EmailAddress","Phone1"]
        
        #exclude = ['id']
        #fields = "__all__"
        #depth = 1

class BPSelectFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessPartner
        fields = ['id',"CardCode", "CardName", "CreditLimit", "CreditLimitLeft","U_LAT","U_LONG"]
       

class BPAddressesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BPAddresses
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"
        depth = 1
        
class BPBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = BPBranch
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"

class BPEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BPEmployee
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"

class BPDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BPDepartment
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"
        
class BPPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BPPosition
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"
        
class BPTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BPType
        fields = "__all__"
        
#added by millan on 03-October-2022
class BPAttachmentSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = "__all__"
        
                
class BusinessPartnerGroupsSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = BusinessPartnerGroups
        fields = "__all__"

class BusinessPartnerZoneSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = BusinessPartnerZone
        fields = "__all__"
        
                