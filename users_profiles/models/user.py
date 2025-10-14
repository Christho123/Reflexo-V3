# users_profiles/models/user.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import FileExtensionValidator
from histories_configurations.models import DocumentType 

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        
        if password is None:
            raise ValueError("El superusuario debe tener una contraseña")

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    # Desactivar campos de AbstractUser que NO existen en tu tabla
    username = None
    first_name = None
    last_name = None

    # Campos según la tabla SQL
    document_type = models.ForeignKey(DocumentType, on_delete=models.SET_NULL, null=True, blank=True)
    document_number = models.CharField(
        max_length=255, 
        null=True, 
        blank=True, 
        unique=True, 
        verbose_name="Número de documento"
    )
    photo_url = models.ImageField(  # Cambié CharField por ImageField
        upload_to='photo_pics/',  # Especifica el directorio donde se almacenarán las imágenes
        null=True, 
        blank=True, 
        verbose_name="Foto URL"
    )
    name = models.CharField(
        max_length=255, 
        null=True, 
        blank=True, 
        verbose_name="Nombres"
    )
    paternal_lastname = models.CharField(
        max_length=255, 
        null=True, 
        blank=True, 
        verbose_name="Apellido paterno"
    )
    maternal_lastname = models.CharField(
        max_length=255, 
        null=True, 
        blank=True, 
        verbose_name="Apellido materno"
    )
    email = models.EmailField(
        unique=True, 
        verbose_name="Correo electrónico"
    )
    sex = models.CharField(
        max_length=1, 
        null=True, 
        blank=True, 
        choices=[('M', 'Masculino'), ('F', 'Femenino')],
        verbose_name="Sexo"
    )
    phone = models.CharField(
        max_length=100, 
        null=True, 
        blank=True, 
        verbose_name="Teléfono"
    )
    user_name = models.CharField(
        max_length=150, 
        unique=True, 
        null=True, 
        blank=True, 
        verbose_name="Nombre de usuario"
    )
    password_change = models.BooleanField(
        default=False, 
        null=True, 
        blank=True, 
        verbose_name="Cambio de contraseña"
    )
    last_session = models.DateTimeField(
        null=True, 
        blank=True, 
        default=timezone.now, 
        verbose_name="Última sesión"
    )
    account_statement = models.CharField(
        max_length=1, 
        choices=[('A', 'Activo'), ('I', 'Inactivo')], 
        null=True, 
        blank=True, 
        default='A', 
        verbose_name="Estado de la cuenta"
    )
    email_verified_at = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name="Verificación del correo"
    )
    country = models.ForeignKey(
        'ubi_geo.Country', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="País"
    )
    remember_token = models.CharField(
        max_length=100, 
        null=True, 
        blank=True, 
        verbose_name="Token de recordatorio"
    )
    
    password = models.CharField(max_length=255, null=True, blank=True, verbose_name="Contraseña")
    
    # Campos de auditoría
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name="Fecha de actualización"
    )
    deleted_at = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name="Fecha de eliminación"
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'document_number']

    class Meta:
        db_table = 'users'
        managed = True  # Django gestiona la tabla
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.name} {self.paternal_lastname} - {self.document_number}"

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])

    def restore(self):
        self.deleted_at = None
        self.save(update_fields=['deleted_at'])

    def get_full_name(self):
        return f"{self.name} {self.paternal_lastname} {self.maternal_lastname or ''}"

    def verify_email(self):
        self.email_verified_at = timezone.now()
        self.save(update_fields=['email_verified_at'])