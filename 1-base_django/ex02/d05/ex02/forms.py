from django import forms

class historyForm(forms.Form):
    history = forms.CharField(label="SOME LABEL")