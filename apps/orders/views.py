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
from django.shortcuts import render, redirect
from .forms import OrderForm
from .models import Order
from apps.carts.models import CartItem


@login_required(login_url="login")
def place_order(request):
    current_user = request.user

    # Step 1: Get the cart items of the logged-in user
    cart_items = CartItem.objects.filter(user=current_user)

    # Step 2: If the cart is empty, send the user back to the store
    if cart_items.count() == 0:
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
        return redirect("checkout")

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