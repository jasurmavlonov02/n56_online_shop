from typing import Optional
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View

from shop.models import Product, Category, Order, Comment
from shop.forms import OrderForm, ProductModelForm, CommentModelForm

from django.views.generic import CreateView, DetailView


# Create your views here.


def index(request, slug=None):
    search_query = request.GET.get('q', '')
    filter_type = request.GET.get('filter', '')
    categories = Category.objects.all()

    if slug:
        if filter_type == 'expensive':
            products = Product.objects.filter(category__slug=slug).order_by('-price')[:5]
        elif filter_type == 'cheap':
            products = Product.objects.filter(category__slug=slug).order_by('price')[:5]
        elif filter_type == 'rating':
            products = Product.objects.filter(category__slug=slug, rating__gte=4).order_by('-rating')

        else:
            products = Product.objects.filter(category__slug=slug)

    else:
        if filter_type == 'expensive':
            products = Product.objects.all().order_by('-price')[:5]
        elif filter_type == 'cheap':
            products = Product.objects.all().order_by('price')[:5]
        elif filter_type == 'rating':
            products = Product.objects.filter(rating__gte=4).order_by('-rating')

        else:
            products = Product.objects.all()

    if search_query:
        products = Product.objects.filter(name__icontains=search_query)

    paginator = Paginator(products, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # .order_by('-id')

    context = {
        'page_obj': page_obj,
        'categories': categories,
    }
    return render(request, 'shop/index.html', context=context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    comments = Comment.objects.filter(product=product, is_negative=False)
    related_products = Product.objects.filter(category_id=product.category).exclude(id=product.id)

    context = {
        'product': product,
        'comments': comments,
        'related_products': related_products
    }
    return render(request, 'shop/detail.html', context=context)


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


@login_required
def product_create(request):
    # form = ProductModelForm()
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('shop:products')
    else:
        form = ProductModelForm()
    context = {
        'form': form,
        'action': 'Create New'
    }
    return render(request, 'shop/create.html', context=context)


def product_delete(request, pk):
    try:
        product = Product.objects.get(id=pk)
        product.delete()
        return redirect('shop:products')
    except Product.DoesNotExist as e:
        print(e)


def product_edit(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductModelForm(instance=product)
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('shop:product_detail', pk)
    context = {
        'form': form,
        'product': product,
        'action': 'Edit'
    }
    return render(request, 'shop/create.html', context=context)


def comment_view(request, pk):
    product = get_object_or_404(Product, id=pk)
    form = CommentModelForm()
    if request.method == 'POST':
        form = CommentModelForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.save()
            return redirect('shop:product_detail', pk)

    context = {
        'product': product,
        'form': form
    }
    return render(request, 'shop/detail.html', context=context)


# class CreateProduct(View):
#     def get(self, request):
#         form = ProductModelForm()
#         return render(request, 'shop/create.html', {'form': form, 'action': 'Create New'})
#
#     def post(self, request):
#         form = ProductModelForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('shop:products')


class CreateProduct(CreateView):
    model = Product
    template_name = 'shop/create.html'
    form_class = ProductModelForm
    success_url = reverse_lazy('shop:products')

    # def get_success_url(self):
    #     return reverse_lazy('shop:products')


class DetailProduct(DetailView):
    model = Product
    template_name = 'shop/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        context['product'] = product
        context['comments'] = Comment.objects.filter(product=product, is_negative=False)
        context['related_products'] = Product.objects.filter(category_id=product.category).exclude(id=product.id)
        return context
