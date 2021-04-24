# Generated by Django 3.2 on 2021-04-24 06:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Plyta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cena', models.DecimalField(decimal_places=2, max_digits=20)),
                ('tytul', models.CharField(max_length=200)),
                ('dostepna_ilosc', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Zamowienie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_utworzenia', models.DateTimeField()),
                ('status', models.CharField(choices=[('NIE_ZREALIZOWANE', 'Nie Zrealizowane'), ('W_TRAKCIE_REALIZACJI', 'W Trakcie Realizacji'), ('ZREALIZOWANE', 'Zrealizowane')], default='NIE_ZREALIZOWANE', max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Produkt_zamowienia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ilosc', models.IntegerField()),
                ('plyta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plyty.plyta')),
                ('zamowienie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plyty.zamowienie')),
            ],
            options={
                'unique_together': {('plyta', 'zamowienie')},
            },
        ),
    ]
