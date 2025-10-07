from django.db import models

class PaymentStatus(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'payment_status'
        verbose_name = "Estado de pago"
        verbose_name_plural = "Estados de pago"
        ordering = ['name']

    def __str__(self):
        return self.name