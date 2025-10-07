from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import update_last_login

class PasswordChangeSerializer(serializers.Serializer):
    """Serializer para cambio de contraseña con verificación de contraseña actual"""
    
    # Campo para la contraseña actual del usuario
    current_password = serializers.CharField(
        write_only=True,
        help_text='Tu contraseña actual'
    )
    
    # Nueva contraseña con validación automática de Django
    new_password = serializers.CharField(
        write_only=True,
        validators=[validate_password],  # Aplica validaciones de Django
        help_text='Tu nueva contraseña'
    )
    
    # Confirmación de la nueva contraseña
    new_password_confirm = serializers.CharField(
        write_only=True,
        help_text='Confirma tu nueva contraseña'
    )
    
    def validate_current_password(self, value):
        """Valida que la contraseña actual sea correcta"""
        user = self.context['request'].user
        # Verificar que la contraseña actual coincida
        if not user.check_password(value):
            raise serializers.ValidationError("La contraseña actual es incorrecta")
        return value
    
    def validate(self, attrs):
        """Validación personalizada para el cambio de contraseña"""
        # Verificar que las nuevas contraseñas coincidan
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Las nuevas contraseñas no coinciden")
        
        # Evitar que la nueva contraseña sea igual a la actual
        if attrs['current_password'] == attrs['new_password']:
            raise serializers.ValidationError("La nueva contraseña debe ser diferente a la actual")
        
        return attrs
    
    def save(self):
        """Cambia la contraseña del usuario"""
        user = self.context['request'].user
        # Establecer la nueva contraseña (se hashea automáticamente)
        user.set_password(self.validated_data['new_password'])
        user.save()
        
        # Actualizar la última fecha de login para mantener la sesión
        update_last_login(None, user)
        
        return user

class PasswordResetSerializer(serializers.Serializer):
    """Serializer para solicitar restablecimiento de contraseña"""
    
    # Email del usuario que solicita el restablecimiento
    email = serializers.EmailField(
        help_text='Email asociado a tu cuenta'
    )
    
    def validate_email(self, value):
        """Valida el formato del email (no verifica existencia por seguridad)"""
        # Solo validar formato, no existencia
        # La existencia se maneja en la vista sin revelar si existe o no
        return value

class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer para confirmar el restablecimiento de contraseña"""
    
    # Código de verificación enviado por email
    code = serializers.CharField(
        max_length=6,
        help_text='Código de verificación de 6 dígitos'
    )
    
    # Nueva contraseña con validación
    new_password = serializers.CharField(
        write_only=True,
        validators=[validate_password],  # Validaciones de seguridad de Django
        help_text='Tu nueva contraseña'
    )
    
    # Confirmación de la nueva contraseña
    new_password_confirm = serializers.CharField(
        write_only=True,
        help_text='Confirma tu nueva contraseña'
    )
    
    def validate(self, attrs):
        """Validación personalizada para el restablecimiento de contraseña"""
        # Verificar que ambas contraseñas coincidan
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return attrs


class PasswordStrengthSerializer(serializers.Serializer):
    """Serializer para validar la fortaleza de una contraseña"""
    
    # Contraseña a evaluar
    password = serializers.CharField(
        help_text='Contraseña a validar'
    )
    
    def validate_password(self, value):
        """Valida la fortaleza de la contraseña"""
        try:
            # Usar las validaciones de Django para evaluar fortaleza
            validate_password(value)
        except serializers.ValidationError as e:
            # Re-lanzar los errores de validación
            raise serializers.ValidationError(e.messages)
        return value


class PasswordHistorySerializer(serializers.Serializer):
    """Serializer para historial de cambios de contraseña"""
    
    # Fecha y hora del cambio
    changed_at = serializers.DateTimeField(
        read_only=True,
        help_text='Fecha del cambio de contraseña'
    )
    
    # IP desde donde se realizó el cambio (para auditoría)
    ip_address = serializers.CharField(
        read_only=True,
        help_text='Dirección IP desde donde se cambió la contraseña'
    )
    
    # Información del navegador/dispositivo (para auditoría)
    user_agent = serializers.CharField(
        read_only=True,
        help_text='Navegador/dispositivo utilizado'
    )