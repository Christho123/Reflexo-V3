from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.appointment import AppointmentViewSet
from .views.appointment_status import AppointmentStatusViewSet
from .views.ticket import TicketViewSet

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'appointment-statuses', AppointmentStatusViewSet, basename='appointment-status')
router.register(r'tickets', TicketViewSet, basename='ticket')

app_name = 'appointments_status'

urlpatterns = [
    path('', include(router.urls)),
]
