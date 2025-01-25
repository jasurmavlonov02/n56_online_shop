from typing import Optional
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from shop.models import Product, Category, Order
from shop.forms import OrderForm, ProductModelForm


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

    return render(request, 'shop/detail.html', {'product': product})


def order_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        form = OrderForm(request.GET)
        if form.is_valid():
            full_name = request.GET.get('full_name')
            phone_number = request.GET.get('phone_number')
            quantity = int(request.GET.get('quantity'))
            if product.quantity >= quantity:
                product.quantity -= quantity
                order = Order.objects.create(
                    full_name=full_name,
                    phone_number=phone_number,
                    quantity=quantity,
                    product=product
                )
                order.save()
                product.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Order successful sent'

                )

            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Something with wrong...'
                )


    else:
        form = OrderForm()
    context = {
        'form': form,
        'product': product
    }

    return render(request, 'shop/detail.html', context)


def product_create(request):
    # form = ProductModelForm()
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = ProductModelForm()
    context = {
        'form': form,
    }
    return render(request, 'shop/create.html', context=context)


def product_delete(request, pk):
    try:
        product = Product.objects.get(id=pk)
        product.delete()
        return redirect('products')
    except Product.DoesNotExist as e:
        print(e)
