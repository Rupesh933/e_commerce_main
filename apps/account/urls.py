from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login, name="login"),
    path("register/", views.registration, name="register"),
    path("logout/", views.signout, name="logout"),

    path("edit_profile/", views.edit_profile, name="edit_profile"),
    
    path("forgotPassword/", views.forgotPassword, name="forgotPassword"),
    path("profile/", views.profile, name="profile"),


]
