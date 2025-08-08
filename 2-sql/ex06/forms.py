from django import forms

class MovieSelectForm(forms.Form):
    movie = forms.ChoiceField(choices=[], label="Select Movie To Update")
    opening_crawl = forms.CharField(widget=forms.Textarea, label="Opening Crawl")

    def __init__(self, movie_choices=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if movie_choices:
            self.fields['movie'].choices = [('', '--- Select a movie ---')] + movie_choices
        else:
            self.fields['movie'].choices = [('', 'No movies available')]
            self.fields['movie'].disabled = True
            