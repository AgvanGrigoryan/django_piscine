from django import forms
from .models import Movies

class MovieSelectForm(forms.Form):
    movie = forms.ModelChoiceField(queryset=Movies.objects.none(), label="Select Movie To Update")
    opening_crawl = forms.CharField(widget=forms.Textarea, label="Opening crawl")
    
    def __init__(self, movie_queryset=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['movie'].to_field_name = "title"
        if movie_queryset and movie_queryset.exists():
            self.fields['movie'].empty_label = '--- Select a movie ---'
            self.fields['movie'].queryset = movie_queryset
        else:
            self.fields['movie'].queryset = Movies.objects.none()
            self.fields['movie'].empty_label = 'No movies available'
            self.fields['movie'].disabled = True
            