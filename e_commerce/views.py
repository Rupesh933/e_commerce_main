from django.shortcuts import get_object_or_404, render
from apps.store.models import Product, Banner
from apps.category.models import Category

def home(request, category_slug=None):
    products = Product.objects.all().filter(is_availbale=True)[:10]
    banners = Banner.objects.filter(is_active=True)
    if category_slug is not None:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    context = {"products": products, "banners": banners}
    return render(request, "home.html", context)
