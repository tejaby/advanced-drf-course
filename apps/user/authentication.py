from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework import exceptions


"""
Autenticación personalizada que hereda de la clase TokenAuthentication
- Extiende la autenticación basada en tokens para incluir una verificación de tiempo de expiración en el token de autenticación

"""


class ExpiringTokenAuthentication(TokenAuthentication):

    def has_token_expires(self, token):
        token_expired = timezone.now() - token.created - timezone.timedelta(seconds=10)
        # Verificar si el token ha caducado
        if token_expired:
            print('El token ha caduc')
            token.delete()
            token = Token.objects.create(user=token.user)
            return token

    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
            token = self.has_token_expires(token)
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        return token.user, token
