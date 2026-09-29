from django.db import models

from django.utils.text import slugify

from apps.category.models import Category
from django.urls import reverse

# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    is_availbale = models.BooleanField(default=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    images = models.ImageField(upload_to='photos/products')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse("product_detail", args=[self.category.slug, self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.product_name)
            slug = base_slug
            counter = 1

            # Keep trying until we find a slug that is not already used
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name

class Banner(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to="banners/")
    button_type = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

variation_category_choice = (
    ("color", "color"),
    ("size", "size"),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.product_name