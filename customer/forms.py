from django.forms import ModelForm
from .models import Patient, CreditCard
from django import forms
from django.contrib.auth.models import User


class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['age', 'phone_number', 'address']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')


class CardForm(ModelForm):
    class Meta:
        model = CreditCard
        fields = ['card_num', 'cvv', 'name']
