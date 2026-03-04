from django.db import models
from django.utils import timezone


class Appointment(models.Model):
    # Relaciones con otros módulos
    history = models.ForeignKey('histories_configurations.History', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Historial")
    patient = models.ForeignKey('patients_diagnoses.Patient', on_delete=models.CASCADE, verbose_name="Paciente")
    therapist = models.ForeignKey('therapists.Therapist', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Terapeuta")
    
    # Campos principales de la cita
    appointment_date = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de la cita")
    hour = models.TimeField(blank=True, null=True, verbose_name="Hora de la cita")
    
    # Información médica
    ailments = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Padecimientos")
    diagnosis = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Diagnóstico")
    surgeries = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Cirugías")
    reflexology_diagnostics = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Diagnósticos de reflexología")
    medications = models.CharField(max_length=255, blank=True, null=True, verbose_name="Medicamentos")
    observation = models.CharField(max_length=255, blank=True, null=True, verbose_name="Observaciones")
    
    # Fechas de tratamiento
    initial_date = models.DateField(blank=True, null=True, verbose_name="Fecha inicial")
    final_date = models.DateField(blank=True, null=True, verbose_name="Fecha final")
    
    # Configuración de la cita
    appointment_type = models.CharField(max_length=255, blank=True, null=True, verbose_name="Tipo de cita")
    room = models.IntegerField(blank=True, null=True, verbose_name="Habitación/Consultorio")
    
    # Información de pago
    social_benefit = models.BooleanField(default=True, verbose_name="Beneficio social")
    payment_detail = models.CharField(max_length=255, blank=True, null=True, verbose_name="Detalle de pago")
    payment = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name="Pago")
    ticket_number = models.CharField(max_length=20, blank=True, null=True, db_index=True)
    
    # Relaciones
    payment_type = models.ForeignKey('histories_configurations.PaymentType', on_delete=models.SET_NULL, null=True, verbose_name="Tipo de pago")
    payment_status = models.ForeignKey('histories_configurations.PaymentStatus', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Estado de pago")
    
    appointment_status = models.ForeignKey('AppointmentStatus', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Estado de Cita")
    
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    
    class Meta:
        db_table = 'appointments'
        verbose_name = "Cita"
        verbose_name_plural = "Citas"
        ordering = ['-appointment_date', '-hour']
        indexes = [
            models.Index(fields=['appointment_date', 'hour']),
            models.Index(fields=['appointment_status']),
        ]
    
    def __str__(self):
        return f"Cita {self.id} - {self.appointment_date} {self.hour}"
    
    @property
    def is_completed(self):
        """Verifica si la cita está completada basándose en el estado o fecha"""
        # Prioridad 1: Si tiene estado ID 2 (Completado), está completada
        if self.appointment_status_id == 2:
            return True
        
        # Prioridad 2: Si tiene estado "Completado", está completada
        if self.appointment_status and hasattr(self.appointment_status, 'name'):
            if self.appointment_status.name == "Completado":
                return True
        
        # Prioridad 3: Si no tiene estado, usar fecha
        if self.appointment_date is None:
            return False
        return self.appointment_date.date() < timezone.now().date()

    @property
    def is_pending(self):
        """Verifica si la cita está pendiente basándose en el estado o fecha"""
        # Prioridad 1: Si tiene estado ID 2 (Completado), NO está pendiente
        if self.appointment_status_id == 2:
            return False
        
        # Prioridad 2: Si tiene estado "Completado", NO está pendiente
        if self.appointment_status and hasattr(self.appointment_status, 'name'):
            if self.appointment_status.name == "Completado":
                return False
        
        # Prioridad 3: Si tiene estado ID 5 (Pendiente), SÍ está pendiente
        if self.appointment_status_id == 5:
            return True
        
        # Prioridad 4: Si tiene estado "Pendiente", SÍ está pendiente
        if self.appointment_status and hasattr(self.appointment_status, 'name'):
            if self.appointment_status.name == "Pendiente":
                return True
        
        # Prioridad 5: Si no tiene estado, usar fecha
        if self.appointment_date is None:
            return False
        return self.appointment_date.date() >= timezone.now().date()