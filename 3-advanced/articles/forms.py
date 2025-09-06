from django import forms
from .models import Article

class PublishForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'synopsis', 'content']