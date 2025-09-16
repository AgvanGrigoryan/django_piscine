from django import forms
from .models import Article, UserFavouriteArticle
from django.utils.translation import pgettext_lazy

class PublishForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'synopsis', 'content']
        labels = {
            'title': pgettext_lazy('PublishForm form Title field label', 'Title'),
            'synopsis': pgettext_lazy('PublishForm form Synopsis field label', 'Synopsis'),
            'content': pgettext_lazy('PublishForm form Content field label', 'Content'),
        }

class AddFavouriteForm(forms.ModelForm):

    class Meta:
        model = UserFavouriteArticle
        fields = ['article']
        widgets = {
            'article': forms.HiddenInput()
        }
