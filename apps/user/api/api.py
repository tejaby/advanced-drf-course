from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User

from .serializers import UserSerializer, UserListSerializer, UpdateUserSerializer
# from .serializers import TestUserSerializer


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


class UserViewSet(viewsets.GenericViewSet):
    model = User
    serializer_class = UserSerializer
    list_serializer_class = UserListSerializer

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
        serializer = UpdateUserSerializer(instance, data=request.data, partial=True)
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