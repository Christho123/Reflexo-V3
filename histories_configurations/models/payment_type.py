from django.db import models

class PaymentType(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre"
    )
    description = models.CharField(
        max_length=255,
        blank=True, 
        null=True,
        verbose_name="Descripción"
    )

    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de eliminación")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "payment_types"
        verbose_name = "Tipo de Pago"
        verbose_name_plural = "Tipos de Pago"
        ordering = ['name']
