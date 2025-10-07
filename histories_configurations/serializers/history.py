from rest_framework import serializers
from ..models import History
from django.contrib.auth import get_user_model

class HistorySerializer(serializers.ModelSerializer):
    # Campo relacionado anidado
    patient = serializers.SerializerMethodField(read_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
        source='patient',
        write_only=True
    )
    
    def get_patient(self, obj):
        """Obtiene los datos del paciente de forma segura"""
        if obj.patient:
            return {
                'id': obj.patient.id,
                'name': obj.patient.name,
                'paternal_lastname': obj.patient.paternal_lastname,
                'maternal_lastname': obj.patient.maternal_lastname,
                'document_number': obj.patient.document_number,
            }
        return None
    
    class Meta:
        model = History
        fields = [
            'id', 'patient', 'patient_id', 'testimony', 'private_observation', 
            'observation', 'height', 'weight', 'last_weight', 'menstruation', 
            'diu_type', 'gestation', 'created_at', 'updated_at', 'deleted_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']
