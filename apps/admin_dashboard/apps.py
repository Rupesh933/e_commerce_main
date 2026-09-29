from django.apps import AppConfig


# class AdminDashboardConfig(AppConfig):
#     name = "apps.admin_dashboard"

# AppConfig is used to configure a Django application. In this class, name tells Django where the app is located, and default_auto_field tells Django what type of ID field to use automatically for models.


class AdminDashboardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.admin_dashboard"

"""
AdminDashboardConfig → Django app ki configuration class hai.

AppConfig → Django ki built-in class hai jo app ko configure karti hai.

name = "apps.admin_dashboard" → Django ko batata hai ki app kis location/package mein hai.

default_auto_field = "django.db.models.BigAutoField" → Models ke liye automatic id field ka type set karta hai.
"""