from apps.base.api import GeneralListAPIView

from apps.product.api.serializers.product_serializers import ProductSerializer


class ProductListAPIView(GeneralListAPIView):
    serializer_class = ProductSerializer
