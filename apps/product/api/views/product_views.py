from rest_framework.generics import CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from apps.base.api import GeneralListAPIView

from apps.product.api.serializers.product_serializers import ProductSerializer

from apps.product.models import Product

"""
Vista basada en clase ListAPIView para el listado de productos
- ProductListAPIView hereda la funcionalidad de GeneralListAPIView

"""


class ProductListAPIView(GeneralListAPIView):
    serializer_class = ProductSerializer


"""
Vista basada en clase CreateAPIView para la creacion de productos
- Se sobrescribe el metodo post para procesar la solicitud de creación de productos

"""


class ProductCreateAPIView(CreateAPIView):
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'product created successfully', 'product': serializer.data}, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


"""
Vista basada en clase RetrieveAPIView para la obtención de producto
- la queryset se define usando el metodo get_queryset en lugar de usar el atributo queryset

"""


class ProductRetrieveAPIView(RetrieveAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state=True)


"""
Vista basada en clase DestroyAPIView para la eliminacion de productos
- Se sobrescribe el metodo delete para una eliminacion logica para producto
- Usando el metodo get_object obtenemos el objeto basado en el valor pk

"""


class ProductDestroyAPIView(DestroyAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state=True)

    def delete(self, request, pk=None):
        # product = self.get_queryset().filter(id=pk).first()
        product = self.get_object()
        if product:
            product.state = False
            product.save()
            return Response({'message': 'Product deleted successfully'}, status=HTTP_200_OK)
        return Response({'message': 'Product not found'})


"""
Vista basada en clase UpdateAPIView para la actualizacion de productos
- Se sobrescribe el metodo update para procesar la solicitud de actualizacion de productos
- Usando el metodo get_object obtenemos el objeto basado en el valor pk

"""


class ProductUpdateAPIView(UpdateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state=True)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


"""
Vista basada en clase ListCreateAPIView para el listado y creacion de productos
- Se sobrescribe el metodo get para procesar la solicitud de listado de productos
- Se sobrescribe el metodo post para procesar la solicitud de creación de productos

"""


class ProductListCreateAPIView(ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = ProductSerializer.Meta.model.objects.filter(state=True)

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'product created successfully', 'product': serializer.data}, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


"""
Vista basada en clase RetrieveUpdateAPIView para la obtención y actualizacion de productos
- Se sobrescribe el metodo put para procesar la solicitud de actualizacion de productos

"""

# class ProductRetrieveUpdateAPIView(RetrieveUpdateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     def put(self, request, pk, *args, **kwargs):
#         # instance = self.get_object()
#         instance = self.get_queryset().filter(id=pk).first()
#         serializer = self.get_serializer(
#             instance, data=request.data, partial=True)  # permite actualizaciones parciales
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=HTTP_200_OK)
#         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


"""
Vista basada en clase RetrieveUpdateDestroyAPIView para la obtención, actualizacion y eliminacion de productos
- la queryset se define usando el metodo get_queryset en lugar de usar el atributo queryset
- En el metodo get_queryset se agrego validacion si al utilizar el metodo se agrego pk.
- Se sobrescribe el metodo update para procesar la solicitud de actualizacion de productos
- Se sobrescribe el metodo delete para una eliminacion logica para producto

"""


class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state=True)
        else:
            return self.get_serializer().Meta.model.objects.filter(state=True, id=pk).first()

    def update(self, request, pk=None, *args, **kwargs):
        if self.get_queryset(pk):
            serializer = self.get_serializer(
                self.get_queryset(pk), data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTP_200_OK)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, *args, **kwargs):
        instance = self.get_queryset().filter(id=pk).first()
        if instance:
            instance.state = False
            instance.save()
            return Response({'message': 'Product deleted successfully'}, status=HTTP_200_OK)
        return Response({'message': 'Product not found'}, status=HTTP_404_NOT_FOUND)
