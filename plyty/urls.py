from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.render_glowna, name='glowna'),
    path('plyty', views.render_plyty, name='plyty'),
    path('plyty/dodaj', views.render_nowa_plyta, name='dodaj_plyte'),
    path('plyty/edytuj/<int:plyta_id>', views.render_edytuj_plyte, name='edytuj_plyte'),
    path('zamowienia', views.render_zamowienia, name='zamowienia'),
    path('koszyk/dodaj/<int:plyta_id>', views.add_new_disk_to_cart, name='dodaj_do_koszyka'),
    path('accounts/register', views.render_register_user, name='register_user'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('cart', views.render_cart, name='cart'),
    path('cart/<int:plyta_id>/increment', views.increment_disk_in_cart, name='increment_disk_in_cart'),
    path('cart/<int:plyta_id>/decrement', views.decrement_disk_in_cart, name='decrement_disk_in_cart'),
    path('orders/<int:cart_id>', views.create_order, name='create_order')
]
