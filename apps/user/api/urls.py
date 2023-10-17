from django.urls import path

from .api import user_api_view

urlpatterns = [
    path('user/', user_api_view, name='list_user'),
]