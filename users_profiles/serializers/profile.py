from rest_framework import serializers
from .user import UserSerializer
from ..models.user import User

class ProfileSerializer(serializers.ModelSerializer):
    """Serializer para lectura completa del perfil de usuario.
    
    Incluye información del usuario relacionado y el porcentaje de completitud.
    Usado principalmente para mostrar el perfil completo al propietario.
    """
    
    user = UserSerializer(read_only=True)  # Información del usuario asociado
    completion_percentage = serializers.SerializerMethodField()  # Porcentaje calculado
    
    class Meta:
        model = User
        fields = [
            'id', 'user_name', 'name', 'paternal_lastname', 'maternal_lastname',
            'sex', 'email', 'phone', 'photo_url', 'document_number', 'document_type',
            'country', 'account_statement', 'is_active', 'date_joined', 'last_login',
            'completion_percentage'
        ]
        read_only_fields = ['id', 'user_name', 'date_joined', 'last_login', 'account_statement']
    
    def get_completion_percentage(self, obj):
        """Calcula y retorna el porcentaje de completitud del perfil."""
        return obj.get_completion_percentage()


class ProfileCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear un nuevo perfil de usuario.
    
    Valida que el email no esté duplicado y asocia automáticamente
    el perfil al usuario autenticado.
    """
    
    class Meta:
        model = User
        fields = [
            'name', 'paternal_lastname', 'maternal_lastname',
            'sex', 'email', 'phone', 'document_number', 'document_type', 'country'
        ]
    
    def validate_email(self, value):
        """Valida que el email no esté registrado en otro perfil."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email ya está registrado en otro perfil")
        return value
    
    def create(self, validated_data):
        """Crea un nuevo perfil asociado al usuario autenticado."""
        user = self.context['request'].user
        for attr, value in validated_data.items():
            setattr(user, attr, value)
        user.save()
        return user


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer para actualizar un perfil existente.
    
    Permite actualizar todos los campos del perfil excepto el usuario asociado.
    Valida que el email no esté en uso por otro perfil.
    """
    
    class Meta:
        model = User
        fields = [
            'name', 'paternal_lastname', 'maternal_lastname',
            'sex', 'email', 'phone', 'document_number', 'document_type', 'country'
        ]
    
    def validate_email(self, value):
        """Valida que el email no esté en uso por otro perfil."""
        user = self.context['request'].user
        # Verificar que el email no esté en uso por otro usuario (excluyendo el actual)
        if User.objects.filter(email=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("Este email ya está registrado")
        return value
    
    def update(self, instance, validated_data):
        """Actualiza los campos del perfil."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class PublicProfileSerializer(serializers.ModelSerializer):
    """Serializer para perfiles públicos sin información sensible.
    
    Filtra automáticamente la información según las configuraciones de privacidad
    del usuario. Usado para mostrar perfiles a otros usuarios.
    """
    
    user = serializers.SerializerMethodField()  # Info básica del usuario
    display_name = serializers.SerializerMethodField()  # Nombre para mostrar
    
    class Meta:
        model = User
        fields = [
            'id', 'user_name', 'display_name', 'sex', 'country',
            'photo_url', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']
    
    def get_display_name(self, obj):
        """Retorna el nombre para mostrar"""
        return f"{obj.name} {obj.paternal_lastname}".strip()


class ProfileSettingsSerializer(serializers.ModelSerializer):
    """Serializer para configuraciones de privacidad del perfil.
    
    Permite actualizar únicamente las configuraciones de visibilidad
    y notificaciones sin afectar otros datos del perfil.
    """
    
    class Meta:
        model = User
        fields = [
            'account_statement'
        ]
    
    def update(self, instance, validated_data):
        """Actualiza solo las configuraciones de privacidad."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance