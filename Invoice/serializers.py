from rest_framework import serializers
from .models import *

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
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

class IncomingPaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomingPayments
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"

class IncomingPaymentInvoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomingPaymentInvoices
        #fields = ['ename',"econtact"]
        #exclude = ['id']
        fields = "__all__"

class CreditNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditNotes
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
                