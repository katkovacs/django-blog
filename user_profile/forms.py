from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta():
        model = UserProfile
        fields = ('website','profile_pic', 'bio')

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['website','profile_pic', 'bio']
