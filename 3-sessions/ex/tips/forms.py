from django import forms
from .models import Tip

class TipCreatingForm(forms.ModelForm):
    class Meta:
        model = Tip
        fields = ['content']