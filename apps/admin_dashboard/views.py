from django.shortcuts import render

from django.contrib.admin.views.decorators import staff_member_required

from apps.orders.models import Order
from apps.account.models import Account
from apps.store.models import Product

# Create your views here.

# @staff_member_required(login_url="login")
def dashboard(request):
    total_products = Product.objects.count()
    total_customers = Account.objects.filter(role="customer").count()
    total_orders = Order.objects.filter(is_ordered=True).count()
    context = {
        "total_products": total_products,
        "total_custormers": total_customers,
        "total_orders": total_orders,
    }
    return render(request, "admin_dashboard/dashboard.html", context)

def admin_products(request):
    return render(request, "admin_dashboard/products.html")


def admin_customers(request):
    return render(request, "admin_dashboard/customers.html")

def admin_orders(request):
    return render(request, "admin_dashboard/orders.html")

def admin_payments(request):
    return render(request, "admin_dashboard/payments.html")

# def admin_products(request):
#     return render(request, "admin_dashboard/banners.html")

def admin_banner(request):
    return render(request, "admin_dashboard/banners.html")