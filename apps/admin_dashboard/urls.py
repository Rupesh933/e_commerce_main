from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="admin_dashboard"),

    path("products/", views.admin_products, name="admin_products"),
    path("products/add/", views.add_product, name="add_products"),
    path("products/edit/<int:product_id>/", views.edit_product, name="edit_product"),
    path("products/delete/<int:product_id>/", views.delete_product, name="delete_product"),

    path("customers/", views.admin_customers, name="admin_customers"),

    path("orders/", views.admin_orders, name="admin_orders"),
    path("orders/<int:order_id>/", views.order_detail, name="order_detail"),

    path("payments/", views.admin_payments, name="admin_payments"),
    path("banner/", views.admin_banner, name="admin_banner"),
]
