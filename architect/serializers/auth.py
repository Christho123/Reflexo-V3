from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError(_('Se requieres email y contraseña.'))

        # Buscar usuario por email y verificar contraseña
        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                user = None
        except User.DoesNotExist:
            user = None

        if user is None:
            raise AuthenticationFailed(_('Credenciales inválidas.'))
        
        if not user.is_active:
            raise AuthenticationFailed(_('Cuenta no activada.'))
        
        refresh = RefreshToken.for_user(user)

        return {
            'email': user.email,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
        }


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, required=True)
    user_name = serializers.CharField(required=True, max_length=150)
    document_number = serializers.CharField(required=True, max_length=255)

    class Meta:
        model = User
        fields = ('user_name', 'email', 'document_number', 'password', 'password_confirm')

    def validate_password(self, value):
        # Validación personalizada de contraseña
        if len(value) < 8:
            raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        
        # Verificar que no sea una contraseña común
        common_passwords = ['password', '123456', '12345678', 'qwerty', 'abc123', 'password123', 'admin', 'letmein']
        if value.lower() in common_passwords:
            raise serializers.ValidationError("Esta contraseña es demasiado común. Elige una contraseña más segura.")
        
        return value

    def validate_document_number(self, value):
        if not value:
            raise serializers.ValidationError("El número de documento es obligatorio.")
        
        # Verificar que sea único
        if User.objects.filter(document_number=value).exists():
            raise serializers.ValidationError("Este número de documento ya está registrado.")
        
        return value

    def validate_user_name(self, value):
        if not value:
            raise serializers.ValidationError("El nombre de usuario es obligatorio.")
        
        # Verificar que sea único
        if User.objects.filter(user_name=value).exists():
            raise serializers.ValidationError("Este nombre de usuario ya está registrado.")
        
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Las contraseñas no coinciden"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        user.is_active = True  # Asegurar que el usuario esté activo
        user.save()
        return user 