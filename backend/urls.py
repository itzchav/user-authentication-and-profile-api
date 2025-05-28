from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),

    # Rutas para vistas HTML
    path('', include('users.urls')),

    # Rutas para API REST
    path('api/users/', include('users.api_urls')),

    # JWT token endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', include('users.urls')),
    #path('api/', include('tasks.urls')),


]

