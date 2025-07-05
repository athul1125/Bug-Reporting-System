from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    contact_number = forms.CharField(max_length=15, required=False)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'contact_number', 'role')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            # Save profile fields
            profile = Profile.objects.get(user=user)
            profile.contact_number = self.cleaned_data['contact_number']
            profile.role = self.cleaned_data['role']
            profile.save()
            # Add user to group based on role
            group, created = Group.objects.get_or_create(name=profile.role)
            user.groups.add(group)
        return user