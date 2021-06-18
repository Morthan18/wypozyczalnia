from django.db import models
from django.contrib.auth.models import User


class Disk(models.Model):
    price = models.DecimalField(max_digits=20, decimal_places=2)
    title = models.CharField(max_length=200)
    quantity = models.IntegerField()


class OrderStatus(models.TextChoices):
    NOT_REALISED = 'NOT_REALISED',
    IN_REALISATION = 'IN_REALISATION',
    REALISED = 'REALISED'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField()
    status = models.CharField(
        max_length=100,
        choices=OrderStatus.choices,
        default=OrderStatus.NOT_REALISED
    )


class OrderDisk(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    disk = models.ForeignKey(Disk, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        unique_together = (("order", "disk"),)

    def disks_cost(self):
        return self.quantity * self.disk.price


class CartStatus(models.TextChoices):
    ACTIVE = 'ACTIVE',
    INACTIVE = 'INACTIVE'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=100,
        choices=CartStatus.choices,
        default=CartStatus.ACTIVE
    )


class CartDisk(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    disk = models.ForeignKey(Disk, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        unique_together = (("cart", "disk"),)

    @property
    def disks_cost(self):
        return self.quantity * self.disk.price
