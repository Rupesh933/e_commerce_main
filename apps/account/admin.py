from django.contrib import admin
from .models import Account

@admin.register(Account)
class CustomAccountAdmin(admin.ModelAdmin):
    model = Account
    list_display = ("first_name", "last_name", "username", "email", "role", "phone_number", "is_active", "is_admin", "is_staff")
    list_filter = ("is_active", "is_admin", "is_staff")
    list_display_links = ("username", "email")
    filter_horizontal = ("groups", "user_permissions")
    list_editable = ("is_staff", "is_active", "is_admin")
    readonly_fields = ("date_joined", "last_login")
    ordering = ("-date_joined",)