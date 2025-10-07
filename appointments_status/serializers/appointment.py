from rest_framework import serializers
from ..models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Appointment.
    Basado en la estructura actualizada del modelo.
    """
    
    # Campos calculados
    is_completed = serializers.ReadOnlyField()
    is_pending = serializers.ReadOnlyField()
    
    # Campos de relación
    patient_name = serializers.CharField(
        source='patient.get_full_name', 
        read_only=True
    )
    therapist_name = serializers.CharField(
        source='therapist.get_full_name', 
        read_only=True,
        allow_null=True
    )
    payment_type_name = serializers.CharField(
        source='payment_type.name', 
        read_only=True,
        allow_null=True
    )
    payment_status_name = serializers.CharField(
        source='payment_status.name', 
        read_only=True,
        allow_null=True
    )
    
    class Meta:
        model = Appointment
        fields = [
            'id',
            'history',
            'patient',
            'patient_name',
            'therapist',
            'therapist_name',
            'appointment_date',
            'hour',
            'ailments',
            'diagnosis',
            'surgeries',
            'reflexology_diagnostics',
            'medications',
            'observation',
            'initial_date',
            'final_date',
            'appointment_type',
            'room',
            'social_benefit',
            'payment_detail',
            'payment',
            'payment_type',
            'payment_type_name',
            'payment_status',
            'payment_status_name',
            'ticket_number',
            'appointment_status',
            'is_completed',
            'is_pending',
            'created_at',
            'updated_at',
            'deleted_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']
        
    def validate_appointment_date(self, value):
        """Validación personalizada para la fecha de la cita"""
        from django.utils import timezone
        today = timezone.now().date()
        
        if value and value.date() < today:
            raise serializers.ValidationError(
                "La fecha de la cita no puede ser anterior a hoy."
            )
        return value
    
    def validate(self, data):
        """Validación a nivel de objeto"""
        appointment_date = data.get('appointment_date')
        hour = data.get('hour')
        
        if appointment_date and hour:
            # Aquí se podría agregar validación para evitar solapamientos
            # cuando estén disponibles los modelos Patient y Therapist
            pass
        
        return data
