from django.db import models
from django.utils import timezone

class Diagnosis(models.Model):
    code = models.CharField(max_length=255, unique=True, verbose_name="Código")
    name = models.CharField(max_length=255, verbose_name="Nombre")
    
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de eliminación")
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'diagnoses'
        verbose_name = 'Diagnóstico'
        verbose_name_plural = 'Diagnósticos'
        ordering = ['code']