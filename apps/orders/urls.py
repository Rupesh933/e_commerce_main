from django.urls import path
from . import views

urlpatterns = [
    path("place_order/", views.place_order, name="place_order"),
    path("payments/<str:order_number>/", views.payments, name="payments"),
    path("confirm_payment/<str:order_number>/", views.confirm_payment, name="confirm_payment"),

    path("my_orders/", views.my_orders, name="my_orders"),
    path("address_list/", views.address_list, name="address_list")
]