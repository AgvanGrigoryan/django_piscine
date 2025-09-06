from django import forms
from .models import Article, UserFavouriteArticle

class PublishForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'synopsis', 'content']

class AddFavouriteForm(forms.ModelForm):

    class Meta:
        model = UserFavouriteArticle
        fields = ['article']
        widgets = {
            'article': forms.HiddenInput()
        }
