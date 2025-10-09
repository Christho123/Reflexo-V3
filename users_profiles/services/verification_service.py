"""
Servicio para gestión de verificaciones de email y códigos de verificación
"""

from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from ..models.user_verification_code import UserVerificationCode

User = get_user_model()

class VerificationService:
    """Servicio para verificación de email de usuario"""
    
    @staticmethod
    def send_verification_email(user, verification_type='email_verification'):
        """
        Envía email de verificación al usuario
        
        Args:
            user: Usuario al que enviar el email
            verification_type: Tipo de verificación
            
        Returns:
            bool: True si se envió exitosamente
            
        Raises:
            ValidationError: Si hay error al enviar el email
        """
        try:
            with transaction.atomic():
                # Crear código de verificación
                verification_code = UserVerificationCode.create_code(
                    user=user,
                    verification_type=verification_type
                )
                
                # Preparar contenido del email
                subject, message, html_message = VerificationService._prepare_email_content(
                    user, verification_code, verification_type
                )
                
                # Enviar email
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    html_message=html_message,
                    fail_silently=False
                )
                
                return True
                
        except Exception as e:
            raise ValidationError(f"Error al enviar email de verificación: {str(e)}")
    
    @staticmethod
    def verify_email_code(code, verification_type='email_verification'):
        """
        Verifica código de email y actualiza estado del usuario
        
        Args:
            code: Código de verificación
            verification_type: Tipo de verificación
            
        Returns:
            tuple: (bool, str) - (éxito, mensaje)
        """
        try:
            with transaction.atomic():
                # Verificar código
                verification, error = UserVerificationCode.verify_code(
                    code=code,
                    verification_type=verification_type
                )
                
                if not verification:
                    return False, error
                
                user = verification.user
                
                # Marcar email como verificado según el tipo
                if verification_type == 'email_verification':
                    # No hay campo is_email_verified, solo marcar como usado
                    pass
                elif verification_type == 'email_change':
                    # Cambiar email si es cambio de email
                    new_email = verification.target_email
                    if new_email:
                        user.email = new_email
                        user.save()
                
                # Marcar código como usado
                verification.mark_as_used()
                
                return True, "Email verificado exitosamente"
                
        except Exception as e:
            return False, f"Error al verificar email: {str(e)}"
    
    @staticmethod
    def resend_verification_email(user, verification_type='email_verification'):
        """
        Reenvía email de verificación invalidando códigos anteriores
        
        Args:
            user: Usuario al que reenviar el email
            verification_type: Tipo de verificación
            
        Returns:
            bool: True si se reenvió exitosamente
        """
        try:
            # Invalidar códigos anteriores del mismo tipo
            UserVerificationCode.objects.filter(
                user=user,
                verification_type=verification_type,
                is_used=False
            ).update(is_used=True)
            
            # Enviar nuevo email
            return VerificationService.send_verification_email(user, verification_type)
            
        except Exception as e:
            raise ValidationError(f"Error al reenviar email de verificación: {str(e)}")
    
    @staticmethod
    def request_email_change(user, new_email):
        """
        Solicita cambio de email enviando código de verificación
        
        Args:
            user: Usuario que solicita el cambio
            new_email: Nuevo email
            
        Returns:
            bool: True si se envió la solicitud exitosamente
            
        Raises:
            ValidationError: Si el email ya está en uso o hay otros errores
        """
        try:
            # Verificar que el nuevo email no esté en uso
            if User.objects.filter(email=new_email).exists():
                raise ValidationError("El email ya está en uso")
            
            # Crear código de verificación con target_email (fuera de la transacción)
            verification_code = UserVerificationCode.create_code(
                user=user,
                verification_type='email_change',
                target_email=new_email
            )
            
            # Verificar que el código se creó correctamente
            if not verification_code.target_email:
                raise ValidationError("Error al crear el código de verificación")
            
            # Intentar enviar el email (sin transacción para que no revierta el código)
            try:
                # Preparar contenido del email
                subject, message, html_message = VerificationService._prepare_email_content(
                    user, verification_code, 'email_change', new_email
                )
                
                # Enviar email al nuevo email
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[new_email],
                    html_message=html_message,
                    fail_silently=False
                )
                
                print(f"✅ Email enviado exitosamente a {new_email}")
                
            except Exception as email_error:
                print(f"⚠️ Error al enviar email: {str(email_error)}")
                # No lanzar excepción aquí, el código ya se creó
                
            return True
                
        except Exception as e:
            raise ValidationError(f"Error al solicitar cambio de email: {str(e)}")
    
    @staticmethod
    def _prepare_email_content(user, verification_code, verification_type, new_email=None):
        """
        Prepara contenido del email según tipo de verificación
        
        Args:
            user: Usuario
            verification_code: Código de verificación
            verification_type: Tipo de verificación
            new_email: Nuevo email (para cambio de email)
            
        Returns:
            tuple: (subject, message, html_message)
        """
        base_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
        full_name = f"{user.name} {user.paternal_lastname}".strip() if user.name else user.user_name
        
        if verification_type == 'email_verification':
            subject = "Código de verificación - Reflexo"
            message = f"""
            Hola {full_name},
            
            Gracias por registrarte en Reflexo. Para verificar tu email, utiliza el siguiente código:
            
            CÓDIGO DE VERIFICACIÓN: {verification_code.code}
            
            Este código expirará en 15 minutos.
            
            Si no solicitaste esta verificación, puedes ignorar este email.
            
            Saludos,
            Equipo Reflexo
            """
            
            html_message = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #333;">Código de verificación - Reflexo</h2>
                <p>Hola {full_name},</p>
                <p>Gracias por registrarte en Reflexo. Para verificar tu email, utiliza el siguiente código:</p>
                
                <div style="background-color: #f5f5f5; padding: 20px; text-align: center; margin: 20px 0; border-radius: 5px;">
                    <h1 style="color: #007bff; font-size: 32px; margin: 0; letter-spacing: 5px;">{verification_code.code}</h1>
                </div>
                
                <p>Este código expirará en 15 minutos.</p>
                <p>Si no solicitaste esta verificación, puedes ignorar este email.</p>
                
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                <p style="color: #666; font-size: 12px;">Saludos,<br>Equipo Reflexo</p>
            </div>
            """
            
        elif verification_type == 'email_change':
            subject = "Código de confirmación de cambio de email - Reflexo"
            message = f"""
            Hola {full_name},
            
            Has solicitado cambiar tu email a: {new_email}
            
            Para confirmar este cambio, utiliza el siguiente código:
            
            CÓDIGO DE CONFIRMACIÓN: {verification_code.code}
            
            Este código expirará en 15 minutos.
            
            Si no solicitaste este cambio, puedes ignorar este email.
            
            Saludos,
            Equipo Reflexo
            """
            
            html_message = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #333;">Código de confirmación de cambio de email - Reflexo</h2>
                <p>Hola {full_name},</p>
                <p>Has solicitado cambiar tu email a: <strong>{new_email}</strong></p>
                <p>Para confirmar este cambio, utiliza el siguiente código:</p>
                
                <div style="background-color: #f5f5f5; padding: 20px; text-align: center; margin: 20px 0; border-radius: 5px;">
                    <h1 style="color: #ffc107; font-size: 32px; margin: 0; letter-spacing: 5px;">{verification_code.code}</h1>
                </div>
                
                <p>Este código expirará en 15 minutos.</p>
                <p>Si no solicitaste este cambio, puedes ignorar este email.</p>
                
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                <p style="color: #666; font-size: 12px;">Saludos,<br>Equipo Reflexo</p>
            </div>
            """
            
        elif verification_type == 'password_change':
            subject = "Código de recuperación de contraseña - Reflexo"
            message = f"""
            Hola {full_name},
            
            Has solicitado recuperar tu contraseña en Reflexo. Para crear una nueva contraseña, utiliza el siguiente código:
            
            CÓDIGO DE RECUPERACIÓN: {verification_code.code}
            
            Este código expirará en 15 minutos.
            
            Si no solicitaste este cambio, puedes ignorar este email.
            
            Saludos,
            Equipo Reflexo
            """
            
            html_message = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #333;">Código de recuperación de contraseña - Reflexo</h2>
                <p>Hola {full_name},</p>
                <p>Has solicitado recuperar tu contraseña en Reflexo. Para crear una nueva contraseña, utiliza el siguiente código:</p>
                
                <div style="background-color: #f5f5f5; padding: 20px; text-align: center; margin: 20px 0; border-radius: 5px;">
                    <h1 style="color: #dc3545; font-size: 32px; margin: 0; letter-spacing: 5px;">{verification_code.code}</h1>
                </div>
                
                <p>Este código expirará en 15 minutos.</p>
                <p>Si no solicitaste este cambio, puedes ignorar este email.</p>
                
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                <p style="color: #666; font-size: 12px;">Saludos,<br>Equipo Reflexo</p>
            </div>
            """
        
        else:
            raise ValidationError(f"Tipo de verificación no válido: {verification_type}")
        
        return subject, message, html_message
    
    @staticmethod
    def get_verification_status(user):
        """
        Obtiene estado de verificación del usuario
        
        Args:
            user: Usuario a verificar
            
        Returns:
            dict: Estado de verificación
        """
        return {
            'email': user.email,
            'has_pending_verifications': UserVerificationCode.objects.filter(
                user=user,
                is_used=False
            ).exists()
        }
    
    @staticmethod
    def cleanup_expired_codes():
        """
        Limpia códigos de verificación expirados
        
        Returns:
            int: Número de códigos eliminados
        """
        from django.utils import timezone
        
        expired_codes = UserVerificationCode.objects.filter(
            expires_at__lt=timezone.now()
        )
        count = expired_codes.count()
        expired_codes.delete()
        
        return count