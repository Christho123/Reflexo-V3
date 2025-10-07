from django.db import models
from .region import Region

class Province(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nombre")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name="Región")
    
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de eliminación")

    class Meta:
        db_table = 'provinces'
        verbose_name = "Provincia"
        verbose_name_plural = "Provincias"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.region.name})"
