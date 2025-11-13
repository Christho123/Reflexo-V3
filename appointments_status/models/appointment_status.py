from django.db import models


class AppointmentStatus(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Nombre del estado"
    )
    description = models.TextField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Descripción"
    )
    
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    
    class Meta:
        db_table = 'appointment_statuses'
        verbose_name = "Estado de Cita"
        verbose_name_plural = "Estados de Citas"
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return self.name
    
    @property
    def appointments_count(self):
        """Retorna el número de citas con este estado"""
        return self.appointment_set.count()
