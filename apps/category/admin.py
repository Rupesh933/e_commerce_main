from django.contrib import admin
from django.utils.text import Truncator
from django.utils.html import format_html
from .models import Category

# Register your models here.

@admin.register(Category)
class CustomCategoryAdmin(admin.ModelAdmin):
    list_display = ("category_name", "slug", "short_description", "cat_image_tag")
    prepopulated_fields = {
        "slug": ("category_name",),
    }
    search_fields = ("category_name", "description")
    list_filter = ("category_name", "created_at")


    def short_description(self, obj):
        return Truncator(obj.description).chars(60, truncate="...")

    short_description.short_description = "Description"  # column header label

    def cat_image_tag(self, obj):
        """Render a small preview thumbnail of the category image."""
        if obj.category_image:
            return format_html(
                '<img src="{}" width="80" height="60" '
                'style="object-fit:cover; border-radius:4px;" />',
                obj.category_image.url,
            )
        return "No Image"

    cat_image_tag.short_description = "Image Preview"
