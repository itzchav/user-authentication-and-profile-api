from django.urls import include, path
from .views import RegisterUser, login_view, register_view, index, profile_view,user_profile

urlpatterns = [
    path('', index, name='index'),  # Página principal HTML
    path('register/', register_view, name='register'),  # Mostrar formulario HTML
    path('login/', login_view, name='login'),  # Mostrar formulario HTML
    path('profile/', profile_view, name='profile'),  # 👈 Nuevo endpoint seguro
    path('me/', user_profile, name='user-profile'),
    #path('api/users/', include('users.urls')),
    path('api/', include('tasks.urls')),  # <- agrega esta línea para incluir tasks


    #path('api/users/', include('users.urls')),


]
