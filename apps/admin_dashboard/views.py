from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum

from apps.orders.models import Order
from apps.account.models import Account
from apps.store.models import Product

from .forms import ProductForm

# Create your views here.

# @staff_member_required(login_url="login")
def dashboard(request):
    low_stock_threshold = 20
    total_products = Product.objects.count()
    total_customers = Account.objects.filter(role="customer").count()
    total_orders = Order.objects.filter(is_ordered=True).count()
    total_revenue = Order.objects.filter(is_ordered=True).aggregate(total=Sum("order_total"))["total"] or 0
    pending_orders = Order.objects.filter(is_ordered=True, status="New").count()
    recent_orders = Order.objects.filter(is_ordered=True).order_by("-created_at")[:5]
    low_stock_products = Product.objects.filter(
        stock__lte=low_stock_threshold,
        is_availbale=True,
    ).order_by("stock")[:5]

    context = {
        "total_products": total_products,
        "total_custormers": total_customers,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "pending_orders": pending_orders,
        "recent_orders": recent_orders,
        "low_stock_products": low_stock_products,
        "low_stock_threshold": low_stock_threshold,
    }
    return render(request, "admin_dashboard/dashboard.html", context)

def admin_products(request):
    products = Product.objects.all().order_by("-created_at")
    total_products = Product.objects.count()
    context = {
        "products": products,
        "total_products": total_products
    }
    return render(request, "admin_dashboard/products.html", context)

def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("admin_products")
    else:
        form = ProductForm()
    context = {
        "form": form
    }
    return render(request, "admin_dashboard/add_products.html", context)

def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == "POST":
        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product,  # update only exiting product
        )
        if form.is_valid():
            form.save()
            return redirect("admin_products")
    else:
        form = ProductForm(instance=product)
    context = {
        "form": form,
        "product": product
    }
    return render(request, "admin_dashboard/edit_product.html", context)

def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == "POST":
        product.delete()
        return redirect("admin_products")
    return redirect("admin_products")

def admin_payments(request):
    return render(request, "admin_dashboard/payments.html")



def admin_customers(request):
    return render(request, "admin_dashboard/customers.html")

def admin_orders(request):
    orders = Order.objects.filter(is_ordered=True).order_by("-created_at")
    new_orders_count = orders.filter(status="New").count()
    accepted_orders_count = orders.filter(status="Accepted").count()
    completed_orders_count = orders.filter(status="Completed").count()
    canceled_orders_count = orders.filter(status="Cancelled").count()
    context = {
        "orders": orders,
        "new_orders_count": new_orders_count,
        "accepted_orders_count": accepted_orders_count,
        "completed_orders_count": completed_orders_count,
        "canceled_orders_count": canceled_orders_count,
    }
    return render(request, "admin_dashboard/orders.html", context)


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_products = order.items.all()

    if request.method == "POST":
        new_status = request.POST.get("status")

        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f"Order status updated to {order.status}.")
        else:
            messages.error(request, "Invalid status selected.")

        # Return to the orders list after updating the status
        return redirect("admin_orders")

    context = {
        "order": order,
        "order_products": order_products,
        "status_choices": Order.STATUS_CHOICES,
    }
    return render(request, "admin_dashboard/order_detail.html", context)


# def admin_products(request):
#     return render(request, "admin_dashboard/banners.html")

def admin_banner(request):
    return render(request, "admin_dashboard/banners.html")