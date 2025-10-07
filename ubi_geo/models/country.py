from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nombre del país")
    phone_code = models.CharField(max_length=255, blank=True, null=True, verbose_name="Código telefónico")
    ISO2 = models.CharField(max_length=255, blank=True, null=True, unique=True, verbose_name="Código ISO2")
    
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de eliminación")
    
    class Meta:
        db_table = 'countries'
        verbose_name = "País"
        verbose_name_plural = "Países"
        ordering = ['name']
    
    def __str__(self):
        return self.name
