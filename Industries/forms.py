from django import forms
from .models import Industries

class IndustriesForm(forms.ModelForm):
    class Meta:
        model = Industries
        fields = "__all__"
