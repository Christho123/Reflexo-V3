from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nombre")
    country = models.ForeignKey('Country', on_delete=models.CASCADE, verbose_name="País")
    
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de eliminación")

    class Meta:
        db_table = 'regions'
        verbose_name = "Región"
        verbose_name_plural = "Regiones"
        ordering = ["name"]

    def __str__(self):
        return self.name
