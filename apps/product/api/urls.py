from django.urls import path

from apps.product.api.views.general_views import CategoryListAPIView
from apps.product.api.views.product_views import ProductListAPIView, ProductCreateAPIView, ProductRetrieveAPIView, ProductDestroyAPIView, ProductUpdateAPIView, ProductListCreateAPIView, ProductRetrieveUpdateAPIView


urlpatterns = [
    path('category/', CategoryListAPIView.as_view(), name='category'),
    path('product/list/', ProductListAPIView.as_view(), name='product_list'),
    path('product/create/', ProductCreateAPIView.as_view(), name='product_create'),
    path('product/retrieve/<int:pk>/',
         ProductRetrieveAPIView.as_view(), name='product_retrieve'),
    path('product/destroy/<int:pk>/',
         ProductDestroyAPIView.as_view(), name='product_destroy'),
    path('product/update/<int:pk>/',
         ProductUpdateAPIView.as_view(), name='product_update'),
    path('product/', ProductListCreateAPIView.as_view(), name='product'),
    path('product/<int:pk>/', ProductRetrieveUpdateAPIView.as_view(), name='product')
]
