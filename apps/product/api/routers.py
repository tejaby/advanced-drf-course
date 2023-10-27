from rest_framework import routers

from apps.product.api.views.product_views import ProductViewset, CategoryViewSet

router = routers.DefaultRouter()

router.register(r'producto', ProductViewset, basename='producto')
router.register(r'categoria', CategoryViewSet, basename='categoria')
