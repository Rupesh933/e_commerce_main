from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

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