from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as DefaultUser
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.http import JsonResponse

def current_user_profile(request):
    # Example implementation
    return JsonResponse({"message": "Current user profile"})

# ============================================================================
# 🔐 Serializer para registrar usuarios
# ============================================================================


class UserSerializer(ModelSerializer):
    class Meta:
        model = DefaultUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        if DefaultUser.objects.filter(username=validated_data['username']).exists():
            raise ValidationError("El usuario ya existe")
        user = DefaultUser.objects.create_user(**validated_data)
        user.is_active = True
        user.save()
        return user

    def validate_password(self, value):
        try:
            from django.contrib.auth.password_validation import validate_password
            validate_password(value)
        except DjangoValidationError as e:
            raise ValidationError(e.messages)
        return value

# ============================================================================
# 🔄 Desactiva CSRF para ciertas vistas (solo en desarrollo)
# ============================================================================

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # Desactiva CSRF check

# ============================================================================
# 📩 Registro de usuario con respuesta JWT
# ============================================================================

class RegisterUser(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Usuario creado con éxito',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ============================================================================
# 🔐 Login personalizado con mensajes específicos de error
# ============================================================================

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed('El usuario no existe')

        if not user.check_password(password):
            raise AuthenticationFailed('Contraseña incorrecta')

        if not user.is_active:
            raise AuthenticationFailed('Cuenta inactiva, contacta al administrador')

        data = super().validate(attrs)
        data['username'] = user.username
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# ============================================================================
# 🖼️ Vistas HTML para frontend
# ============================================================================

def index(request):
    return render(request, 'users/index.html')

def register_view(request):
    return render(request, 'users/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Inicia sesión
            return redirect('profile')  # Redirige al perfil
        else:
            return render(request, 'users/login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'users/login.html')

def profile_view(request):
    return render(request, 'users/profile.html')
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    return Response({
        'username': user.username,
        'email': user.email
    })
"""

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email
    })