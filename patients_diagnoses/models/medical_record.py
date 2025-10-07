from django.db import models
from django.utils import timezone

class MedicalRecord(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, verbose_name="Paciente")
    diagnose = models.ForeignKey('Diagnosis', on_delete=models.CASCADE, verbose_name="Diagnóstico")
    
    # Información del diagnóstico
    diagnosis_date = models.DateField(verbose_name="Fecha de diagnóstico")
    symptoms = models.TextField(blank=True, null=True, verbose_name="Síntomas")
    treatment = models.TextField(blank=True, null=True, verbose_name="Tratamiento")
    notes = models.TextField(blank=True, null=True, verbose_name="Notas")
    
    # Estado del diagnóstico
    status = models.CharField(max_length=20, default='active', verbose_name="Estado")
    
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de eliminación")
    
    class Meta:
        db_table = 'medical_records'
        verbose_name = 'Historial Médico'
        verbose_name_plural = 'Historiales Médicos'
        ordering = ['-diagnosis_date', '-created_at']
        unique_together = ['patient', 'diagnose', 'diagnosis_date']
    
    def soft_delete(self):
        """Soft delete del historial médico."""
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])
    
    def restore(self):
        """Restaura un historial médico eliminado."""
        self.deleted_at = None
        self.save(update_fields=['deleted_at'])
    
    def __str__(self):
        return f"{self.patient} - {self.diagnose} ({self.diagnosis_date})"
