from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

def dashboard(request):
    return render(request, "admin_dashboard/dashboard.html")

def admin_products(request):
    return render(request, "admin_dashboard/products.html")


def admin_categories(request):
    return render(request, "admin_dashboard/customers.html")

def admin_orders(request):
    return render(request, "admin_dashboard/orders.html")

def admin_payments(request):
    return render(request, "admin_dashboard/payments.html")

# def admin_products(request):
#     return render(request, "admin_dashboard/banners.html")

def admin_banner(request):
    return render(request, "admin_dashboard/banners.html")