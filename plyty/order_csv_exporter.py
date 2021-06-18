import csv
from datetime import datetime, timedelta, date, timezone

from django.contrib.auth.models import User

from plyty.models import Zamowienie, Produkt_zamowienia, StatusZamowienia
from plyty.templatetags.calculate_total_order import calculate_total_order


def export_orders():
    now = date.today()
    with open("reports/orders/report__{}.csv".format(now.strftime("%m_%d_%Y")), "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Id zamówienia', 'Status', 'Użytkownik', 'Wartość zamówienia'])

        yesterday = date_to_date_time(now - timedelta(days=1))
        today = date_to_date_time(now)

        orders = Zamowienie.objects.filter(data_utworzenia__range=[yesterday, today])

        for order in orders:
            writer.writerow([order.id, order.status, order.user.email, calculate_total_order(order)])


def export_total_user_orders():
    now = date.today()
    with open("reports/user/report__{}.csv".format(now.strftime("%m_%d_%Y")), "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Użytkownik',
                         'Ilość zrealizowanych zamówień',
                         'Ilość nie zrealizowanych zamówień',
                         "Ilość zamówień w trakcie realizacji",
                         'Wartość zrealizowanych zamówień'
                         ])

        yesterday = date_to_date_time(now - timedelta(days=1))
        today = date_to_date_time(now)

        users = User.objects.all()

        for user in users:
            realised_orders = Zamowienie.objects.filter(data_utworzenia__range=[yesterday, today],
                                                        user=user,
                                                        status=StatusZamowienia.ZREALIZOWANE)
            not_realised_orders = Zamowienie.objects.filter(data_utworzenia__range=[yesterday, today],
                                                            user=user,
                                                            status=StatusZamowienia.NIE_ZREALIZOWANE)
            in_realisation_orders = Zamowienie.objects.filter(data_utworzenia__range=[yesterday, today],
                                                              user=user,
                                                              status=StatusZamowienia.W_TRAKCIE_REALIZACJI)

            realised_orders_total = 0
            for realised_order in realised_orders:
                realised_orders_total += calculate_total_order(realised_order)

            writer.writerow([
                user.email,
                realised_orders.count(),
                not_realised_orders.count(),
                in_realisation_orders.count(),
                realised_orders_total
            ])


def date_to_date_time(date):
    return datetime.combine(date, datetime.min.time(), tzinfo=timezone.utc)
