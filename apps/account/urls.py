from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login, name="login"),
    path("register/", views.registration, name="register"),
    path("logout/", views.signout, name="logout"),

    path("edit_profile/", views.edit_profile, name="edit_profile"),
    
    path("change_password/", views.change_password, name="change_password"),
    path("profile/", views.profile, name="profile"),


    path("address/", views.address_list, name="address_list"),
    path("address/add/", views.add_address, name="add_address"),
    path("address/<int:address_id>/edit/", views.edit_address, name="edit_address"),
    path("address/<int:address_id>/delete/", views.delete_address, name="delete_address"),

]
