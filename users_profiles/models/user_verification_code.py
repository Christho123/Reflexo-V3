# users_profiles/models/user_verification_code.py
from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class UserVerificationCode(models.Model):
    # user_id permite múltiples códigos por usuario → ForeignKey
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Usuario',
        db_column='user_id',
        related_name='verification_codes',
        null=True,
        blank=True,
    )

    code = models.CharField(max_length=255, blank=True, null=True, verbose_name='Código')
    verification_type = models.CharField(
        max_length=50, 
        default='email_verification',
        choices=[
            ('email_verification', 'Verificación de email'),
            ('email_change', 'Cambio de email'),
            ('password_change', 'Cambio de contraseña'),
        ],
        verbose_name='Tipo de verificación'
    )
    target_email = models.EmailField(blank=True, null=True, verbose_name='Email objetivo')
    is_used = models.BooleanField(default=False, verbose_name='¿Usado?')
    expires_at = models.DateTimeField(verbose_name='Expira en')
    failed_attempts = models.IntegerField(default=0, verbose_name='Intentos fallidos')
    locked_until = models.DateTimeField(blank=True, null=True, verbose_name='Bloqueado hasta')

    created_at = models.DateTimeField(verbose_name='Creado en')
    updated_at = models.DateTimeField(verbose_name='Actualizado en')

    class Meta:
        db_table = 'users_verification_code'
        managed = True  # Django gestiona la tabla
        verbose_name = 'Código de verificación de usuario'
        verbose_name_plural = 'Códigos de verificación de usuarios'
        ordering = ['-created_at']
        # Removido unique_together para permitir múltiples códigos por usuario/tipo

    def __str__(self):
        username = getattr(self.user, "user_name", getattr(self.user, "email", str(self.user_id)))
        return f'Código {self.code} para {username}'

    # Helpers opcionales
    def is_expired(self):
        return timezone.now() > self.expires_at

    def is_locked(self):
        return self.locked_until and timezone.now() < self.locked_until

    def increment_failed_attempts(self):
        self.failed_attempts = (self.failed_attempts or 0) + 1
        self.save(update_fields=['failed_attempts', 'updated_at'])

    def lock_temporarily(self, minutes=15):
        self.locked_until = timezone.now() + timedelta(minutes=minutes)
        self.save(update_fields=['locked_until', 'updated_at'])

    def unlock(self):
        self.locked_until = None
        self.failed_attempts = 0
        self.save(update_fields=['locked_until', 'failed_attempts', 'updated_at'])
    
    @classmethod
    def create_code(cls, user, verification_type='email_verification', target_email=None, metadata=None):
        """Crea un nuevo código de verificación para un usuario"""
        import random
        
        # DEBUG: Imprimir parámetros recibidos
        print(f"DEBUG create_code: user={user}, verification_type={verification_type}, target_email={target_email}")
        
        # Generar código de 6 dígitos
        code = str(random.randint(100000, 999999))
        
        # Calcular expiración (15 minutos)
        expires_at = timezone.now() + timedelta(minutes=15)
        
        # Marcar códigos anteriores del mismo tipo como usados
        cls.objects.filter(
            user=user,
            verification_type=verification_type,
            is_used=False
        ).update(is_used=True)
        
        # Crear nuevo código
        verification_code = cls.objects.create(
            user=user,
            verification_type=verification_type,
            code=code,
            target_email=target_email,
            expires_at=expires_at,
            failed_attempts=0,
            locked_until=None,
            is_used=False,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
        
        # DEBUG: Verificar lo que se guardó
        print(f"DEBUG create_code: Código creado {code}, target_email guardado: '{verification_code.target_email}'")
        
        return verification_code
    
    def mark_as_used(self):
        """Marca el código como usado"""
        self.is_used = True
        self.save(update_fields=['is_used', 'updated_at'])
    
    def can_attempt(self):
        """Verifica si se puede intentar usar el código"""
        return not self.is_expired() and not self.is_locked()
    
    def is_valid(self):
        """Verifica si el código es válido"""
        return self.code is not None and not self.is_expired() and not self.is_locked() and not self.is_used