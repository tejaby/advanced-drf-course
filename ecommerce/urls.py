"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

# custom views login, logout, refresh authtoken
from apps.user.views import CustomLoginView, CustomLogoutView, CustomTokenRefreshView, CustomTokenObtainPairView, CustomLogoutPairView

# custom views login, logout simplejwt
from apps.user.views import CustomTokenObtainPairView, CustomLogoutPairView


# views that rest_framework_simplejwt provides
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # authtoken
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='refresh'),
    # simplejwt default views
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # simplejwt
    path('api/login/', CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),
    path('api/logout/', CustomLogoutPairView.as_view(), name='custom_logout_pair'),
    # user app views
    path('user/', include('apps.user.api.urls')),
    # product app views
    path('product/', include('apps.product.api.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
