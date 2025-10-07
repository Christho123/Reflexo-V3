from .diagnosis import DiagnosisSerializer
from .patient import PatientSerializer, PatientListSerializer
from .medical_record import MedicalRecordSerializer, MedicalRecordListSerializer

__all__ = [
    'PatientSerializer', 'PatientListSerializer',
    'DiagnosisSerializer', 'DiagnosisListSerializer',
    'MedicalRecordSerializer', 'MedicalRecordListSerializer'
]