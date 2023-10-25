from rest_framework import routers

from apps.product.api.views.product_views import ProductViewset

router = routers.DefaultRouter()

router.register(r'producto', ProductViewset, basename='product')
