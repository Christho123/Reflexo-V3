from django.db import models

class PredeterminedPrice(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Nombre"
    )
    price = models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        verbose_name="Precio"
    )

    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de eliminación")

    def __str__(self):
        return f"{self.name} - {self.price}"

    class Meta:
        db_table = "predetermined_prices"
        verbose_name = "Precio Predeterminado"
        verbose_name_plural = "Precios Predeterminados"
        ordering = ['name']
