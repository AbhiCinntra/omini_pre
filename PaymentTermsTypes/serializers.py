from rest_framework import serializers
from .models import PaymentTermsTypes

class PaymentTermsTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTermsTypes
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"
        