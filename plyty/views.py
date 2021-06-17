import random

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.utils import timezone

from .forms import PlytaForm, NewUserForm
from .models import Plyta, Koszyk, StatusKoszyka, Plyty_koszyk, Produkt_zamowienia, StatusZamowienia
from .models import Zamowienie
from datetime import datetime


def render_glowna(request):
    return render(request, 'plyty/glowna.html')


def render_plyty(request):
    plyty = Plyta.objects.all().filter(dostepna_ilosc__gte=1)
    return render(request, 'plyty/plyty.html', {'plyty': plyty})


@login_required
def render_nowa_plyta(request):
    if not request.user.is_superuser:
        messages.error(request, "Odmowa dostępu")
        return HttpResponseRedirect("/plyty")

    if request.method == 'POST':
        form = PlytaForm(request.POST)
        if form.is_valid():
            Plyta.objects.create(
                tytul=form.cleaned_data['tytul'],
                cena=form.cleaned_data['cena'],
                dostepna_ilosc=form.cleaned_data['ilosc']
            )
            messages.info(request, "Dodano płytę do asortymentu")
            return HttpResponseRedirect("/plyty")
    else:
        form = PlytaForm()
    return render(request, 'plyty/plyta_form.html', {'form': form})


@login_required
def render_edytuj_plyte(request, plyta_id):
    plyta = Plyta.objects.filter(pk=plyta_id)
    if not plyta.exists():
        messages.error(request, "Plyta nie istnieje")
        return HttpResponseRedirect("/plyty")
    plyta = plyta.first()
    if request.method == 'POST':
        form = PlytaForm(request.POST)
        if form.is_valid():
            Plyta.objects.filter(pk=plyta_id).update(
                tytul=form.cleaned_data['tytul'],
                cena=form.cleaned_data['cena'],
                dostepna_ilosc=form.cleaned_data['ilosc']
            )
            return HttpResponseRedirect("/plyty")
    else:
        form = PlytaForm(initial={
            'tytul': plyta.tytul,
            'cena': plyta.cena,
            'ilosc': plyta.dostepna_ilosc
        })
    return render(request, 'plyty/plyta_form.html', {'form': form})


@login_required
def render_zamowienia(request):
    zamowienia = Zamowienie.objects.all()
    return render(request, 'plyty/zamowienia.html', {'zamowienia': zamowienia})


@login_required
def add_new_disk_to_cart(request, plyta_id):
    plyta_to_add = Plyta.objects.filter(pk=plyta_id)
    if not plyta_to_add.exists():
        messages.error(request, "Plyta nie istnieje")
        return HttpResponseRedirect("/plyty")
    plyta_to_add = plyta_to_add.first()
    if plyta_to_add.dostepna_ilosc < 1:
        messages.error(request, "Brak płyty na stanie")
        return HttpResponseRedirect("/plyty")

    user = request.user
    user_cart = Koszyk.objects.filter(user=user, status=StatusKoszyka.AKTYWNY)
    if not user_cart.exists():
        user_cart = Koszyk.objects.create(user=user)
    else:
        user_cart = user_cart.first()

    maybe_disk_already_in_cart = Plyty_koszyk.objects.filter(koszyk=user_cart, plyta=plyta_to_add)
    if maybe_disk_already_in_cart.exists():

        maybe_disk_already_in_cart = maybe_disk_already_in_cart.first()
        maybe_disk_already_in_cart.ilosc += 1
        maybe_disk_already_in_cart.save()
    else:
        Plyty_koszyk.objects.create(
            plyta=plyta_to_add,
            koszyk=user_cart,
            ilosc=1
        )

    plyta_to_add.dostepna_ilosc -= 1
    plyta_to_add.save()

    messages.info(request, "Dodano plytę do koszyka")
    return HttpResponseRedirect("/plyty")


def render_register_user(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if User.objects.filter(username=email).exists():
                messages.error(request, "Użytkownik z podanym adresem email już istnieje")
                return render(request, 'plyty/register_user_form.html', {'form': form, }, status=400)

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


@login_required
def render_cart(request):
    cart_disks = None
    koszyk = Koszyk.objects.filter(user=request.user, status=StatusKoszyka.AKTYWNY)
    if koszyk.exists():
        cart_disks = Plyty_koszyk.objects.all().filter(koszyk=koszyk.first()).filter(ilosc__gte=1)
    return render(request, 'plyty/cart.html', {'cart_disks': cart_disks})


@login_required
def increment_disk_in_cart(request, plyta_id):
    disk_to_increment = Plyta.objects.filter(pk=plyta_id)
    if not disk_to_increment.exists():
        messages.error(request, "Plyta nie istnieje")
        return render_cart(request)
    disk_to_increment = disk_to_increment.first()
    if disk_to_increment.dostepna_ilosc < 1:
        messages.error(request, "Brak płyty na stanie")
        return render_cart(request)

    koszyk = Koszyk.objects.filter(user=request.user, status=StatusKoszyka.AKTYWNY)
    if not koszyk.exists():
        messages.error(request, "Koszyk nie istnieje")
        return render_cart(request)
    disk_in_cart_to_increment = Plyty_koszyk.objects.filter(koszyk=koszyk.first(), plyta=disk_to_increment).first()
    disk_in_cart_to_increment.ilosc += 1
    disk_in_cart_to_increment.save()

    disk_to_increment.dostepna_ilosc -= 1
    disk_to_increment.save()
    return HttpResponseRedirect("/cart")


@login_required
def decrement_disk_in_cart(request, plyta_id):
    disk_to_decrement = Plyta.objects.filter(pk=plyta_id)
    if not disk_to_decrement.exists():
        messages.error(request, "Plyta nie istnieje")
        return render_cart(request)
    disk_to_decrement = disk_to_decrement.first()
    koszyk = Koszyk.objects.filter(user=request.user, status=StatusKoszyka.AKTYWNY)
    if not koszyk.exists():
        messages.error(request, "Koszyk nie istnieje")
        return HttpResponseRedirect("/cart")
    disk_in_cart_to_increment = Plyty_koszyk.objects.filter(koszyk=koszyk.first(), plyta=disk_to_decrement).first()
    disk_in_cart_to_increment.ilosc -= 1
    disk_in_cart_to_increment.save()
    if disk_in_cart_to_increment.ilosc == 0:
        disk_in_cart_to_increment.delete()

    disk_to_decrement.dostepna_ilosc += 1
    disk_to_decrement.save()
    return HttpResponseRedirect("/cart")


@login_required
def create_order(request, cart_id):
    cart = Koszyk.objects.filter(id=cart_id, status=StatusKoszyka.AKTYWNY)
    if not cart.exists():
        messages.error(request, "Koszyk nie istnieje")
        return HttpResponseRedirect("/cart")
    cart = cart.first()
    new_order = Zamowienie.objects.create(user=request.user,
                                          data_utworzenia=datetime.now(tz=timezone.utc),
                                          status=StatusZamowienia.W_TRAKCIE_REALIZACJI)
    cart_items = Plyty_koszyk.objects.all().filter(koszyk=cart)
    for cart_item in cart_items:
        Produkt_zamowienia.objects.create(plyta=cart_item.plyta, zamowienie=new_order, ilosc=cart_item.ilosc)

    cart.status = StatusKoszyka.NIEAKTYWNY
    cart.save()
    return HttpResponseRedirect("/zamowienia")
