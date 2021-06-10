import random

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render

from .forms import PlytaForm
from .models import Plyta
from .models import Zamowienie
from datetime import datetime


def render_glowna(request):
    return render(request, 'plyty/glowna.html')


def render_plyty(request):
    plyty = Plyta.objects.all()
    return render(request, 'plyty/plyty.html', {'plyty': plyty})


def render_nowa_plyta(request):
    if request.method == 'POST':
        form = PlytaForm(request.POST)
        if form.is_valid():
            Plyta.objects.create(
                tytul=form.cleaned_data['tytul'],
                cena=form.cleaned_data['cena'],
                dostepna_ilosc=form.cleaned_data['ilosc']
            )
            return render_plyty(request)
    else:
        form = PlytaForm()
    return render(request, 'plyty/plyta_form.html', {'form': form})


def render_edytuj_plyte(request, plyta_id):
    plyta = Plyta.objects.filter(pk=plyta_id)
    if not plyta.exists():
        return HttpResponseNotFound("<h1>Zasób nie znaleziony</h1>")
    plyta = plyta.first()
    if request.method == 'POST':
        form = PlytaForm(request.POST)
        if form.is_valid():
            Plyta.objects.filter(pk=plyta_id).update(
                tytul=form.cleaned_data['tytul'],
                cena=form.cleaned_data['cena'],
                dostepna_ilosc=form.cleaned_data['ilosc']
            )
            return render_plyty(request)
    else:
        form = PlytaForm(initial={
            'tytul': plyta.tytul,
            'cena': plyta.cena,
            'ilosc': plyta.dostepna_ilosc
        })
    return render(request, 'plyty/plyta_form.html', {'form': form})


def render_zamowienia(request):
    zamowienia = Zamowienie.objects.all()
    return render(request, 'plyty/zamowienia.html', {'zamowienia': zamowienia})
