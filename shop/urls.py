from django.contrib import admin
from django.urls import path

from shop import views

urlpatterns = [
    path('', views.index, name='products'),
    path('detail/<int:pk>/', views.product_detail, name='product_detail'),
    path('category-detail/<int:category_id>/', views.index, name='products_of_category')
]
