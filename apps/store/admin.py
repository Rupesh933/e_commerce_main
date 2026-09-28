from django.contrib import admin
from .models import Product, Banner, Variation

# Register your models here.

admin.site.register(Product)
admin.site.register(Banner)
admin.site.register(Variation)