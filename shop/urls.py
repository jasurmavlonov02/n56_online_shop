from django.contrib import admin
from django.urls import path

from shop import views

urlpatterns = [
    path('', views.index, name='products'),
    path('detail/', views.product_detail, name='product_detail'),
]
