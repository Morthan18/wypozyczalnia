from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .models import Disk


class DiskForm(forms.Form):
    title = forms.CharField(max_length=200)
    price = forms.DecimalField(max_digits=20, decimal_places=2)
    quantity = forms.IntegerField()


class NewUserForm(forms.Form):
    first_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
    last_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
    email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}))

    class Meta:
        model = User
