""" checkout / order views """
import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings
from django_countries.fields import CountryField
from products.models import Product
from accounts.models import UserAccount


class Order(models.Model):
    """ order process class """
    user_account = models.ForeignKey(UserAccount, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='orders')
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default='')
    order_number = models.CharField(max_length=32, null=False, editable=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    phone_number = models.CharField(max_length=25, null=False, blank=False)
    address_line_one = models.CharField(max_length=80, null=False, blank=False)
    address_line_two = models.CharField(max_length=80, null=True, blank=True)
    city = models.CharField(max_length=40, null=False, blank=False)
    county = models.CharField(max_length=40, null=True, blank=True)
    postcode = models.CharField(max_length=25, null=True, blank=True)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    delivery = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)

    def _generate_order_number(self):
        """ generate a randon order number """
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """set order number after overwriting save"""
        if not self.order_number:
            self.order_number = self._generate_order_number()

        super().save(*args, **kwargs)

    def update_total(self):
        """update total after each new item"""
        self.total = self.order_items.aggregate(Sum('order_item_total'))[
            'order_item_total__sum'] or 0
        if self.total < settings.DELIVERY_THRESHOLD:
            self.delivery = self.total * settings.DELIVERY_PERCENTAGE / 100
        else:
            self.delivery = 0
        self.grand_total = self.total + self.delivery
        self.save()

    def __str__(self):
        """ return order number """
        return self.order_number


class OrderItem(models.Model):
    """ order item class """
    order = models.ForeignKey(Order, null=False, blank=False,
                              on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE)
    order_item_total = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False, default=0)

    def save(self, *args, **kwargs):
        """override save"""

        self.order_item_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def _str_(self):
        return f'SKU {self.product.sku} for {self.order.order_number}'
