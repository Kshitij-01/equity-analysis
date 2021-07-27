from django import forms
from .models import User


class userform(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'dob', 'Username', 'password']


class loginform(forms.ModelForm):
    class Meta:
        model = User
        fields = ['Username', 'password']
