from rest_framework.generics import CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from apps.base.api import GeneralListAPIView

from apps.product.api.serializers.product_serializers import ProductSerializer

from apps.product.models import Product


class ProductListAPIView(GeneralListAPIView):
    serializer_class = ProductSerializer


class ProductCreateAPIView(CreateAPIView):
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'product created successfully'}, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ProductRetrieveAPIView(RetrieveAPIView):
    # queryset = Product.objects.filter(state=True) # usando atributo queryset
    serializer_class = ProductSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state=True)


class ProductDestroyAPIView(DestroyAPIView):
    # queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state=True)

    def delete(self, request, pk=None):
        # product = self.get_queryset().filter(id=pk).first()
        # usando el metodo get_object obtenemos el objeto basado en el valor pk
        product = self.get_object()
        if product:
            product.state = False
            product.save()
            return Response({'message': 'Product deleted successfully'}, status=HTTP_200_OK)
        return Response({'message': 'Product not found'})


class ProductUpdateAPIView(UpdateAPIView):
    serializer_class = ProductSerializer
    # queryset = Product.objects.all()

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state=True)

    def patch(self, request, pk=None):
        instance = self.get_queryset().filter(id=pk).first()
        if instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=HTTP_200_OK)
        return Response({'message': 'Product not found'})

    def put(self, request, pk=None):
        instance = self.get_queryset().filter(id=pk).first()
        if instance:
            serializer = self.get_serializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTP_200_OK)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
