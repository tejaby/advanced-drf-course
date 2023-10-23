from django.urls import path

from apps.product.api.views.general_views import CategoryListAPIView
from apps.product.api.views.product_views import ProductListAPIView, ProductCreateAPIView, ProductRetrieveAPIView, ProductDestroyAPIView


urlpatterns = [
    path('category/', CategoryListAPIView.as_view(), name='category'),
    path('product/list/', ProductListAPIView.as_view(), name='product_list'),
    path('product/create/', ProductCreateAPIView.as_view(), name='product_create'),
    path('product/retrieve/<int:pk>',
         ProductRetrieveAPIView.as_view(), name='product_retrieve'),
    path('product/destroy/<int:pk>',
         ProductDestroyAPIView.as_view(), name='destroy'),


]
