from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings

from .managers import MyAccountManager

class Account(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = [
        ("customer", "Customer"),
        ("seller", "Seller"),
        ("admin", "Admin")
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10)

    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default="customer")

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = MyAccountManager()


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "phone_number"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin and (self.is_admin or self.is_superuser)

    def has_module_perms(self, app_label):
        return self.is_active and self.is_staff

    

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="addresses", on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    address_line_1 = models.CharField(max_length=200)
    address_line_2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)

    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # If this address is marked default, remove default from the user's other addresses
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.address_line_1}, {self.city}"