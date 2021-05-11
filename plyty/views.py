import random

from django.http import HttpResponse
from django.shortcuts import render
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


def render_zamowienia(request):
    zamowienia = Zamowienie.objects.all()
    return render(request, 'plyty/zamowienia.html', {'zamowienia': zamowienia})
