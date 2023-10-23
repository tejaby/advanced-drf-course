from django.urls import path

from apps.product.api.views.general_views import CategoryListAPIView
from apps.product.api.views.product_views import ProductListAPIView, ProductCreateAPIView


urlpatterns = [
    path('category/', CategoryListAPIView.as_view(), name='category'),
    path('product/list/', ProductListAPIView.as_view(), name='product_list'),
    path('product/create/', ProductCreateAPIView.as_view(), name='product_create')

]
