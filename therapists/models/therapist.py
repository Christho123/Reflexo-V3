from django.db import models
from django.conf import settings
from ubi_geo.models import Region, Province, District
from histories_configurations.models import DocumentType

class Therapist(models.Model):
    # Datos personales
    document_type = models.ForeignKey(
        DocumentType, 
        on_delete=models.CASCADE,
        verbose_name="Tipo de documento"
    )

    document_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Número de documento")
    license_number = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="Numero de licencia")
    last_name_paternal = models.CharField(max_length=150, verbose_name="Apellido paterno")
    last_name_maternal = models.CharField(max_length=150, verbose_name="Apellido materno")
    first_name = models.CharField(max_length=150, verbose_name="Nombre")
    birth_date = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de nacimiento")
    gender = models.CharField(max_length=50, blank=True, null=True, verbose_name="Sexo")
    personal_reference = models.CharField(max_length=255, blank=True, null=True, verbose_name="Referencia personal")
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    # Información de contacto
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    email = models.CharField(max_length=254, unique=True, blank=True, null=True, verbose_name="Email")

    # Ubicación
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name="Región")
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name="Provincia")
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name="Distrito")

    address = models.TextField(blank=True, null=True, verbose_name="Dirección")
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Foto de perfil"
    )
    
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de eliminación")

    def get_full_name(self):
        """Obtiene el nombre completo del terapeuta."""
        return f"{self.first_name} {self.last_name_paternal} {self.last_name_maternal or ''}"
    
    def __str__(self):
        return self.get_full_name()
    
    def get_profile_picture_url(self):
        """Retorna la URL de la foto de perfil o None si no tiene foto."""
        if self.profile_picture:
            return f"{settings.MEDIA_URL}{self.profile_picture}"
        return None

    def soft_delete(self):
        """Soft delete del terapeuta."""
        from django.utils import timezone
        self.deleted_at = timezone.now()
        self.is_active = False
        self.save(update_fields=['deleted_at', 'is_active'])

    def restore(self):
        """Restaura un terapeuta eliminado."""
        self.deleted_at = None
        self.is_active = True
        self.save(update_fields=['deleted_at', 'is_active'])

    class Meta:
        db_table = 'therapists'
        verbose_name = "Terapeuta"
        verbose_name_plural = "Terapeutas"
        ordering = ['first_name', 'last_name_paternal']