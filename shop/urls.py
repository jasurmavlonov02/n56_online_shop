from django.contrib import admin
from django.urls import path

from shop import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='products'),
    path('detail/<int:pk>/', views.DetailProduct.as_view(), name='product_detail'),
    path('category-detail/<slug:slug>/', views.index, name='products_of_category'),
    path('order-detail/<int:pk>/save/', views.order_detail, name='order_detail'),
    path('create-product/', views.CreateProduct.as_view(), name='product_create'),
    path('delete-product/<int:pk>/', views.product_delete, name='product_delete'),
    path('edit-product/<int:pk>/', views.product_edit, name='product_edit'),
    path('product-comments/<int:pk>/', views.comment_view, name='comment_view')
]
