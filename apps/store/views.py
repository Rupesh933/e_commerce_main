from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Product
from apps.category.models import Category
from apps.carts.models import Cart, CartItem
from apps.carts.views import _cart_id

def _get_cart_product_ids(request):
    product_ids = set()
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        product_ids.update(CartItem.objects.filter(cart=cart, is_active=True).values_list("product_id", flat=True))
    except Exception:
        pass
    if request.user.is_authenticated:
        user_ids = CartItem.objects.filter(user=request.user, is_active=True).values_list("product_id", flat=True)
        product_ids.update(user_ids)
    return product_ids

def store(request, category_slug=None):
    products = Product.objects.filter(is_available=True).order_by("-id")
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    product_paginator = Paginator(products, 10)
    paged_products = product_paginator.get_page(request.GET.get("page"))
    cart_product_ids = _get_cart_product_ids(request)

    context = {
        "products": paged_products,
        "category_slug": category_slug,
        "cart_product_ids": cart_product_ids,
    }
    return render(request, "store/store.html", context)

def product_detail(request, category_slug, product_slug):
    single_product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    cart_product_ids = _get_cart_product_ids(request)
    in_cart = single_product.id in cart_product_ids

    context = {
        "single_product": single_product,
        "in_cart": in_cart,
    }
    return render(request, "store/product_detail.html", context)

def search(request):
    keyword = request.GET.get("keyword", "").strip()
    products = Product.objects.filter(is_available=True)
    if keyword:
        products = products.filter(
            Q(description__icontains=keyword)
            | Q(product_name__icontains=keyword)
            | Q(category__category_name__icontains=keyword)
        )
    products = products.order_by("-created_at")

    paginator = Paginator(products, 10)
    paged_products = paginator.get_page(request.GET.get("page"))
    cart_product_ids = _get_cart_product_ids(request)

    context = {
        "products": paged_products,
        "keyword": keyword,
        "cart_product_ids": cart_product_ids,
    }

    return render(request, "store/store.html", context)