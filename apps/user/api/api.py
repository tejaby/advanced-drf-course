from rest_framework.decorators import api_view, action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from rest_framework import permissions
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User

from .serializers import UserSerializer, UserListSerializer, UpdateUserSerializer, UserPasswordSerializer
# from .serializers import TestUserSerializer

"""
Vista basada en funciones para el listado, obtencion, crecion, actualizacion y eliminacion de producto
- Se definen los metodos permitidos con el decorador api_view para cada vista


"""

@api_view(['GET', 'POST'])
def user_api_view(request):
    if request.method == 'GET':
        user = User.objects.filter(is_active=True).values(
            'id', 'username', 'email', 'first_name', 'last_name')
        user_serializer = UserListSerializer(user, many=True)

        return Response(user_serializer.data, status=HTTP_200_OK)

    elif request.method == 'POST':
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=HTTP_201_CREATED)
        return Response(user_serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail_api_view(request, user_id):

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'message': 'user not found'}, status=HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data, status=HTTP_200_OK)

    elif request.method == 'PUT':
        user_serializer = UserSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=HTTP_200_OK)
        return Response(user_serializer.errors, status=HTTP_400_BAD_REQUEST)

    # elif request.method == 'DELETE':
    #     user.is_active = False
    #     user.save()
    #     return Response(status=HTTP_204_NO_CONTENT)

    elif request.method == 'DELETE':
        user.delete()
        return Response({'message': 'usuario eliminado exitosamente'}, status=HTTP_200_OK)


"""
Vista basada en clase GenericViewSet para el listado, obtencion, crecion, actualizacion y eliminacion de producto
- Se definen los metodos listar, retrieve, create, update, delete y funciones extras para el usuario
- Se utiliza el decorador action para convertir funciones en vistas validas para tener una ruta en el viewset
- la propiedad detail en el decorador hace que la ruta sea tipo manipulación de una instancia específica de un objeto
- Si detail es False se refiere a una operación que afecta a una colección de objetos o no requiere un objeto específico
- url_path se utiliza si se decea personalizar la parte de la URL que corresponde a una acción personalizada

"""


class UserViewSet(viewsets.GenericViewSet):
    model = User
    serializer_class = UserSerializer
    list_serializer_class = UserListSerializer
    # authentication_classes = []
    # permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        if self.queryset is None:
            return self.serializer_class().Meta.model.objects.filter(is_active=True).values('id', 'username', 'email', 'first_name', 'last_name')
        return self.queryset

    def get_object(self, pk):
        instance = get_object_or_404(self.model, id=pk)
        return instance

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.list_serializer_class(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, *args, **kwargs):
        instance = self.get_object(pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        instance = self.get_object(pk)
        serializer = UpdateUserSerializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        instance = User.objects.filter(pk=pk).first()
        if instance:
            instance.is_active = False
            instance.save()
            return Response(status=HTTP_204_NO_CONTENT)
        return Response({'error': 'user not found'}, status=HTTP_404_NOT_FOUND)

    @action(methods=['POST'], detail=True)
    def set_password(self, request, pk=None):
        instance = self.get_object(pk)
        # se utiliza el serializador para validar que ambas passwords sean validas
        serializer = UserPasswordSerializer(data=request.data)
        if serializer.is_valid():
            # se actualiza y se encripta el password de la instancia del usuario
            instance.set_password(serializer.validated_data['password'])
            instance.save()
            return Response({'message': 'successfully updated password'}, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
