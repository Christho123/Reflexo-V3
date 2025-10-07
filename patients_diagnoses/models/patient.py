from django.db import models
from django.utils import timezone

class Patient(models.Model):
    # Información personal
    document_type = models.ForeignKey('histories_configurations.DocumentType', on_delete=models.CASCADE, verbose_name="Tipo de documento")
    document_number = models.CharField(max_length=20, unique=True, verbose_name="Número de documento")
    
    paternal_lastname = models.CharField(
    max_length=150, null=True, blank=True,
    db_column="last_name_paternal", verbose_name="Apellido paterno"
    )
    maternal_lastname = models.CharField(
    max_length=150, null=True, blank=True,
    db_column="last_name_maternal", verbose_name="Apellido materno"
    )
    name = models.CharField(max_length=150, verbose_name="Nombre")
    personal_reference = models.CharField(max_length=255, blank=True, null=True, verbose_name="Referencia personal")
    birth_date = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de nacimiento")
    sex = models.CharField(max_length=50, blank=True, null=True,db_column="gender", verbose_name="Sexo")

    # Información de contacto
    phone1 = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono 1")
    phone2 = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono 2")
    email = models.CharField(max_length=254, unique=True, verbose_name="Email")

    # Información adicional
    ocupation = models.CharField(max_length=100, verbose_name="Ocupación")
    health_condition = models.TextField(verbose_name="Condición de salud")
    address = models.TextField(blank=True, null=True, verbose_name="Dirección")

    # Relaciones con otras apps
    region = models.ForeignKey('ubi_geo.Region', on_delete=models.CASCADE, verbose_name="Región")
    province = models.ForeignKey('ubi_geo.Province', on_delete=models.CASCADE, verbose_name="Provincia")
    district = models.ForeignKey('ubi_geo.District', on_delete=models.CASCADE, verbose_name="Distrito")

    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de eliminación")

    class Meta:
        db_table = 'patients'
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['-created_at']

    def soft_delete(self):
        """Soft delete del paciente."""
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])

    def restore(self):
        """Restaura un paciente eliminado."""
        self.deleted_at = None
        self.save(update_fields=['deleted_at'])

    def get_full_name(self):
        """Obtiene el nombre completo del paciente."""
        return f"{self.name} {self.paternal_lastname} {self.maternal_lastname}"

    def __str__(self):
        return self.get_full_name()
