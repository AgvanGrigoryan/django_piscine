from django import forms
from .models import People

class SearchField(forms.Form):
    min_release_date = forms.DateField(label="Minimum release date", required=False)
    max_release_date = forms.DateField(label="Maximum release date", required=False)
    min_planet_diameter = forms.IntegerField(label="Minimum planet diameter", required=False)
    actor_gender = forms.ChoiceField(choices=[], label="Actor Gender", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        genders = People.objects.values_list('gender', flat=True).distinct()
        choices = [('', 'Any')] + [(g, g) for g in genders]
        print(choices)
        self.fields['actor_gender'].choices = choices

    def clean(self):
        cleaned_data = super().clean()
        min_date = cleaned_data.get('min_released_date')
        max_date = cleaned_data.get('max_released_date')
        if min_date and max_date and min_date > max_date:
            raise forms.ValidationError("Minimum release date cannot be after maximum release date")
        return cleaned_data