from django import forms
from .models import Countries

class CountriesForm(forms.ModelForm):
    class Meta:
        model = Countries
        fields = "__all__"
