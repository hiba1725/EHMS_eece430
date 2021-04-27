from django.forms import ModelForm
from .models import Manager
from django import forms
from django.contrib.auth.models import User


class ManagerForm(ModelForm):
    class Meta:
        model = Manager
        fields = ('role',)


class UserForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(max_length=150, required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
