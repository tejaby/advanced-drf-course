from django.urls import path

from .routers import router

from .api import user_api_view, user_detail_api_view

urlpatterns = [
    path('user/', user_api_view, name='list_user'),
    path('user/<int:user_id>/', user_detail_api_view, name='detail_user'),
]

urlpatterns += router.urls