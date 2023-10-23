from django.urls import path

from apps.product.api.views.general_views import CategoryListAPIView
from apps.product.api.views.product_views import ProductListAPIView


urlpatterns = [
    path('category/', CategoryListAPIView.as_view(), name='category'),
    path('product/', ProductListAPIView.as_view(), name='product')
]
