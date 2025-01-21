from django.shortcuts import render, get_object_or_404

from shop.models import Product


# Create your views here.


def index(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'shop/index.html', context=context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    # product = Product.objects.get(id=pk)

    return render(request, 'shop/detail.html', {'product': product})
