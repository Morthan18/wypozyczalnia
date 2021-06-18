import csv
from datetime import datetime, timedelta, date, timezone

from plyty.models import Zamowienie, Produkt_zamowienia
from plyty.templatetags.calculate_total_order import calculate_total_order


def export_orders():
    now = date.today()
    with open("reports/report__{}.csv".format(now.strftime("%m_%d_%Y")), "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Id zamówienia', 'Status', 'Użytkownik', 'Wartość zamówienia'])

        yesterday = date_to_date_time(now - timedelta(days=1))
        today = date_to_date_time(now)

        orders = Zamowienie.objects.filter(data_utworzenia__range=[yesterday, today])

        for order in orders:
            writer.writerow([order.id, order.status, order.user.email, calculate_total_order(order)])


def date_to_date_time(date):
    return datetime.combine(date, datetime.min.time(), tzinfo=timezone.utc)
