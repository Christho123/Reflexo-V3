from django.db import models
from django.utils import timezone

# Manager para obtener solo registros activos (sin eliminar)
class ActiveHistoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class History(models.Model):
    # Relación con paciente
    patient = models.ForeignKey('patients_diagnoses.Patient', on_delete=models.CASCADE, verbose_name="Paciente")
    
    # Fecha del historial (permite múltiples historias por paciente con diferentes fechas)
    history_date = models.DateField(verbose_name="Fecha del historial")
    
    # Información médica
    testimony = models.BooleanField(default=True, verbose_name="Testimonio")
    private_observation = models.TextField(blank=True, null=True, verbose_name="Observación privada")
    observation = models.TextField(blank=True, null=True, verbose_name="Observación")
    height = models.DecimalField(max_digits=7, decimal_places=3, blank=True, null=True, verbose_name="Altura")
    initial_weight = models.CharField(max_length=255, blank=True, null=True, verbose_name="Peso Inicial")
    last_weight = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, verbose_name="Último peso")
    actual_weight = models.CharField(max_length=255, blank=True, null=True, verbose_name="Peso actual")
    
    # Información específica
    menstruation = models.BooleanField(default=True, verbose_name="Menstruación")
    diu_type = models.ForeignKey(
        'histories_configurations.DIUType',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Tipo de dispositivo intrauterino",
    )
    gestation = models.BooleanField(default=True, verbose_name="Gestación")

    # Método anticonceptivo (opcional)
    contraceptive_method = models.ForeignKey(
        'histories_configurations.ContraceptiveMethod',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Método anticonceptivo",
    )

    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de eliminación")

    # Managers
    objects = models.Manager()  # Manager por defecto
    active = ActiveHistoryManager()  # Manager para obtener solo los registros activos

    def __str__(self):
        return f"Historial de {self.patient}"

    class Meta:
        db_table = "histories"
        verbose_name = "Historial"
        verbose_name_plural = "Historiales"
        ordering = ['-history_date', '-created_at']
        unique_together = ['patient', 'history_date']  # Un historial por paciente por fecha
