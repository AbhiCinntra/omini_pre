from django import forms
from .models import *

class BusinessPartnerForm(forms.ModelForm):
    class Meta:
        model = BusinessPartner
        fields = "__all__"

class BPBranch(forms.ModelForm):
    class Meta:
        model = BPBranch
        fields = "__all__"

class BPEmployee(forms.ModelForm):
    class Meta:
        model = BPEmployee
        fields = "__all__"
