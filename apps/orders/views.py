# from django.shortcuts import render, redirect
# from decimal import Decimal
# from django.contrib import messages
# from django.http import HttpResponse
# import datetime

# from .forms import OrderForm
# from .models import Order, Payment, OrderProduct
# from apps.carts.models import Cart, CartItem
# from apps.carts.views import _cart_id

# # Create your views here.

# def place_order(request):
#     current_user = request.user

#     cart_items = CartItem.objects.filter(user=current_user)
#     cart_count = cart_items.count()
#     if cart_count <= 0:
#         return redirect("store")

#     grand_total = 0
#     tax = 0
#     for cart_item in cart_items:
#         total += (cart_item.product.price * cart_item.quantity)
#         quantity += cart_item.quantity

#     tax = (2 * total)/100
#     grand_total = total + tax


#     if request.method == "POST":
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             # store all the billing information inside order table
#             data = Order()
#             data.first_name = form.cleaned_data("first_name")
#             data.last_name = form.cleaned_data("last_name")
#             data.phone_number = form.cleaned_data("phone_number")
#             data.email = form.cleaned_data("email")
#             data.address_line_1 = form.cleaned_data("address_line_1")
#             data.address_line_2 = form.cleaned_data("address_line_2")
#             data.city = form.cleaned_data("city")
#             data.state = form.cleaned_data("state")
#             data.country = form.cleaned_data("country")
#             data.order_note = form.cleaned_data("order_note")
#             data.order_total = grand_total
#             data.tax = tax
#             data.ip = request.META.get('REMOTE_ADDR')
#             data.save()

#             # generate order number
#             yr = int(datetime.data.today().strftime("%Y"))
#             dt = int(datetime.date.today().strftime("%d"))
#             mt = int(datetime.date.today().strftime("%m"))
#             d = datetime.date(yr,mt, dt)
#             current_date = d.strftime("%Y%m%d")  # 20261028
#             order_number = current_date + str(data.id)
#             data.order_number = order_number
#             data.save()
#             return redirect("checkout")
#     else:
#         return redirect("checkout")
#     # return HttpResponse("Place order")


import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import OrderForm
from .models import Order, Payment, OrderProduct
from apps.carts.models import Cart, CartItem
from apps.carts.views import _cart_id

def get_cart_items(request):
    # Get the session cart, return None if it does not exist
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        return None

    # Return only the active items of that cart
    return CartItem.objects.filter(cart=cart, is_active=True)


@login_required(login_url="login")
def place_order(request):
    current_user = request.user

    cart_items = get_cart_items(request)

    # Step 2: If the cart is missing or empty, go back to the store
    if cart_items is None or cart_items.count() == 0:
        return redirect("store")

    # Step 3: Calculate total, quantity and tax
    total = 0
    quantity = 0
    for cart_item in cart_items:
        total = total + (cart_item.product.price * cart_item.quantity)
        quantity = quantity + cart_item.quantity

    tax = (2 * total) / 100
    grand_total = total + tax

    # Step 4: If the request is not POST, go back to the checkout page
    if request.method != "POST":
        return redirect("checkout")

    # Step 5: Validate the submitted form
    form = OrderForm(request.POST)

    if form.is_valid():
        # Step 6: Create the order and fill in the billing details
        data = Order()
        data.user = current_user
        data.first_name = form.cleaned_data["first_name"]
        data.last_name = form.cleaned_data["last_name"]
        data.phone_number = form.cleaned_data["phone_number"]
        data.email = form.cleaned_data["email"]
        data.address_line_1 = form.cleaned_data["address_line_1"]
        data.address_line_2 = form.cleaned_data["address_line_2"]
        data.city = form.cleaned_data["city"]
        data.state = form.cleaned_data["state"]
        data.country = form.cleaned_data["country"]
        data.order_note = form.cleaned_data["order_note"]
        data.order_total = grand_total
        data.tax = tax
        data.ip = request.META.get("REMOTE_ADDR")
        data.save()  # First save, so that the order gets an id

        # Step 7: Generate the order number (current date + order id)
        today = datetime.date.today()
        current_date = today.strftime("%Y%m%d")  # e.g. 20260928
        data.order_number = current_date + str(data.id)
        data.save()  # Second save, now with the order number

        # Step 8: Move to the next step (for now, back to checkout)
        # return redirect("checkout")
        return redirect("payments", order_number=data.order_number)

    else:
        # Form is invalid, so show the checkout page again with the errors
        context = {
            "form": form,
            "cart_items": cart_items,
            "quantity": quantity,
            "total": total,
            "tax": tax,
            "grand_total": grand_total,
        }
        return render(request, "store/checkout.html", context)  # use your own template path


@login_required(login_url="login")
def payments(request, order_number):
    # Get this user's order that is not confirmed yet
    order = get_object_or_404(Order, order_number=order_number, user=request.user, is_ordered=False)

    # Get the cart items of this user
    cart_items = get_cart_items(request)
    if cart_items is None or cart_items.count() == 0:
        return redirect("store")

    total = 0
    quantity = 0
    for cart_item in cart_items:
        total = total + (cart_item.product.price * cart_item.quantity)
        quantity = quantity + cart_item.quantity

    tax = (2*total)/100
    grand_total = total + tax

    context = {
        "order": order,
        "cart_items": cart_items,
        "quantity": quantity,
        "total": total,
        "tax": tax,
        "grand_total": grand_total,
    }
    return render(request, "orders/payments.html", context)


@login_required(login_url="login")
def confirm_payment(request, order_number):
    # Step 1: Get this user's order that is not confirmed yet
    order = get_object_or_404(Order, order_number=order_number, user=request.user, is_ordered=False)

    # Step 2: Only accept POST requests
    if request.method != "POST":
        return redirect("payments", order_number=order_number)

    # Step 3: Read the selected payment method from the form
    method = request.POST.get("payment_method")

    # Step 4: Only Cash on delivery is supported for now
    if method != "cod":
        return redirect("payments", order_number=order_number)

    # Step 5: Get the cart items (same helper as place_order)
    cart_items = get_cart_items(request)
    if cart_items is None or cart_items.count() == 0:
        return redirect("store")

    # Step 6: Save the payment record
    payment = Payment()
    payment.user = request.user
    payment.payment_id = "COD-" + order.order_number
    payment.payment_method = "Cash on delivery"
    payment.amount_paid = order.order_total
    payment.save()

    # Step 7: Link the payment to the order and mark the order as confirmed
    order.payment = payment
    order.is_ordered = True
    order.save()

    # Step 8: Copy every cart item into OrderProduct
    for cart_item in cart_items:
        order_product = OrderProduct()
        order_product.order = order
        order_product.payment = payment
        order_product.user = request.user
        order_product.product = cart_item.product
        order_product.color = ""
        order_product.size = ""
        order_product.quantity = cart_item.quantity
        order_product.product_price = cart_item.product.price
        order_product.ordered = True
        order_product.save()

    # Step 9: Clear the cart
    cart_items.delete()

    # Step 10: Go to the next page (for now, the store)
    return redirect("store")

def my_orders(request): pass
def address_list(request): pass