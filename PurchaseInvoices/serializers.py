from rest_framework import serializers
from .models import *

class PurchaseInvoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseInvoices
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"

class AddressExtensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressExtension
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"
        
class DocumentLinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentLines
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"

class VendorPaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorPayments
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"

class VendorPaymentsInvoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorPaymentsInvoices
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"


class PurchaseCreditNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseCreditNotes
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"

class CreditNotesAddressExtensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditNotesAddressExtension
        fields = "__all__"

class CreditNotesDocumentLinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditNotesDocumentLines
        fields = "__all__"
                     