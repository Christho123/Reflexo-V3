# users_profiles/serializers/verification.py

from typing import List, Tuple
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

# Import del modelo (usa el directo al archivo; si reexportas en models/__init__.py
# puedes cambiar a: from ..models import UserVerificationCode)
from ..models.user_verification_code import UserVerificationCode

User = get_user_model()
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

# Import del modelo (usa el directo al archivo; si reexportas en models/__init__.py
# puedes cambiar a: from ..models import UserVerificationCode)
from ..models.user_verification_code import UserVerificationCode

User = get_user_model()


# =====================================================
# Helpers para obtener las choices desde el propio modelo
# =====================================================
def _verification_type_choices() -> List[Tuple[str, str]]:
    """
    Obtiene las choices reales del campo `verification_type` del modelo,
    evitando depender de una constante inexistente (e.g. VERIFICATION_TYPES).
    """
    try:
        field = UserVerificationCode._meta.get_field("verification_type")
        choices = list(field.choices or [])
        if choices:
            return choices
    except Exception:
        pass

    # Fallback mínimo por si el modelo no define choices (no debería pasar)
    return [
        ("email_verification", "Email verification"),
        ("email_change", "Email change"),
    ]


# =====================================================
# Serializers
# =====================================================

class VerificationCodeSerializer(serializers.ModelSerializer):
    """Serializer para códigos de verificación del modelo UserVerificationCode"""

    class Meta:
        model = UserVerificationCode
        fields = ["code", "verification_type", "target_email"]

    def validate_code(self, value: str) -> str:
        """
        Valida el formato del código de verificación:
        - Debe ser numérico
        - Debe tener 6 dígitos
        """
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("El código debe ser de 6 dígitos")
        return value


class EmailChangeSerializer(serializers.Serializer):
    """Serializer para solicitar cambio de email"""

    new_email = serializers.EmailField(help_text="Nuevo email para la cuenta")

    def validate_new_email(self, value: str) -> str:
        """
        Valida que el nuevo email no esté en uso por otro usuario.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email ya está registrado")
        return value


class EmailChangeConfirmSerializer(serializers.Serializer):
    """Serializer para confirmar cambio de email con código de verificación"""

    code = serializers.CharField(
        max_length=6,
        help_text="Código de verificación de 6 dígitos",
    )

    def validate_code(self, value: str) -> str:
        """
        Valida el formato del código de confirmación.
        """
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("El código debe ser de 6 dígitos")
        return value


class VerificationCodeRequestSerializer(serializers.Serializer):
    """Serializer para solicitar un código de verificación"""

    verification_type = serializers.ChoiceField(
        choices=_verification_type_choices(),
        help_text="Tipo de verificación requerida",
    )
    target_email = serializers.EmailField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="Email objetivo (requerido para cambio de email)",
    )

    def validate(self, attrs: dict) -> dict:
        """
        Verifica que se proporcione el email objetivo cuando el tipo
        de verificación sea cambio de email.
        """
        verification_type = attrs.get("verification_type")
        target_email = attrs.get("target_email")

        if verification_type == "email_change":
            if not target_email:
                raise serializers.ValidationError(
                    {"target_email": "El email objetivo es requerido para cambio de email"}
                )
            # Validación explícita adicional (EmailField ya valida, pero por si acaso)
            try:
                validate_email(target_email)
            except DjangoValidationError:
                raise serializers.ValidationError({"target_email": "Email inválido"})

        return attrs


class VerificationCodeResendSerializer(serializers.Serializer):
    """Serializer para reenviar código de verificación"""

    verification_type = serializers.ChoiceField(
        choices=_verification_type_choices(),
        help_text="Tipo de verificación",
    )
    target_email = serializers.EmailField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="Email objetivo (para cambio de email)",
    )

    def validate(self, attrs: dict) -> dict:
        verification_type = attrs.get("verification_type")
        target_email = attrs.get("target_email")

        if verification_type == "email_change":
            if not target_email:
                raise serializers.ValidationError(
                    {"target_email": "El email objetivo es requerido para cambio de email"}
                )
            try:
                validate_email(target_email)
            except DjangoValidationError:
                raise serializers.ValidationError({"target_email": "Email inválido"})
        return attrs


class VerificationStatusSerializer(serializers.Serializer):
    """Serializer para mostrar el estado de verificación (solo lectura)"""

    is_verified = serializers.BooleanField(
        read_only=True, help_text="Indica si la verificación fue exitosa"
    )
    message = serializers.CharField(
        read_only=True, help_text="Mensaje descriptivo del resultado"
    )
    expires_at = serializers.DateTimeField(
        read_only=True, help_text="Fecha de expiración del código"
    )
    attempts_remaining = serializers.IntegerField(
        read_only=True, help_text="Intentos restantes para usar el código"
    )


class EmailVerificationSerializer(serializers.Serializer):
    """Serializer para verificación de email de registro"""

    email = serializers.EmailField(help_text="Email a verificar")

    def validate_email(self, value: str) -> str:
        """
        Valida que el email exista y no esté verificado.
        Ojo: tu modelo expone `email_verified_at` (timestamp), no `email_verified` (bool).
        """
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("No existe una cuenta con este email")

        # Consideramos verificado si el timestamp existe
        if getattr(user, "email_verified_at", None):
            raise serializers.ValidationError("Este email ya está verificado")

        return value
