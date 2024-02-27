from django import forms
from .models import Appsetting

class AppsettingForm(forms.ModelForm):
    class Meta:
        model = Appsetting
        fields = "__all__"
