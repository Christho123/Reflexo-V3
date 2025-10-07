from django.contrib import admin
from .models.patient import Patient
from .models.diagnosis import Diagnosis
from .models.medical_record import MedicalRecord

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'document_number', 'name', 'paternal_lastname', 'maternal_lastname', 'phone1', 'email')
    search_fields = ('id', 'document_number', 'name', 'paternal_lastname', 'maternal_lastname', 'personal_reference')
    list_filter = ('sex', 'region', 'province', 'district', 'document_type', 'created_at', 'deleted_at')
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')

@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'created_at')
    search_fields = ('code', 'name')
    ordering = ('code',)
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'diagnose', 'diagnosis_date', 'status', 'created_at')
    list_filter = ('status', 'diagnosis_date', 'created_at', 'deleted_at')
    search_fields = ('patient__name', 'patient__document_number', 'diagnose__name', 'diagnose__code')
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')
    ordering = ('-diagnosis_date', '-created_at')
    
    fieldsets = (
        ('Información del Paciente', {
            'fields': ('patient',)
        }),
        ('Información del Diagnóstico', {
            'fields': ('diagnose', 'diagnosis_date', 'status')
        }),
        ('Detalles Médicos', {
            'fields': ('symptoms', 'treatment', 'notes')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'deleted_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('patient', 'diagnose')