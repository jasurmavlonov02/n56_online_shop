from django.shortcuts import render

from shop.models import Product


# Create your views here.


def index(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'shop/index.html', context=context)


def product_detail(request):
    return render(request, 'shop/detail.html')
