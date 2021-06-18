from django import template

from plyty.models import Produkt_zamowienia

register = template.Library()


@register.simple_tag()
def calculate_total_order(order):
    total = 0
    disks_in_order = Produkt_zamowienia.objects.filter(zamowienie=order)
    for order_disk in disks_in_order:
        total += order_disk.disks_cost()
    return total
