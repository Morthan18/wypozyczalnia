from django import forms

from .models import Plyta


class PlytaForm(forms.Form):
    tytul = forms.CharField(max_length=200)
    cena = forms.DecimalField(max_digits=20, decimal_places=2)
    ilosc = forms.IntegerField()
