from django.urls import path, include
from rest_framework.routers import DefaultRouter
from company_reports.views.statistics_views import StatisticsViewSet, dashboard_view, GetMetricsView
from company_reports.views.company_views import CompanyDataViewSet
from company_reports.views import reports_views as views
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()
router.register(r'statistics', StatisticsViewSet, basename='statistics')
router.register(r'company', CompanyDataViewSet, basename='company')

# Agrupar rutas por funcionalidad
api_urlpatterns = [
    path('', include(router.urls)),
]

reports_urlpatterns = [
    path('reports/statistics/', GetMetricsView.as_view(), name='statistics_metrics'),
    path('reports/appointments-per-therapist/', views.ReportsAPIView.as_view(), name='appointments_per_therapist'),
    path('reports/patients-by-therapist/', views.PatientsByTherapistAPIView.as_view(), name='patients_by_therapist'),
    path('reports/daily-cash/', views.DailyCashAPIView.as_view(), name='daily_cash'),
    path('reports/improved-daily-cash/', views.ImprovedDailyCashAPIView.as_view(), name='improved_daily_cash'),
    path('reports/daily-paid-tickets/', views.DailyPaidTicketsAPIView.as_view(), name='daily_paid_tickets'),
    path('reports/appointments-between-dates/', views.AppointmentsBetweenDatesAPIView.as_view(), name='appointments_between_dates'),
]

export_urlpatterns = [
    path('exports/pdf/citas-terapeuta/', views.PDFCitasTerapeutaAPIView.as_view(), name='pdf_citas_terapeuta'),
    path('exports/pdf/pacientes-terapeuta/', views.PDFPacientesTerapeutaAPIView.as_view(), name='pdf_pacientes_terapeuta'),
    path('exports/pdf/resumen-caja/', views.PDFResumenCajaAPIView.as_view(), name='pdf_resumen_caja'),
    path('exports/pdf/caja-chica-mejorada/', views.PDFCajaChicaMejoradaAPIView.as_view(), name='pdf_caja_chica_mejorada'),
    path('exports/pdf/tickets-pagados/', views.PDFTicketsPagadosAPIView.as_view(), name='pdf_tickets_pagados'),
    path('exports/excel/citas-rango/', views.ExcelCitasAPIView.as_view(), name='exportar_excel_citas'),
    path('exports/excel/caja-chica-mejorada/', views.ExcelCajaChicaMejoradaAPIView.as_view(), name='exportar_excel_caja_chica_mejorada'),
    path('exports/excel/tickets-pagados/', views.ExcelTicketsPagadosAPIView.as_view(), name='exportar_excel_tickets_pagados'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''
views_urlpatterns = [
    path('form/', company_form_view, name='company_form'),
]
'''
urlpatterns = []
urlpatterns.extend(api_urlpatterns)
urlpatterns.extend(reports_urlpatterns)
urlpatterns.extend(export_urlpatterns)
#urlpatterns.extend(views_urlpatterns)