from rest_framework import serializers
from ..models.medical_record import MedicalRecord
from .patient import PatientSerializer
from .diagnosis import DiagnosisSerializer

class MedicalRecordSerializer(serializers.ModelSerializer):
    """Serializer para el modelo MedicalRecord."""
    
    # Campos relacionados anidados
    patient = PatientSerializer(read_only=True)
    diagnose = DiagnosisSerializer(read_only=True)
    
    # IDs para escritura
    patient_id = serializers.PrimaryKeyRelatedField(
        queryset=PatientSerializer.Meta.model.objects.all(), 
        source='patient', 
        write_only=True,
        required=False
    )
    diagnose_id = serializers.PrimaryKeyRelatedField(
        queryset=DiagnosisSerializer.Meta.model.objects.all(), 
        source='diagnose', 
        write_only=True,
        required=False
    )
    
    class Meta:
        model = MedicalRecord
        fields = [
            'id', 'patient', 'diagnose', 'diagnosis_date',
            'symptoms', 'treatment', 'notes', 'status',
            'patient_id', 'diagnose_id', 'created_at', 'updated_at', 'deleted_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']
        extra_kwargs = {
            'diagnosis_date': {'required': False},
            'symptoms': {'required': False},
            'treatment': {'required': False},
            'notes': {'required': False},
            'status': {'required': False}
        }
    
    def validate_diagnosis_date(self, value):
        """Validar que la fecha de diagnóstico no sea futura."""
        from datetime import date
        if value > date.today():
            raise serializers.ValidationError("La fecha de diagnóstico no puede ser futura.")
        return value
    
    def validate(self, data):
        """Validación personalizada."""
        # Solo validar duplicados si se están enviando los campos relevantes
        if 'patient' in data and 'diagnose' in data and 'diagnosis_date' in data:
            # Validar que no exista un registro duplicado para la misma fecha
            if MedicalRecord.objects.filter(
                patient=data['patient'],
                diagnose=data['diagnose'],
                diagnosis_date=data['diagnosis_date']
            ).exclude(id=self.instance.id if self.instance else None).exists():
                raise serializers.ValidationError(
                    "Ya existe un registro médico para este paciente con este diagnóstico en la misma fecha."
                )
        return data

class MedicalRecordListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listar historiales médicos."""
    
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    diagnose_name = serializers.CharField(source='diagnose.name', read_only=True)
    diagnose_code = serializers.CharField(source='diagnose.code', read_only=True)
    
    class Meta:
        model = MedicalRecord
        fields = [
            'id', 'patient_name', 'diagnose_name', 'diagnose_code',
            'diagnosis_date', 'symptoms', 'treatment', 'notes', 'status', 'created_at'
        ]
