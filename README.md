# Descripción
Proyecto backend con Django y Django REST Framework que implementa autenticación básica de usuarios usando JSON Web Tokens (JWT). Permite:

Registrar usuarios (opcional para más adelante)

Iniciar sesión validando usuario y contraseña

Acceder a perfil del usuario autenticado usando token JWT

Es ideal como base para aplicaciones que requieran autenticación segura y manejo básico de usuarios.

# Funcionalidades actuales
Login: Validación de usuario y contraseña, retorna tokens JWT.

Perfil: Endpoint protegido que retorna datos del usuario autenticado.

Logout: (Implementación en frontend removiendo el token localmente)

Tecnologías usadas
Python 3

Django 5

Django REST Framework

Simple JWT para manejo de tokens

