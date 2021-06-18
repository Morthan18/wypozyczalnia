from django.urls import path, include

from . import views
from .forms import LoginForm

urlpatterns = [
    path('', views.render_main_page, name='main'),
    path('disks', views.render_disks, name='disks'),
    path('disks/add', views.render_add_new_disk, name='add_disk'),
    path('disks/edit/<int:disk_id>', views.render_edit_disk, name='edit_disk'),
    path('orders', views.render_orders, name='orders'),
    path('cart/add/<int:disk_id>', views.add_to_cart, name='add_to_cart'),
    path('accounts/register', views.render_register_user, name='register_user'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('cart', views.render_cart, name='cart'),
    path('cart/<int:disk_id>/increment', views.increment_disk_in_cart, name='increment_disk_in_cart'),
    path('cart/<int:disk_id>/decrement', views.decrement_disk_in_cart, name='decrement_disk_in_cart'),
    path('orders/<int:cart_id>', views.create_order, name='create_order')
]
