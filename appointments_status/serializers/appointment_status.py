from rest_framework import serializers
from ..models import AppointmentStatus


class AppointmentStatusSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo AppointmentStatus.
    Basado en la estructura actualizada del modelo.
    """
    
    # Campo calculado - temporalmente deshabilitado para debug
    # appointments_count = serializers.ReadOnlyField()
    
    class Meta:
        model = AppointmentStatus
        fields = [
            'id',
            'name',
            'description',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_name(self, value):
        """Validación personalizada para el nombre del estado"""
        # Verificar que el nombre no esté vacío
        if not value.strip():
            raise serializers.ValidationError(
                "El nombre del estado no puede estar vacío."
            )
        
        # Verificar que no exista otro estado activo con el mismo nombre (excluyendo soft deleted)
        instance = self.instance
        if AppointmentStatus.objects.filter(
            name=value 
        ).exclude(id=instance.id if instance else None).exists():
            raise serializers.ValidationError(
                "Ya existe un estado de cita activo con este nombre."
            )
        
        return value.strip()
    
    def validate(self, data):
        """Validación a nivel de objeto"""
        name = data.get('name', '')
        description = data.get('description', '')
        
        # Si no hay descripción, usar el nombre como descripción
        if not description and name:
            data['description'] = name
        
        return data
