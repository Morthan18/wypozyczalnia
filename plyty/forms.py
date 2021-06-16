from django import forms
from django.contrib.auth.models import User

from .models import Plyta


class PlytaForm(forms.Form):
    tytul = forms.CharField(max_length=200)
    cena = forms.DecimalField(max_digits=20, decimal_places=2)
    ilosc = forms.IntegerField()


class NewUserForm(forms.Form):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    email = forms.EmailField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
