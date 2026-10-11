from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime
from django.db.models.functions import TruncMonth
from django.db.models import Q
from django.core.paginator import Paginator


from apps.orders.models import Order
from apps.account.models import Account
from apps.category.models import Category
from apps.store.models import Product

from .forms import ProductForm

# Create your views here.

# @staff_member_required(login_url="login")
def dashboard(request):
    low_stock_threshold = 20
    total_products = Product.objects.count()
    total_customers = Account.objects.filter(role="customer").count()
    total_orders = Order.objects.filter(is_ordered=True).count()
    total_revenue = Order.objects.filter(is_ordered=True).aggregate(total=Sum("order_total"))["total"] or 0
    pending_orders = Order.objects.filter(is_ordered=True, status="New").count()
    recent_orders = (
        Order.objects.filter(is_ordered=True)
        .prefetch_related("items__product")
        .order_by("-created_at")[:5]
    )
    low_stock_products = Product.objects.filter(stock__lte=low_stock_threshold, is_available=True,).order_by("stock")[:5]
    
##===================================================================
    # Sales Overview - Last 7 Months
    today = timezone.localdate()
    months = []
    year = today.year
    month = today.month
    for i in range(7):
        months.append((year, month))
        month -=1
        if month == 0:
            month = 12
            year -= 1
    months.reverse()
    first_year, first_month = months[0]
    first_month_date = timezone.make_aware(datetime(first_year, first_month, 1))
    monthly_sales = (Order.objects.filter(is_ordered=True, created_at__gte=first_month_date)).annotate(month=TruncMonth("created_at")).values("month").annotate(total=Sum("order_total")).order_by("month")

    sales_map = {}
    for sale in monthly_sales:
        sale_date = sale["month"].date().replace(day=1)
        sales_map[sale_date] = sale["total"] or 0

    sales_overview = []
    for year, month in months:
        month_date = datetime(year, month, 1).date()
        revenue = sales_map.get(month_date, 0)
        sales_overview.append({
            "month": month_date.strftime("%b"),
            "revenue": revenue,
        })
    # Maximum revenue for bar height
    max_revenue = max(
        [item["revenue"] for item in sales_overview],
        default=0
    )
    for item in sales_overview:
        if max_revenue > 0:
            item["height"] = int(
                (float(item["revenue"]) / float(max_revenue)) * 100
            )
        else:
            item["height"] = 0

    new_orders = Order.objects.filter(is_ordered=True, status="New").count()
    accepted_orders = Order.objects.filter(is_ordered=True,status="Accepted").count()
    completed_orders = Order.objects.filter(is_ordered=True,status="Completed").count()
    cancelled_orders = Order.objects.filter(is_ordered=True,status="Cancelled").count()
    order_status_total = (new_orders + accepted_orders + completed_orders + cancelled_orders)
##========================================================================

    context = {
        "total_products": total_products,
        "total_customers": total_customers,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "pending_orders": pending_orders,
        "recent_orders": recent_orders,
        "low_stock_products": low_stock_products,

        # Sales
        "sales_overview": sales_overview,

        # Order status
        "order_status_total": order_status_total,
        "new_orders": new_orders,
        "accepted_orders": accepted_orders,
        "completed_orders": completed_orders,
        "cancelled_orders": cancelled_orders,
    }
    return render(request, "admin_dashboard/dashboard.html", context)

def admin_products(request):
    keyword = request.GET.get("keyword", "").strip()
    category = request.GET.get("category", "").strip()
    selected_category = category if category.isdecimal() else ""
    stock_status = request.GET.get("stock", "").strip()
    status = request.GET.get("status", "").strip()

    products = Product.objects.all()

    if keyword:
        products = products.filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword) | Q(category__category_name__icontains=keyword))

    if selected_category:
        products = products.filter(category__id=selected_category)
    if stock_status == "in_stock":
        products = products.filter(stock__gte=0)
    elif stock_status == "low_stock":
        products = products.filter(stock__gt=0, stock__lt=10)
    elif stock_status == "out_of_stock":
        products = products.filter(stock=0)
    if status == "active":
        products = products.filter(is_available=True)
    elif status == "inactive":
        products = products.filter(is_available=False)

    products = products.order_by("-created_at")

    paginator = Paginator(products, 10)
    paged_products = paginator.get_page(request.GET.get("page"))

    total_products = Product.objects.count()
    available_products_count = Product.objects.filter(is_available=True).count()
    low_stock = Product.objects.filter(stock__gt=0, stock__lt=10).count()
    out_of_stock = Product.objects.filter(stock=0).count()
    categories = Category.objects.all().order_by("category_name")

    context = {
        "products": paged_products,
        "total_products": total_products,
        "available_products_count": available_products_count,
        "low_stock": low_stock,
        "out_of_stock": out_of_stock,

        "categories": categories,
        "keyword": keyword,
        "selected_category": selected_category,
        "selected_stock": stock_status,
        "selected_status": status
    }
    return render(request, "admin_dashboard/products.html", context)


def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("admin_products")
    else:
        form = ProductForm()
    context = {
        "form": form
    }
    return render(request, "admin_dashboard/add_products.html", context)

def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == "POST":
        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product,  # update only exiting product
        )
        if form.is_valid():
            form.save()
            return redirect("admin_products")
    else:
        form = ProductForm(instance=product)
    context = {
        "form": form,
        "product": product
    }
    return render(request, "admin_dashboard/edit_product.html", context)

def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == "POST":
        product.delete()
        return redirect("admin_products")
    return redirect("admin_products")

def admin_payments(request):
    return render(request, "admin_dashboard/payments.html")



def admin_customers(request):
    return render(request, "admin_dashboard/customers.html")

def admin_orders(request):
    orders = Order.objects.filter(is_ordered=True).order_by("-created_at")
    new_orders_count = orders.filter(status="New").count()
    accepted_orders_count = orders.filter(status="Accepted").count()
    completed_orders_count = orders.filter(status="Completed").count()
    canceled_orders_count = orders.filter(status="Cancelled").count()
    context = {
        "orders": orders,
        "new_orders_count": new_orders_count,
        "accepted_orders_count": accepted_orders_count,
        "completed_orders_count": completed_orders_count,
        "canceled_orders_count": canceled_orders_count,
    }
    return render(request, "admin_dashboard/orders.html", context)


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_products = order.items.all()

    if request.method == "POST":
        new_status = request.POST.get("status")

        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f"Order status updated to {order.status}.")
        else:
            messages.error(request, "Invalid status selected.")

        # Return to the orders list after updating the status
        return redirect("admin_orders")

    context = {
        "order": order,
        "order_products": order_products,
        "status_choices": Order.STATUS_CHOICES,
    }
    return render(request, "admin_dashboard/order_detail.html", context)


# def admin_products(request):
#     return render(request, "admin_dashboard/banners.html")

def admin_banner(request):
    return render(request, "admin_dashboard/banners.html")

def admin_category(request):
    return render(request, "admin_dashboard/categories.html")