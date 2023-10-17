from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT

from django.contrib.auth.models import User

from .serializers import UserSerializer


@api_view(['GET', 'POST'])
def user_api_view(request):
    if request.method == 'GET':
        user = User.objects.filter(is_active = True)
        user_serializer = UserSerializer(user, many=True)
        return Response(user_serializer.data)

    elif request.method == 'POST':
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data)
        return Response(user_serializer.errors)

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail_api_view(request, user_id):

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)
    
    elif request.method == 'PUT':
        user_serializer = UserSerializer(user, data = request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data)
        return Response(user_serializer.errors)

    # elif request.method == 'DELETE':
    #     user.is_active = False
    #     user.save()
    #     return Response(status=HTTP_204_NO_CONTENT)
    
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=HTTP_204_NO_CONTENT)
    

