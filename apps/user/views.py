# ObtainAuthToken
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import status

from rest_framework import permissions

from django.contrib.auth import authenticate

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.authtoken.models import Token
from apps.user.api.serializers import UserTokenSerializer


from apps.user.authentication import ExpiringTokenAuthentication

"""
Vista basada en clase ObtainAuthToken para la autenticacion de usuarios y creacion de tokens
- se puede utlizar tanto el serializer que ObtainAuthToken tiene definido o usar UserLoginSerializer
- Se envía la solicitud en el contexto ya que el serializador AuthTokenSerializer utiliza autenticación.

"""


class CustomLoginView(ObtainAuthToken):
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


"""
Vista basada en clase APIView para la autenticacion de usuarios y eliminacion de tokens
- Permite la autenticación mediante el envío de tokens en los encabezados de la solicitud.
- Utiliza ExpiringTokenAuthentication para validar tokens y renovarlos si han caducado.
-request.user para representar al usuario autenticado. Además, establecerá 
-request.auth para contener información relacionada con la autenticación, como el token  

"""


class CustomLogoutView(APIView):
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        token = request.auth
        if token:
            token.delete()
            return Response({'message': 'Token deleted successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'no token found'}, status=status.HTTP_400_BAD_REQUEST)


"""
Vista basada en clase APIView para verificar la validez de un token de usuario.
- Utiliza ExpiringTokenAuthentication para validar tokens.
- Responde si el token es válido y proporciona el token en caso afirmativo.

"""


class CustomTokenRefreshView(APIView):
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        token = request.auth
        if token:
            return Response({'message': 'token is valid', 'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'no token found'}, status=status.HTTP_401_UNAUTHORIZED)


"""
Vista basada en clase TokenObtainPairView para la autenticacion de usuarios y creacion de tokens con simplejwt
- Utiliza el serializador que proporciona la clase TokenObtainPairView para autenticar al usuario y generar tokens.
- Si el usuario es válido, se retorna el token de acceso y el token de refresco, junto con la información del usuario.

"""


class CustomTokenObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        user = authenticate(
            username=request.data['username'], password=request.data['password'])
        if user is not None:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                user_serializer = UserTokenSerializer(user)
                return Response({'access': serializer.validated_data['access'], 'refresh': serializer.validated_data['refresh'], 'user': user_serializer.data}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)
    
"""
Vista basada en clase APIView para la validación del usuario y revocación del token de refresco.
- Se debe de enviar el token de acceso en los headers Authorization Bearer token_access
- El método RefreshToken recibe el token de refresco y devuelve la instancia si es válido.
- El método blacklist() en el objeto RefreshToken se utiliza para invalidar el token de refresco.

"""


class CustomLogoutPairView(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Cierre de sesión exitoso"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Token de refresco inválido"}, status=status.HTTP_400_BAD_REQUEST)
