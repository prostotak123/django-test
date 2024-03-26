from django.shortcuts import render
from django.db.models import Count

# Create your views here.
from core.models import Product, Category, Vendor


def index(request):
    products = Product.objects.filter(product_status="published", featured=True)
    context = {"products": products}
    return render(request, "core/index.html", context)


def product_list_view(request):
    products = Product.objects.filter()
    context = {"products": products}
    return render(request, "core/shop.html", context)


def category_list_view(request):
    # categories = Category.objects.all()
    categories = Category.objects.all().annotate(product_count=Count("category"))
    context = {"categories": categories}
    return render(request, "core/category-list.html", context)


def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(
        product_status="published", featured=True, category=category
    )
    context = {"category": category, "products": products}
    return render(request, "core/category-product-list.html", context)


def vendor_list_view(request):
    vendor = Vendor.objects.all()
    context = {"vendors": vendor}
    
    return render(request, "core/vendor-list.html", context)
