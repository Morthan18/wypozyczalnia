from django.urls import path

from . import views

urlpatterns = [
    path('', views.render_glowna, name='glowna'),
    path('plyty', views.render_plyty, name='plyty'),
    path('zamowienia', views.render_zamowienia, name='zamowienia')
]