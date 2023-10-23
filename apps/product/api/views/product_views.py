from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from apps.base.api import GeneralListAPIView

from apps.product.api.serializers.product_serializers import ProductSerializer

from apps.product.models import Product


class ProductListAPIView(GeneralListAPIView):
    serializer_class = ProductSerializer


class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'product created successfully'}, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ProductRetrieveAPIView(generics.RetrieveAPIView):
    # queryset = Product.objects.filter(state=True) # usando atributo queryset
    serializer_class = ProductSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state=True)


class ProductDestroyAPIView(generics.DestroyAPIView):
    # queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state=True)
    
    def delete(self, request, pk=None):
        product = self.get_queryset().filter(id=pk).first()
        print(product)
        if product:
            product.state = False
            product.save()
            return Response({'message': 'Product deleted successfully'}, status=HTTP_200_OK)
        return Response({'message': 'Product not found'})
