from django import forms
from .models import *

class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = "__all__"
class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = "__all__"
class StaticStageForm(forms.ModelForm):
    class Meta:
        model = StaticStage
        fields = "__all__"
class LineForm(forms.ModelForm):
    class Meta:
        model = Line
        fields = "__all__"

