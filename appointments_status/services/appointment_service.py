from django.db import transaction
from django.utils import timezone
from django.conf import settings
from datetime import datetime, timedelta, time as dt_time
try:
    from zoneinfo import ZoneInfo
except Exception:  # Python <3.9 fallback no esperado en este entorno
    ZoneInfo = None
from rest_framework import status
from rest_framework.response import Response
from ..models import Appointment, Ticket
from ..serializers import AppointmentSerializer
from decimal import Decimal


class AppointmentService:
    """
    Servicio para gestionar las operaciones de citas médicas.
    Basado en la estructura actualizada del modelo.
    """
    
    @transaction.atomic
    def create(self, data):
        """
        Crea una nueva cita médica con ticket automático.
        
        Args:
            data (dict): Datos de la cita a crear
            
        Returns:
            Response: Respuesta con la cita creada o error
        """
        try:
            # Validar datos requeridos
            required_fields = ['patient', 'appointment_date', 'hour']
            for field in required_fields:
                if field not in data:
                    return Response(
                        {'error': f'El campo {field} es requerido'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Usar el serializer para crear la cita (maneja correctamente las relaciones)
            serializer = AppointmentSerializer(data=data)
            if serializer.is_valid():
                appointment = serializer.save()
                
                # El ticket se crea automáticamente mediante el signal
                # Verificar que se creó correctamente
                try:
                    ticket = Ticket.objects.get(appointment=appointment)
                    return Response({
                        'message': 'Cita creada exitosamente con ticket automático',
                        'appointment': serializer.data,
                        'ticket_number': ticket.ticket_number
                    }, status=status.HTTP_201_CREATED)
                except Ticket.DoesNotExist:
                    return Response(
                        {'error': 'Error al crear el ticket automático'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            else:
                return Response(
                    {'error': 'Datos inválidos', 'details': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except Exception as e:
            return Response(
                {'error': f'Error al crear la cita: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def get_by_id(self, appointment_id):
        """
        Obtiene una cita por su ID.
        
        Args:
            appointment_id (int): ID de la cita
            
        Returns:
            Response: Respuesta con la cita o error si no existe
        """
        try:
            appointment = Appointment.objects.get(id=appointment_id, deleted_at__isnull=True)
            serializer = AppointmentSerializer(appointment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Appointment.DoesNotExist:
            return Response(
                {'error': 'Cita no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error al obtener la cita: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @transaction.atomic
    def update(self, appointment_id, data):
        """
        Actualiza una cita existente.
        
        Args:
            appointment_id (int): ID de la cita a actualizar
            data (dict): Nuevos datos de la cita
            
        Returns:
            Response: Respuesta con la cita actualizada o error
        """
        try:
            appointment = Appointment.objects.get(id=appointment_id, deleted_at__isnull=True)
            
            # Usar el serializer para actualizar (maneja correctamente las relaciones)
            serializer = AppointmentSerializer(appointment, data=data, partial=True)
            if serializer.is_valid():
                appointment = serializer.save()
                
                # El ticket se actualiza automáticamente mediante el signal
                return Response({
                    'message': 'Cita actualizada exitosamente',
                    'appointment': serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': 'Datos inválidos', 'details': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
        except Appointment.DoesNotExist:
            return Response(
                {'error': 'Cita no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error al actualizar la cita: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def delete(self, appointment_id):
        """
        Elimina una cita (soft delete).
        
        Args:
            appointment_id (int): ID de la cita a eliminar
            
        Returns:
            Response: Respuesta de confirmación o error
        """
        try:
            appointment = Appointment.objects.get(id=appointment_id, deleted_at__isnull=True)
            appointment.soft_delete()
            
            # También desactivar el ticket asociado
            try:
                ticket = Ticket.objects.get(appointment=appointment)
                ticket.soft_delete()
            except Ticket.DoesNotExist:
                pass  # Si no hay ticket, no hay problema
            
            return Response({
                'message': 'Cita eliminada exitosamente'
            }, status=status.HTTP_200_OK)
            
        except Appointment.DoesNotExist:
            return Response(
                {'error': 'Cita no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error al eliminar la cita: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def list_all(self, filters=None, pagination=None):
        """
        Lista todas las citas con filtros opcionales.
        
        Args:
            filters (dict): Filtros a aplicar
            pagination (dict): Configuración de paginación
            
        Returns:
            Response: Respuesta con la lista de citas
        """
        try:
            queryset = Appointment.objects.filter(deleted_at__isnull=True)
            
            # Aplicar filtros
            if filters:
                if 'appointment_date' in filters:
                    queryset = queryset.filter(appointment_date=filters['appointment_date'])
                if 'appointment_status' in filters:
                    queryset = queryset.filter(appointment_status=filters['appointment_status'])
                if 'patient' in filters:
                    queryset = queryset.filter(patient=filters['patient'])
                if 'therapist' in filters:
                    queryset = queryset.filter(therapist=filters['therapist'])
            
            # Aplicar paginación básica
            if pagination:
                page = pagination.get('page', 1)
                page_size = pagination.get('page_size', 10)
                start = (page - 1) * page_size
                end = start + page_size
                queryset = queryset[start:end]
            
            serializer = AppointmentSerializer(queryset, many=True)
            return Response({
                'count': queryset.count(),
                'results': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error al listar las citas: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def get_by_date_range(self, start_date, end_date, filters=None):
        """
        Obtiene citas dentro de un rango de fechas.
        
        Args:
            start_date (date): Fecha de inicio
            end_date (date): Fecha de fin
            filters (dict): Filtros adicionales
            
        Returns:
            Response: Respuesta con las citas en el rango
        """
        try:
            queryset = Appointment.objects.filter(
                appointment_date__range=[start_date, end_date],
                deleted_at__isnull=True
            )
            
            # Aplicar filtros adicionales
            if filters:
                if 'appointment_status' in filters:
                    queryset = queryset.filter(appointment_status=filters['appointment_status'])
                if 'patient' in filters:
                    queryset = queryset.filter(patient=filters['patient'])
                if 'therapist' in filters:
                    queryset = queryset.filter(therapist=filters['therapist'])
            
            serializer = AppointmentSerializer(queryset, many=True)
            return Response({
                'count': queryset.count(),
                'results': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error al obtener citas por rango: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def get_completed_appointments(self, filters=None, pagination=None):
        """
        Obtiene las citas completadas.
        
        Args:
            filters (dict): Filtros adicionales
            
        Returns:
            Response: Respuesta con las citas completadas
        """
        try:
            # Buscar citas con estado "Completada" (ID 2) o fecha anterior a hoy
            from ..models import AppointmentStatus
            
            # Intentar obtener el estado "Completado"
            try:
                completed_status = AppointmentStatus.objects.get(name="Completado")
                completed_status_id = completed_status.id
            except AppointmentStatus.DoesNotExist:
                completed_status_id = None
            
            queryset = Appointment.objects.filter(deleted_at__isnull=True)
            
            # Aplicar filtros
            if filters:
                if 'appointment_status' in filters:
                    # Si se especifica un status, usar ese
                    queryset = queryset.filter(appointment_status=filters['appointment_status'])
                else:
                    # Si no se especifica, buscar por estado "Completada" o fecha anterior
                    if completed_status_id:
                        queryset = queryset.filter(appointment_status=completed_status_id)
                    else:
                        # Fallback: usar fecha anterior a hoy
                        today = timezone.now().date()
                        queryset = queryset.filter(appointment_date__lt=today)
                
                if 'patient' in filters and filters['patient']:
                    queryset = queryset.filter(patient=filters['patient'])
                if 'therapist' in filters and filters['therapist']:
                    queryset = queryset.filter(therapist=filters['therapist'])

                # Filtro por fecha con ventana horaria (evita desfases de zona horaria)
                tzname = getattr(settings, 'TIME_ZONE', 'UTC')
                tz = ZoneInfo(tzname) if ZoneInfo else None

                date_str = filters.get('date')
                if date_str:
                    base_date = datetime.fromisoformat(date_str).date()
                    start_dt = datetime.combine(base_date, dt_time.min)
                    end_dt = start_dt + timedelta(days=1)
                    if tz:
                        start_dt = timezone.make_aware(start_dt, tz)
                        end_dt = timezone.make_aware(end_dt, tz)
                    else:
                        start_dt = timezone.make_aware(start_dt)
                        end_dt = timezone.make_aware(end_dt)
                    queryset = queryset.filter(appointment_date__gte=start_dt, appointment_date__lt=end_dt)
                else:
                    start_date = filters.get('start_date')
                    end_date = filters.get('end_date')
                    if start_date and end_date:
                        s_date = datetime.fromisoformat(start_date).date()
                        e_date = datetime.fromisoformat(end_date).date()
                        start_dt = datetime.combine(s_date, dt_time.min)
                        end_dt = datetime.combine(e_date + timedelta(days=1), dt_time.min)
                        if tz:
                            start_dt = timezone.make_aware(start_dt, tz)
                            end_dt = timezone.make_aware(end_dt, tz)
                        else:
                            start_dt = timezone.make_aware(start_dt)
                            end_dt = timezone.make_aware(end_dt)
                        queryset = queryset.filter(appointment_date__gte=start_dt, appointment_date__lt=end_dt)
                    elif start_date:
                        s_date = datetime.fromisoformat(start_date).date()
                        start_dt = datetime.combine(s_date, dt_time.min)
                        if tz:
                            start_dt = timezone.make_aware(start_dt, tz)
                        else:
                            start_dt = timezone.make_aware(start_dt)
                        queryset = queryset.filter(appointment_date__gte=start_dt)
                    elif end_date:
                        e_date = datetime.fromisoformat(end_date).date()
                        end_dt = datetime.combine(e_date + timedelta(days=1), dt_time.min)
                        if tz:
                            end_dt = timezone.make_aware(end_dt, tz)
                        else:
                            end_dt = timezone.make_aware(end_dt)
                        queryset = queryset.filter(appointment_date__lt=end_dt)
            else:
                # Sin filtros: buscar por estado "Completada" o fecha anterior
                if completed_status_id:
                    queryset = queryset.filter(appointment_status=completed_status_id)
                else:
                    # Fallback: usar fecha anterior a hoy
                    today = timezone.now().date()
                    queryset = queryset.filter(appointment_date__lt=today)
            
            total = queryset.count()

            # Aplicar paginación básica
            if pagination:
                page = pagination.get('page', 1)
                page_size = pagination.get('page_size', 10)
                start = (page - 1) * page_size
                end = start + page_size
                queryset = queryset.order_by('-appointment_date', '-hour')[start:end]

            serializer = AppointmentSerializer(queryset, many=True)
            return Response({'count': total, 'results': serializer.data}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error al obtener citas completadas: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def get_pending_appointments(self, filters=None):
        """
        Obtiene las citas pendientes.
        
        Args:
            filters (dict): Filtros adicionales
            
        Returns:
            Response: Respuesta con las citas pendientes
        """
        try:
            # Buscar citas con estado "Pendiente" (ID 5) o fecha >= hoy
            from ..models import AppointmentStatus
            
            # Intentar obtener el estado "Pendiente"
            try:
                pending_status = AppointmentStatus.objects.get(name="Pendiente")
                pending_status_id = pending_status.id
            except AppointmentStatus.DoesNotExist:
                pending_status_id = None
            
            queryset = Appointment.objects.filter(deleted_at__isnull=True)
            
            # Aplicar filtros
            if filters:
                if 'appointment_status' in filters:
                    # Si se especifica un status, usar ese
                    queryset = queryset.filter(appointment_status=filters['appointment_status'])
                else:
                    # Si no se especifica, buscar por estado "Pendiente" o fecha >= hoy
                    if pending_status_id:
                        queryset = queryset.filter(appointment_status=pending_status_id)
                    else:
                        # Fallback: usar fecha >= hoy
                        today = timezone.now().date()
                        queryset = queryset.filter(appointment_date__gte=today)
                
                if 'patient' in filters:
                    queryset = queryset.filter(patient=filters['patient'])
                if 'therapist' in filters:
                    queryset = queryset.filter(therapist=filters['therapist'])
            else:
                # Sin filtros: buscar por estado "Pendiente" o fecha >= hoy
                if pending_status_id:
                    queryset = queryset.filter(appointment_status=pending_status_id)
                else:
                    # Fallback: usar fecha >= hoy
                    today = timezone.now().date()
                    queryset = queryset.filter(appointment_date__gte=today)
            
            serializer = AppointmentSerializer(queryset, many=True)
            return Response({
                'count': queryset.count(),
                'results': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error al obtener citas pendientes: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def check_availability(self, date, hour, duration=60):
        """
        Verifica la disponibilidad para una cita.
        
        Args:
            date (date): Fecha de la cita
            hour (time): Hora de la cita
            duration (int): Duración en minutos
            
        Returns:
            Response: Respuesta con la disponibilidad
        """
        try:
            # Convertir la hora de inicio a datetime
            from datetime import datetime, timedelta
            start_datetime = datetime.combine(date, hour)
            end_datetime = start_datetime + timedelta(minutes=duration)
            
            # Buscar citas que se solapen
            conflicting_appointments = Appointment.objects.filter(
                appointment_date=date,
                deleted_at__isnull=True
            ).exclude(
                hour__gte=end_datetime.time()
            ).exclude(
                hour__lte=start_datetime.time()
            )
            
            is_available = not conflicting_appointments.exists()
            
            return Response({
                'is_available': is_available,
                'conflicting_appointments': conflicting_appointments.count() if not is_available else 0
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error al verificar disponibilidad: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
