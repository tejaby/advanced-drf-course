# ObtainAuthToken
from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework.response import Response

from rest_framework import status

from rest_framework.authtoken.models import Token
from apps.user.api.serializers import UserLoginSerializer
from apps.user.api.serializers import UserTokenSerializer

"""
Vista basada en clase ObtainAuthToken para la autenticacion de usuarios y creacion de tokens
- se puede utlizar tanto el serializer que ObtainAuthToken tiene definido o usar UserLoginSerializer
= Se le envia la request en el contexto ya que el serializador AuthTokenSerializer utiliza authenticate

"""


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            if user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                user_serializer = UserTokenSerializer(user)
                if created:
                    return Response({'token': token.key, 'user': user_serializer.data}, status=status.HTTP_200_OK)
                else:
                    token.delete()
                    token = Token.objects.create(user=user)
            else:
                return Response({'error': 'user is not active'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'username or password is invalid'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'token': token.key, 'user': user_serializer.data}, status=status.HTTP_200_OK)
