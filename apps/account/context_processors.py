from .models import Address


def deliver_to(request):
    if not request.user.is_authenticated:
        return {}

    address = Address.objects.filter(user=request.user, is_default=True).first()
    if not address:
        address = Address.objects.filter(user=request.user).order_by("-id").first()

    return {"deliver_address": address}