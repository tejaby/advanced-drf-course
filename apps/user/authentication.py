from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework import exceptions


"""
Autenticación personalizada que hereda de la clase TokenAuthentication
- Extiende la autenticación basada en tokens para incluir una verificación de tiempo de expiración en el token de autenticación

"""


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):

        try:
            token = self.get_model().objects.get(key=key)
            print(timezone.now())
        except self.get_model().DoesNotExist:
            raise exceptions.AuthenticationFailed('Token no válido')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(
                'Usuario inactivo o eliminado')

        if timezone.now() - token.created > timezone.timedelta(seconds=200):
            raise exceptions.AuthenticationFailed('Token caducado')

        return super().authenticate_credentials(key)
