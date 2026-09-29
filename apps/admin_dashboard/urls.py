from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="admin_dashboard"),
    path("products/", views.admin_products, name="admin_products"),
    path("customers/", views.admin_customers, name="admin_customers"),
    path("orders/", views.admin_orders, name="admin_orders"),
    path("payments/", views.admin_payments, name="admin_payments"),
    path("banner/", views.admin_banner, name="admin_banner"),
]
