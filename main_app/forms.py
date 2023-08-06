from django.forms import ModelForm
from .models import Pet, Vote, Amenity
# import forms
from django import forms

class PetForm(ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'breed']

class VoteForm(forms.ModelForm):

    class Meta:
        model = Vote
        fields = []


    def __init__(self, amenities, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for amenity in amenities:
            amenity_key = amenity[0]
            self.fields[f'{amenity_key}_available'] = forms.ChoiceField(
                choices=[("yes", "Yes"), ("no", "No")],
                widget=forms.RadioSelect,
                required=False,
            )    