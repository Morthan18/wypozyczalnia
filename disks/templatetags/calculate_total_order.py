from django import template

from disks.models import OrderDisk

register = template.Library()


@register.simple_tag()
def calculate_total_order(order):
    total = 0
    disks_in_order = OrderDisk.objects.filter(order=order)
    for order_disk in disks_in_order:
        total += order_disk.disks_cost()
    return total
