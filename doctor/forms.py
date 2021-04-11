from django.forms import ModelForm
from .models import Doctor
from django import forms
from django.contrib.auth.models import User


class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = ['age', 'phone_number', 'address', 'gender', 'specialty', 'years_of_experience', 'profile_pic']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
