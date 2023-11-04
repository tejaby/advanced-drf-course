from rest_framework import routers

from apps.user.api.api import UserViewSet

router = routers.DefaultRouter()

router.register(r'usuario', UserViewSet, basename='usuario')