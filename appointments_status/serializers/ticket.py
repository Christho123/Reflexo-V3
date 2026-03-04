from rest_framework import serializers
from ..models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Ticket.
    Basado en la estructura actualizada del modelo.
    """
    
    # Campos calculados
    is_paid = serializers.ReadOnlyField()
    is_pending = serializers.ReadOnlyField()
    
    # Campos de relación
    appointment_details = serializers.CharField(
        source='appointment.__str__', 
        read_only=True
    )
    payment_type_name = serializers.CharField(
        source='payment_type.name',
        read_only=True,
        allow_null=True
    )
    
    class Meta:
        model = Ticket
        fields = [
            'id',
            'appointment',
            'appointment_details',
            'ticket_number',
            'payment_date',
            'amount',
            'payment_type',
            'payment_type_name',
            'description',
            'status',
            'is_paid',
            'is_pending',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'payment_date', 'created_at', 'updated_at']
        
    def validate_ticket_number(self, value):
        """Validación personalizada para el número de ticket"""
        # Verificar que el número de ticket no esté vacío
        if not value.strip():
            raise serializers.ValidationError(
                "El número de ticket no puede estar vacío."
            )
        
        # Verificar que no exista otro ticket con el mismo número
        instance = self.instance
        if Ticket.objects.filter(ticket_number=value).exclude(id=instance.id if instance else None).exists():
            raise serializers.ValidationError(
                "Ya existe un ticket con este número."
            )
        
        return value.strip()
    
    def validate_amount(self, value):
        """Validación personalizada para el monto"""
        if value < 0:
            raise serializers.ValidationError(
                "El monto no puedee ser negativo."
            )
        return value
    
    def validate_payment_type(self, value):
        """Validación personalizada para el tipo de pago"""
        if value is None:
            return value
        # El campo payment_type es una ForeignKey, Django ya valida que exista
        return value
    
    def validate(self, data):
        """Validación a nivel de objeto"""
        status = data.get('status')
        amount = data.get('amount')
        
        # Si el ticket está marcado como pagado, debe tener un monto válido (puede ser 0)
        if status == 'paid' and (amount is None or amount < 0):
            raise serializers.ValidationError(
                "Un ticket pagado debe tener un monto válido (no puede ser negativo)."
            )
        
        return data
