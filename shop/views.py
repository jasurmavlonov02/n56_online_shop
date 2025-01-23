from typing import Optional

from django.shortcuts import render, get_object_or_404

from shop.models import Product, Category


# Create your views here.


def index(request, category_id: Optional[int] = None):
    categories = Category.objects.all()

    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'shop/index.html', context=context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    # product = Product.objects.get(id=pk)

    return render(request, 'shop/detail.html', {'product': product})
