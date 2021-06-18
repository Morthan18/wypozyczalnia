from django import template

from disks.models import CartDisk

register = template.Library()


@register.simple_tag()
def calculate_total_cart(cart):
    total = 0
    disks_in_cart = CartDisk.objects.filter(cart=cart)
    for disk in disks_in_cart:
        total += disk.disks_cost
    return total
