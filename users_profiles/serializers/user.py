from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
import os

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer para lectura completa del modelo User.
    
    Incluye campos calculados como nombre completo y URL de foto de perfil.
    Usado principalmente para mostrar información del usuario.
    """
    
    full_name = serializers.SerializerMethodField()  # Nombre completo calculado
    profile_photo_url = serializers.SerializerMethodField()  # URL de foto de perfil
    
    class Meta:
        model = User
        fields = [
            'id', 'user_name', 'email', 'name', 'paternal_lastname', 'maternal_lastname',
            'full_name', 'phone', 'account_statement', 'is_active', 'date_joined', 'last_login',
            'profile_photo_url', 'document_number', 'document_type', 'sex', 'country'
        ]
        read_only_fields = ['id', 'user_name', 'date_joined', 'last_login', 'account_statement']
    
    def get_full_name(self, obj):
        """Retorna el nombre completo del usuario"""
        return f"{obj.name} {obj.paternal_lastname} {obj.maternal_lastname}".strip()
    
    def get_profile_photo_url(self, obj):
        """Retorna la URL de la foto de perfil"""
        if obj.photo_url:
            request = self.context.get('request')
            if request:
                try:
                    return request.build_absolute_uri(obj.photo_url.url)
                except Exception:
                    # Fallback: retornar solo el nombre del archivo
                    return str(obj.photo_url)
            else:
                return str(obj.photo_url)
        return None

class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer para actualización de datos básicos del usuario.
    
    Permite actualizar nombre, apellido y teléfono.
    No incluye campos sensibles como email o username.
    """
    
    class Meta:
        model = User
        fields = [
            'name', 'paternal_lastname', 'maternal_lastname', 'phone'
        ]
    
    def validate_phone(self, value):
        """Valida el formato del número de teléfono."""
        if value:
            # Validación básica de longitud mínima
            if len(value) < 7:
                raise serializers.ValidationError("El número de teléfono debe tener al menos 7 dígitos")
        return value
    
    def update(self, instance, validated_data):
        """Actualiza los campos básicos del usuario."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer para registro de nuevos usuarios.
    
    Incluye validación de contraseñas, verificación de unicidad
    de email y username, y creación segura del usuario.
    """
    
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],  # Validación de Django para contraseñas
        help_text='La contraseña debe cumplir con los requisitos de seguridad'
    )
    
    password_confirm = serializers.CharField(
        write_only=True,
        help_text='Confirma tu contraseña'
    )
    
    class Meta:
        model = User
        fields = [
            'user_name', 'email', 'password', 'password_confirm',
            'name', 'paternal_lastname', 'maternal_lastname'
        ]
    
    def validate(self, attrs):
        """Validación completa para el registro de usuario."""
        # Verificar que las contraseñas coincidan
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        
        # Verificar unicidad del email
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError("Este email ya está registrado")
        
        # Verificar que el username no esté en uso
        if User.objects.filter(user_name=attrs['user_name']).exists():
            raise serializers.ValidationError("Este nombre de usuario ya está en uso")
        
        return attrs
    
    def create(self, validated_data):
        """Crea un nuevo usuario con contraseña encriptada."""
        validated_data.pop('password_confirm')  # Remover confirmación
        user = User.objects.create_user(**validated_data)
        return user

class UserProfilePhotoSerializer(serializers.ModelSerializer):
    """Serializer para actualización de la foto de perfil del usuario.
    
    Maneja la subida de imágenes y eliminación de fotos anteriores
    para evitar acumulación de archivos no utilizados.
    """
    
    photo = serializers.ImageField(
        required=False,
        allow_null=True,
        help_text='Archivo de imagen para la foto de perfil'
    )
    
    class Meta:
        model = User
        fields = ['photo']
    
    def update(self, instance, validated_data):
        """Actualiza la foto de perfil del usuario"""
        photo = validated_data.get('photo')
        
        if photo:
            print(f"DEBUG: Subiendo foto: {photo}")
            
            # Eliminar foto anterior si existe
            if instance.photo_url:
                try:
                    if os.path.isfile(instance.photo_url.path):
                        os.remove(instance.photo_url.path)
                        print(f"DEBUG: Foto anterior eliminada")
                except (ValueError, AttributeError):
                    pass
            
            # Guardar la nueva imagen
            instance.photo_url = photo
            instance.save()
            
            # Refrescar para obtener la URL actualizada
            instance.refresh_from_db()
            print(f"DEBUG: Foto guardada: {instance.photo_url}")
            
            # Generar la URL completa
            request = self.context.get('request')
            if request and instance.photo_url:
                try:
                    photo_url = request.build_absolute_uri(instance.photo_url.url)
                    instance._photo_url_full = photo_url
                    print(f"DEBUG: URL completa: {photo_url}")
                except Exception as e:
                    print(f"DEBUG: Error construyendo URL: {e}")
                    instance._photo_url_full = str(instance.photo_url)
        else:
            # Si no se proporciona foto, eliminar la existente
            if instance.photo_url:
                try:
                    if os.path.isfile(instance.photo_url.path):
                        os.remove(instance.photo_url.path)
                except (ValueError, AttributeError):
                    pass
                
                instance.photo_url = None
                instance.save()
                print("DEBUG: Foto eliminada")
        
        return instance