from django.urls import path
from .views import RegisterUser, LoginView

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='api_register'),
    path('login/', LoginView.as_view(), name='api_login'),

    # Puedes agregar más endpoints API aquí
]
