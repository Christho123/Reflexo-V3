from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.diagnosis import (diagnosis_list, diagnosis_create, diagnosis_delete, diagnosis_edit,
                             DiagnosisListView, DiagnosisCreateView, DiagnosisDeleteView, DiagnosisEditView)
from .views.patient import ( PatientListCreateView, PatientRetrieveUpdateDeleteView, PatientSearchView )
from .views.medical_record import ( MedicalRecordListCreateAPIView, MedicalRecordRetrieveUpdateDestroyAPIView, PatientMedicalHistoryAPIView, DiagnosisStatisticsAPIView )

urlpatterns = [
     # URLs de diagnósticos (CON autenticación)
     path('diagnoses/', DiagnosisListView.as_view(), name='diagnosis_list_auth'), 
     path('diagnoses/create/', DiagnosisCreateView.as_view(), name='diagnosis_create_auth'), 
     path('diagnoses/<int:pk>/edit/', DiagnosisEditView.as_view(), name='diagnosis_edit_auth'),
     path('diagnoses/<int:pk>/delete/', DiagnosisDeleteView.as_view(), name='diagnosis_delete_auth'),
     
     # URLs de diagnósticos (SIN autenticación - para compatibilidad)
     path('diagnoses-legacy/', diagnosis_list, name='diagnosis_list_legacy'), 
     path('diagnoses-legacy/create/', diagnosis_create, name='diagnosis_create_legacy'), 
     path('diagnoses-legacy/<int:pk>/edit/', diagnosis_edit, name='diagnosis_edit_legacy'),
     path('diagnoses-legacy/<int:pk>/delete/', diagnosis_delete, name='diagnosis_delete_legacy'),
     
     # URLs de pacientes (CON autenticación)
     path('patients/', PatientListCreateView.as_view(), name='patient-list'),
     path('patients/search/', PatientSearchView.as_view(), name='patient-search'),
     path('patients/<int:pk>/', PatientRetrieveUpdateDeleteView.as_view(), name='patient-detail'),
     
     # URLs de historiales médicos
     path('medical-records/', MedicalRecordListCreateAPIView.as_view(), name='medical-record-list-create'),
     path('medical-records/<int:pk>/', MedicalRecordRetrieveUpdateDestroyAPIView.as_view(), name='medical-record-detail'),
     path('patients/<int:patient_id>/medical-history/', PatientMedicalHistoryAPIView.as_view(), name='patient-medical-history'),
]


