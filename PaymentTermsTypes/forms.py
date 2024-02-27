from django import forms
from .models import PaymentTermsTypes

class PaymentTermsTypesForm(forms.ModelForm):
    class Meta:
        model = PaymentTermsTypes
        fields = "__all__"
