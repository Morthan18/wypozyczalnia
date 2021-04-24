from django.db import models
from django.contrib.auth.models import User


class Plyta(models.Model):
    cena = models.DecimalField(max_digits=20, decimal_places=2)
    tytul = models.CharField(max_length=200)
    dostepna_ilosc = models.IntegerField()


class StatusZamowienia(models.TextChoices):
    NIE_ZREALIZOWANE = 'NIE_ZREALIZOWANE',
    W_TRAKCIE_REALIZACJI = 'W_TRAKCIE_REALIZACJI',
    ZREALIZOWANE = 'ZREALIZOWANE'


class Zamowienie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data_utworzenia = models.DateTimeField()
    status = models.CharField(
        max_length=100,
        choices=StatusZamowienia.choices,
        default=StatusZamowienia.NIE_ZREALIZOWANE
    )


class Produkt_zamowienia(models.Model):
    plyta = models.ForeignKey(Plyta, on_delete=models.CASCADE)
    zamowienie = models.ForeignKey(Zamowienie, on_delete=models.CASCADE)
    ilosc = models.IntegerField()

    class Meta:
        unique_together = (("plyta", "zamowienie"),)
