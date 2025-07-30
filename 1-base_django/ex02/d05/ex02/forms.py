from django import forms

class TextForm(forms.Form):
    user_input = forms.CharField(label="Enter text")