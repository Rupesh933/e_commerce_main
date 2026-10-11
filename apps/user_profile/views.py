from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

from apps.account.models import Address
from apps.orders.models import Order, OrderProduct
from .forms import UserProfileForm, AddressForm, UserPasswordChangeForm


@login_required(login_url="login")
def profile(request):
    """User profile overview dashboard."""
    addresses_count = Address.objects.filter(user=request.user).count()
    orders_count = Order.objects.filter(user=request.user, is_ordered=True).count()
    recent_orders = (
        Order.objects.filter(user=request.user, is_ordered=True)
        .prefetch_related("items__product")
        .order_by("-created_at")[:5]
    )
    context = {
        "addresses_count": addresses_count,
        "orders_count": orders_count,
        "recent_orders": recent_orders,
    }
    return render(request, "my_profile/profile.html", context)


@login_required(login_url="login")
def edit_profile(request):
    """Update personal information."""
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile details have been updated successfully.")
            return redirect("profile")
    else:
        form = UserProfileForm(instance=request.user)

    context = {"form": form}
    return render(request, "my_profile/edit_profile.html", context)


@login_required(login_url="login")
def change_password(request):
    """Change account password."""
    if request.method == "POST":
        form = UserPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Your password has been changed successfully.")
            return redirect("profile")
    else:
        form = UserPasswordChangeForm(user=request.user)

    context = {"form": form}
    return render(request, "my_profile/change_password.html", context)


@login_required(login_url="login")
def signout(request):
    """Log out the current user."""
    auth.logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("home")


# =========================================================
# ADDRESSES
# =========================================================

@login_required(login_url="login")
def address_list(request):
    """View saved addresses."""
    addresses = Address.objects.filter(user=request.user).order_by("-is_default", "-id")
    return render(request, "Saved Addresses/address_list.html", {"addresses": addresses})


@login_required(login_url="login")
def add_address(request):
    """Add a new delivery address."""
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            if not Address.objects.filter(user=request.user).exists():
                address.is_default = True
            address.save()
            messages.success(request, "Address added successfully.")
            return redirect("address_list")
    else:
        form = AddressForm()

    return render(request, "Saved Addresses/address_form.html", {"form": form})


@login_required(login_url="login")
def edit_address(request, address_id):
    """Edit an existing address."""
    address = get_object_or_404(Address, id=address_id, user=request.user)
    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, "Address updated successfully.")
            return redirect("address_list")
    else:
        form = AddressForm(instance=address)

    return render(request, "Saved Addresses/address_form.html", {"form": form})


@login_required(login_url="login")
def delete_address(request, address_id):
    """Delete a saved address."""
    address = get_object_or_404(Address, id=address_id, user=request.user)
    if request.method == "POST":
        address.delete()
        messages.success(request, "Address removed successfully.")
    return redirect("address_list")


# =========================================================
# ORDER HISTORY
# =========================================================

@login_required(login_url="login")
def my_orders(request):
    """User order history list."""
    orders = (
        Order.objects.filter(user=request.user, is_ordered=True)
        .prefetch_related("items__product")
        .order_by("-created_at")
    )
    return render(request, "my_profile/my_orders.html", {"orders": orders})


@login_required(login_url="login")
def order_detail(request, order_number):
    """View order details."""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    order_products = OrderProduct.objects.filter(order=order)
    subtotal = sum(item.product_price * item.quantity for item in order_products)
    context = {
        "order": order,
        "order_products": order_products,
        "subtotal": subtotal,
    }
    return render(request, "my_profile/orders_details.html", context)

