from django.db import models
from django.utils import timezone

class DIUType(models.Model):

    name = models.CharField(
        max_length=255,
        blank=True, 
        null=True,
        verbose_name="Nombre"
    )
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de eliminación")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "diu_types"
        verbose_name = "Tipo de dispositivo intrauterino"
        verbose_name_plural = "Tipos de dispositivos intrauterinos"
        ordering = ['name']
