from rest_framework import serializers
from datetime import datetime
from django.utils.timezone import localtime


class DateParameterSerializer(serializers.Serializer):
    """Valida parámetros de fecha para reportes."""
    
    date = serializers.DateField(required=False, input_formats=['%Y-%m-%d'])
    start_date = serializers.DateField(required=False, input_formats=['%Y-%m-%d'])
    end_date = serializers.DateField(required=False, input_formats=['%Y-%m-%d'])
    
    def validate_date(self, value):
        """Valida formato de fecha."""
        if value:
            return value  # Retornar el objeto date, no string
        return localtime().date()
    
    def validate(self, data):
        """Validaciones cruzadas entre fechas."""
        if 'start_date' in data and 'end_date' in data:
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError("start_date no puede ser mayor que end_date")
        
        # Asegurar que date tenga un valor por defecto si no se proporciona
        if 'date' not in data:
            data['date'] = localtime().date()
            
        return data

class TherapistAppointmentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()  # 👈 SIN source, leerá 'name' del dict
    # Si en tu BD hay nulos en apellidos, permite null / opcional
    last_name_paternal = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    last_name_maternal = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    appointments_count = serializers.IntegerField()
    percentage = serializers.FloatField(required=False)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        total = self.context.get('total_appointments', 0) or 0
        appts = data.get('appointments_count', 0) or 0
        data['percentage'] = (appts / total * 100) if total > 0 else 0.0
        return data


class PatientByTherapistSerializer(serializers.Serializer):
    """Serializa datos de pacientes por terapeuta."""
    
    therapist_id = serializers.CharField()
    therapist = serializers.CharField()
    patients = serializers.ListField(child=serializers.DictField())


class DailyCashSerializer(serializers.Serializer):
    """Serializa datos de caja diaria por cita."""
    
    id_cita = serializers.IntegerField()
    payment = serializers.CharField()
    payment_type = serializers.IntegerField()
    payment_type_name = serializers.CharField()
    
    def to_representation(self, instance):
        """Formatea el pago."""
        data = super().to_representation(instance)
        if isinstance(data['payment'], (int, float)):
            data['payment'] = f"{float(data['payment']):.2f}"
        return data


class AppointmentRangeSerializer(serializers.Serializer):
    """Serializa citas entre fechas."""
    
    appointment_id = serializers.IntegerField()
    patient_id = serializers.IntegerField()
    document_number_patient = serializers.CharField()
    patient = serializers.CharField()
    phone1_patient = serializers.CharField()
    appointment_date = serializers.DateField(format='%Y-%m-%d')
    hour = serializers.TimeField(format='%H:%M')


class ReportResponseSerializer(serializers.Serializer):
    """Serializa respuestas de reportes con manejo de errores."""
    
    def to_representation(self, instance):
        """Maneja errores y datos exitosos."""
        if isinstance(instance, dict) and "error" in instance:
            return {"error": instance["error"]}
        return instance


class PDFContextSerializer(serializers.Serializer):
    """Serializa contexto para templates PDF."""
    
    date = serializers.CharField()
    data = serializers.DictField(required=False)
    title = serializers.CharField()
    total = serializers.FloatField(required=False)


# Nuevos serializers para los reportes mejorados

class PaymentDetailSerializer(serializers.Serializer):
    """Serializa detalles de pagos individuales."""
    
    tipo = serializers.CharField()
    id = serializers.IntegerField()
    ticket_number = serializers.CharField()
    monto = serializers.FloatField()
    metodo_pago = serializers.CharField()
    paciente = serializers.CharField()
    terapeuta = serializers.CharField()
    fecha_pago = serializers.CharField()


class PaymentMethodSummarySerializer(serializers.Serializer):
    """Serializa resumen por método de pago."""
    
    metodo = serializers.CharField()
    cantidad_pagos = serializers.IntegerField()
    total = serializers.FloatField()


class ImprovedDailyCashSerializer(serializers.Serializer):
    """Serializa el reporte mejorado de caja chica."""
    
    fecha = serializers.CharField()
    pagos_detallados = PaymentDetailSerializer(many=True)
    resumen_por_metodo = PaymentMethodSummarySerializer(many=True)
    total_general = serializers.FloatField()
    cantidad_total_pagos = serializers.IntegerField()


class TicketDetailSerializer(serializers.Serializer):
    """Serializa detalles de tickets pagados."""
    
    ticket_id = serializers.IntegerField()
    numero_ticket = serializers.CharField()
    monto = serializers.FloatField()
    metodo_pago = serializers.CharField()
    fecha_pago = serializers.CharField()
    descripcion = serializers.CharField()
    
    # Información de la cita
    cita_id = serializers.IntegerField()
    fecha_cita = serializers.CharField()
    hora_cita = serializers.CharField()
    consultorio = serializers.CharField()
    tipo_pago_cita = serializers.CharField()
    
    # Información del paciente
    paciente_nombre = serializers.CharField()
    paciente_documento = serializers.CharField()
    paciente_telefono = serializers.CharField()
    
    # Información del terapeuta
    terapeuta_nombre = serializers.CharField()
    terapeuta_documento = serializers.CharField()


class TicketMethodSummarySerializer(serializers.Serializer):
    """Serializa resumen por método de pago para tickets."""
    
    metodo = serializers.CharField()
    cantidad_tickets = serializers.IntegerField()
    total = serializers.FloatField()


class DailyPaidTicketsSerializer(serializers.Serializer):
    """Serializa el reporte diario de tickets pagados."""
    
    fecha = serializers.CharField()
    tickets_pagados = TicketDetailSerializer(many=True)
    resumen_por_metodo = TicketMethodSummarySerializer(many=True)
    total_general = serializers.FloatField()
    cantidad_tickets = serializers.IntegerField()
    metodos_pago_utilizados = serializers.ListField(child=serializers.CharField())