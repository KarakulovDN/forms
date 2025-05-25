from django.urls import path
from .views import (ProductListView, ProductCreateView,
                   ProductUpdateView, ProductDetailView, ProductDeleteView)

app_name = 'catalog'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
]