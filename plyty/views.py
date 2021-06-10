import random

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import PlytaForm
from .models import Plyta
from .models import Zamowienie
from datetime import datetime


def render_glowna(request):
    # Plyta.objects.create(
    #     cena=decimal.Decimal(random.randrange(155, 389)) / 100,
    #     tytul="XYZ",
    #     dostepna_ilosc=random.randint(155,389)
    # )
    # Zamowienie.objects.create(
    #     user_id=1,
    #     data_utworzenia=datetime.now()
    # )
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
            return HttpResponseRedirect("/plyty/dodaj")
    else:
        form = PlytaForm()
    return render(request, 'plyty/nowa_plyta.html', {'form': form})


def render_zamowienia(request):
    zamowienia = Zamowienie.objects.all()
    return render(request, 'plyty/zamowienia.html', {'zamowienia': zamowienia})
