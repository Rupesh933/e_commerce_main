from django.db import models
from apps.store.models import Product
from apps.account.models import Account

class Cart(models.Model):
    cart_id = models.CharField(max_length=100, blank=True)   # store user session key even user is not login, django can identify browser/session
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product