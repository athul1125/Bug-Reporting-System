from django import forms
from .models import Sprint
from django.contrib.auth.models import User


class SprintForm(forms.ModelForm):
    class Meta:
        model = Sprint
        fields = ['name', 'lead_developer', 'developers', 'duration']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lead_developer'].queryset = User.objects.filter(
            profile__role='developer'
        )
        self.fields['developers'].queryset = User.objects.filter(
            profile__role='developer'
        )

    def clean(self):
        cleaned_data = super().clean()
        lead_developer = cleaned_data.get('lead_developer')
        developers = cleaned_data.get('developers')

        if lead_developer and developers:
            if lead_developer in developers:
                raise forms.ValidationError(
                    "Lead developer cannot be in the development list."
                )
        return cleaned_data
