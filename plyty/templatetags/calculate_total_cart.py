from django import template

from plyty.models import Plyty_koszyk

register = template.Library()


@register.simple_tag()
def calculate_total_cart(koszyk):
    total = 0
    disks_in_cart = Plyty_koszyk.objects.filter(koszyk=koszyk)
    for disk in disks_in_cart:
        total += disk.disks_cost
    return total
