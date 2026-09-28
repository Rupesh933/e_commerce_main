from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Product
from apps.category.models import Category

def store(request, category_slug=None):
    products = Product.objects.filter(is_availbale=True).order_by("-id")
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    product_paginator = Paginator(products, 10)
    paged_products = product_paginator.get_page(request.GET.get("page"))

    context = {"products": paged_products, "category_slug": category_slug}
    return render(request, "store/store.html", context)

def product_detail(request, category_slug, product_slug):
    single_product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)

    context = {
        "single_product": single_product
    }
    return render(request, "store/product_detail.html", context)

def search(request):
    keyword = request.GET.get("keyword", "").strip()
    products = Product.objects.filter(is_availbale=True)
    if keyword:
        products = products.filter(
            Q(description__icontains=keyword)
            | Q(product_name__icontains=keyword)
            | Q(category__category_name__icontains=keyword)
        )
    products = products.order_by("-created_at")

    paginator = Paginator(products, 10)
    paged_products = paginator.get_page(request.GET.get("page"))

    context = {"products": paged_products, "keyword": keyword,}

    return render(request, "store/store.html", context)