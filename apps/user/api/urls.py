from django.urls import path

from .api import UserAPIView

urlpatterns = [
    path('user', UserAPIView.as_view(), name='list_user')
]