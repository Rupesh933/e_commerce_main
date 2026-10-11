from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from apps.store.models import Product
from .models import Cart, CartItem

# Create your views here.

def _cart_id(request):
    """
    This function generates a unique cart ID for each session.
    If the cart ID is not found, it creates a new cart ID.
    """
    cart = request.session.session_key
    print("cart: ", cart)
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        if request.user.is_authenticated and not cart_item.user:
            cart_item.user = request.user
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
            user=request.user if request.user.is_authenticated else None,
        )
        cart_item.save()

    # go back to whichever page the request came from
    previous_page = request.META.get("HTTP_REFERER")
    if previous_page:
        return redirect(previous_page)
    # # return HttpResponse("cart_item", cart_item.quantity)
    return redirect("store")

def cart(request):
    total = 0
    quantity = 0
    cart_items = []
    tax = 0
    grand_totol = 0
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_totol = total + tax

    except ObjectDoesNotExist:
        pass

    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "tax": tax,
        "grand_total": grand_totol
    }
    return render(request, "store/cart.html", context)

def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -=1 
        cart_item.save()
    else:
        cart_item.delete()
    return redirect("cart")

def update_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.quantity += 1
    cart_item.save()
    return redirect("cart")

def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect("cart")

@login_required(login_url="login")
def checkout(request):
    total = 0
    quantity = 0
    cart_items = []
    tax = 0
    grand_total = 0

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass

    saved_addresses = []
    default_address = None
    if request.user.is_authenticated:
        from apps.account.models import Address
        saved_addresses = Address.objects.filter(user=request.user).order_by("-is_default", "-id")
        default_address = saved_addresses.filter(is_default=True).first() or saved_addresses.first()

    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "tax": tax,
        "grand_total": grand_total,
        "saved_addresses": saved_addresses,
        "default_address": default_address,
    }

    return render(request, "store/checkout.html", context)