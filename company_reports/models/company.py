from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator

class CompanyData(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nombre de la empresa")
    logo = models.ImageField(
        upload_to="company_logos/",
        blank=True,
        null=True,
        verbose_name="Logo de la empresa",
        validators=[ 
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "gif", "webp"])
        ]
    )
    
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    def get_logo_url(self):
        """
        Retorna la URL del logo de la empresa o None si no tiene logo
        """
        if self.logo:
            return f"{settings.MEDIA_URL}{self.logo}"
        return None

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'company_data'
        verbose_name = "Datos de la Empresa"
        verbose_name_plural = "Datos de las Empresas"
        ordering = ['name']
