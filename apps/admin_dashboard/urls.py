from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="admin_dashboard"),
    path("admin_products/", views.admin_products, name="admin_products"),
    path("admin_categories/", views.admin_categories, name="admin_categories"),
    path("admin_orders/", views.admin_orders, name="admin_orders"),
    path("admin_payments/", views.admin_payments, name="admin_customers"),
    path("admin_banner/", views.admin_banner, name="admin_banner"),
]
