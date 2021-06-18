import threading
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from .forms import DiskForm, NewUserForm
from .models import Disk, Cart, CartStatus, CartDisk, OrderDisk, OrderStatus
from .models import Order
from .tasks import export_orders_task

# Run tasks in background thread
exporter_thread = threading.Thread(target=export_orders_task, name="orders_exporter")
exporter_thread.start()


def render_main_page(request):
    return render(request, 'disks/main.html')


def render_disks(request):
    disks = Disk.objects.all().filter(quantity__gte=1)
    return render(request, 'disks/disks.html', {'disks': disks})


@login_required
def render_add_new_disk(request):
    if not request.user.is_superuser:
        messages.error(request, "Odmowa dostępu")
        return HttpResponseRedirect("/disks")

    if request.method == 'POST':
        form = DiskForm(request.POST)
        if form.is_valid():
            price = form.cleaned_data['price']
            quantity = form.cleaned_data['quantity']
            if price < 1 or quantity < 1:
                messages.error(request, "Podaj poprawną cenę lub ilość")
                return render(request, 'disks/disk_form.html', {'form': form})
            Disk.objects.create(
                title=form.cleaned_data['title'],
                price=price,
                quantity=quantity
            )
            messages.info(request, "Dodano płytę do asortymentu")
            return HttpResponseRedirect("/disks")
    else:
        form = DiskForm()
    return render(request, 'disks/disk_form.html', {'form': form})


@login_required
def render_edit_disk(request, disk_id):
    disk = Disk.objects.filter(pk=disk_id)
    if not disk.exists():
        messages.error(request, "Plyta nie istnieje")
        return HttpResponseRedirect("/disks")
    disk = disk.first()
    if request.method == 'POST':
        form = DiskForm(request.POST)
        if form.is_valid():
            Disk.objects.filter(pk=disk_id).update(
                title=form.cleaned_data['title'],
                price=form.cleaned_data['price'],
                quantity=form.cleaned_data['quantity']
            )
            return HttpResponseRedirect("/disks")
    else:
        form = DiskForm(initial={
            'title': disk.title,
            'price': disk.price,
            'quantity': disk.quantity
        })
    return render(request, 'disks/disk_form.html', {'form': form})


@login_required
def render_orders(request):
    return render(request, 'disks/orders.html', {'orders': Order.objects.filter(user=request.user).all()})


@login_required
def add_to_cart(request, disk_id):
    disk_to_add = Disk.objects.filter(pk=disk_id)
    if not disk_to_add.exists():
        messages.error(request, "Plyta nie istnieje")
        return HttpResponseRedirect("/disks")
    disk_to_add = disk_to_add.first()
    if disk_to_add.quantity < 1:
        messages.error(request, "Brak płyty na stanie")
        return HttpResponseRedirect("/disks")

    user = request.user
    user_cart = Cart.objects.filter(user=user, status=CartStatus.ACTIVE)
    if not user_cart.exists():
        user_cart = Cart.objects.create(user=user)
    else:
        user_cart = user_cart.first()

    maybe_disk_already_in_cart = CartDisk.objects.filter(cart=user_cart, disk=disk_to_add)
    if maybe_disk_already_in_cart.exists():

        maybe_disk_already_in_cart = maybe_disk_already_in_cart.first()
        maybe_disk_already_in_cart.quantity += 1
        maybe_disk_already_in_cart.save()
    else:
        CartDisk.objects.create(
            disk=disk_to_add,
            cart=user_cart,
            quantity=1
        )

    disk_to_add.quantity -= 1
    disk_to_add.save()

    messages.info(request, "Dodano plytę do koszyka")
    return HttpResponseRedirect("/disks")


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
                return render(request, 'disks/register_user_form.html', {'form': form, }, status=400)

            else:
                created_user = User.objects.create_user(email, email, password)
                created_user.first_name = first_name
                created_user.last_name = last_name
                created_user.save()

                authenticated_user = authenticate(username=email, password=password)
                if authenticated_user is not None:
                    login(request, created_user)
                return render_main_page(request)
    else:
        form = NewUserForm()
    return render(request, 'disks/register_user_form.html', {'form': form})


@login_required
def render_cart(request):
    cart_disks = None
    cart = Cart.objects.filter(user=request.user, status=CartStatus.ACTIVE)
    if cart.exists():
        cart_disks = CartDisk.objects.all().filter(cart=cart.first()).filter(quantity__gte=1)
    return render(request, 'disks/cart.html', {'cart_disks': cart_disks})


@login_required
def increment_disk_in_cart(request, disk_id):
    disk_to_increment = Disk.objects.filter(pk=disk_id)
    if not disk_to_increment.exists():
        messages.error(request, "Plyta nie istnieje")
        return render_cart(request)
    disk_to_increment = disk_to_increment.first()
    if disk_to_increment.quantity < 1:
        messages.error(request, "Brak płyty na stanie")
        return render_cart(request)

    cart = Cart.objects.filter(user=request.user, status=CartStatus.ACTIVE)
    if not cart.exists():
        messages.error(request, "Koszyk nie istnieje")
        return render_cart(request)
    disk_in_cart_to_increment = CartDisk.objects.filter(cart=cart.first(), disk=disk_to_increment).first()
    disk_in_cart_to_increment.quantity += 1
    disk_in_cart_to_increment.save()

    disk_to_increment.quantity -= 1
    disk_to_increment.save()
    return HttpResponseRedirect("/cart")


@login_required
def decrement_disk_in_cart(request, disk_id):
    disk_to_decrement = Disk.objects.filter(pk=disk_id)
    if not disk_to_decrement.exists():
        messages.error(request, "Plyta nie istnieje")
        return render_cart(request)
    disk_to_decrement = disk_to_decrement.first()
    cart = Cart.objects.filter(user=request.user, status=CartStatus.ACTIVE)
    if not cart.exists():
        messages.error(request, "Koszyk nie istnieje")
        return HttpResponseRedirect("/cart")
    disk_in_cart_to_increment = CartDisk.objects.filter(cart=cart.first(), disk=disk_to_decrement).first()
    disk_in_cart_to_increment.quantity -= 1
    disk_in_cart_to_increment.save()
    if disk_in_cart_to_increment.quantity == 0:
        disk_in_cart_to_increment.delete()

    disk_to_decrement.quantity += 1
    disk_to_decrement.save()
    return HttpResponseRedirect("/cart")


@login_required
def create_order(request, cart_id):
    cart = Cart.objects.filter(id=cart_id, status=CartStatus.ACTIVE)
    if not cart.exists():
        messages.error(request, "Koszyk nie istnieje")
        return HttpResponseRedirect("/cart")
    cart = cart.first()
    new_order = Order.objects.create(user=request.user,
                                     creation_date=datetime.now(tz=timezone.utc),
                                     status=OrderStatus.REALISED)
    cart_items = CartDisk.objects.all().filter(cart=cart)
    for cart_item in cart_items:
        OrderDisk.objects.create(disk=cart_item.disk, order=new_order, quantity=cart_item.quantity)

    cart.status = CartStatus.INACTIVE
    cart.save()
    return HttpResponseRedirect("/orders")
