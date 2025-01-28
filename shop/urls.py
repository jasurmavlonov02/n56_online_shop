from django.contrib import admin
from django.urls import path

from shop import views

urlpatterns = [
    path('', views.index, name='products'),
    path('detail/<int:pk>/', views.product_detail, name='product_detail'),
    path('category-detail/<int:category_id>/', views.index, name='products_of_category'),
    path('order-detail/<int:pk>/save/', views.order_detail, name='order_detail'),
    path('create-product/', views.product_create, name='product_create'),
    path('delete-product/<int:pk>/', views.product_delete, name='product_delete'),
    path('edit-product/<int:pk>/', views.product_edit, name='product_edit'),
    path('product-comments/<int:pk>/', views.comment_view, name='comment_view')
]
