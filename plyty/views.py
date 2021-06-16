import random

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render

from .forms import PlytaForm, NewUserForm
from .models import Plyta
from .models import Zamowienie
from datetime import datetime


def render_glowna(request):
    return render(request, 'plyty/glowna.html')


def render_plyty(request):
    plyty = Plyta.objects.all().filter(dostepna_ilosc__gte=1)
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


def new_product_in_cart(request, plyta_id):
    # if not Plyta.objects.filter(pk=plyta_id).filter().exists():
    #
    #
    plyty = Plyta.objects.all().filter(dostepna_ilosc__gte=1)
    messages.error(request, "Dodano produkt do koszyka")
    return render(request, 'plyty/plyty.html', {'plyty': plyty})


def render_register_user(request):
    email_already_exists = 0
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if User.objects.filter(username=email).exists():
                render(request, 'plyty/register_user_form.html',
                       {'form': form, 'email_already_exists': email_already_exists}, status=400)

            else:
                created_user = User.objects.create_user(email, email, password)
                created_user.first_name = first_name
                created_user.last_name = last_name
                created_user.save()

                authenticated_user = authenticate(username=email, password=password)
                if authenticated_user is not None:
                    login(request, created_user)
                return render_glowna(request)
    else:
        form = NewUserForm()
    return render(request, 'plyty/register_user_form.html', {'form': form})
