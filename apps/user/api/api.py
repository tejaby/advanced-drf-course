from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth.models import User

from .serializers import UserSerializer

class UserAPIView(APIView):

    def get(self, request):
        user = User.objects.all()
        user_serializer = UserSerializer(user, many = True)
        return Response(user_serializer.data)