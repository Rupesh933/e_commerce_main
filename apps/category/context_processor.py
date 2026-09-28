from .models import Category

def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)


"""
- View context = data for one specific view
- Context processor = common data available across templates
- We use context processors for data that is commonly required across multiple templates, such as the current user, site settings, cart count, notifications, or company information. It reduces repeated code in views.
"""