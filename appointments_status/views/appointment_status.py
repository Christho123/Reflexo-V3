from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from ..models import AppointmentStatus
from ..serializers import AppointmentStatusSerializer


class AppointmentStatusViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar los estados de citas.
    Basado en la estructura del módulo Laravel 05_appointments_status.
    """
    
    queryset = AppointmentStatus.objects.all()
    serializer_class = AppointmentStatusSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']  # Removido 'is_active' temporalmente
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['name']
    
    def get_queryset(self):
        """
        Filtra el queryset según los parámetros de la request.
        """
        try:
            # Excluir registros eliminados (soft delete)
            queryset = AppointmentStatus.objects.filter(deleted_at__isnull=True)
            
            # Filtro por estado activo (comentado temporalmente si no existe el campo)
            # is_active = self.request.query_params.get('is_active', None)
            # if is_active is not None:
            #     queryset = queryset.filter(is_active=is_active.lower() == 'true')
            
            return queryset
        except Exception as e:
            print(f"Error en get_queryset: {e}")
            raise
    
    # @action(detail=False, methods=['get'])
    # def active(self, request):
    #     """
    #     Obtiene solo los estados activos.
    #     """
    #     queryset = self.get_queryset().filter(is_active=True)
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)
    
    # @action(detail=True, methods=['post'])
    # def activate(self, request, pk=None):
    #     """
    #     Activa un estado de cita.
    #     """
    #     status_obj = self.get_object()
    #     status_obj.is_active = True
    #     status_obj.save()
    #     serializer = self.get_serializer(status_obj)
    #     return Response(serializer.data)
    
    # @action(detail=True, methods=['post'])
    # def deactivate(self, request, pk=None):
    #     """
    #     Desactiva un estado de cita.
    #     """
    #     status_obj = self.get_object()
    #     status_obj.is_active = False
    #     status_obj.save()
    #     serializer = self.get_serializer(status_obj)
    #     return Response(serializer.data)
    
    # @action(detail=True, methods=['get'])
    # def appointments(self, request, pk=None):
    #     """
    #     Obtiene las citas asociadas a un estado específico.
    #     """
    #     status_obj = self.get_object()
    #     appointments = status_obj.appointment_set.all()
    #     
    #     # TODO: (Dependencia externa) - Usar el serializer de Appointment cuando esté disponible
    #     from ..serializers import AppointmentSerializer
    #     serializer = AppointmentSerializer(appointments, many=True)
    #     return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """
        Elimina un estado de cita (soft delete).
        """
        try:
            instance = self.get_object()
            
            # Verificar si hay citas que usan este estado
            try:
                appointments_count = instance.appointment_set.count()
                if appointments_count > 0:
                    return Response({
                        "error": f"No se puede eliminar el estado '{instance.name}' porque tiene {appointments_count} cita(s) asociada(s). Primero asigne otro estado a esas citas."
                    }, status=status.HTTP_400_BAD_REQUEST)
            except Exception as db_error:
                # Si hay error de base de datos (columna inexistente), continuar con la eliminación
                error_msg = str(db_error)
                if "Unknown column" in error_msg and "appointment_status_id" in error_msg:
                    print(f"Advertencia: No se pudo verificar dependencias debido a estructura de BD: {error_msg}")
                    # Continuar con la eliminación sin verificar dependencias
                else:
                    # Re-lanzar si es otro tipo de error
                    raise
            
            # Soft delete - marcar como eliminado
            from django.utils import timezone
            instance.deleted_at = timezone.now()
            instance.save(update_fields=['deleted_at'])
            
            return Response({
                "message": f"Estado '{instance.name}' eliminado correctamente"
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "error": f"Error al eliminar el estado: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        """
        Restaura un estado de cita eliminado (soft delete).
        """
        try:
            # Buscar el estado incluso si está eliminado
            instance = AppointmentStatus.objects.get(pk=pk)
            
            if instance.deleted_at is None:
                return Response({
                    "error": "El estado no está eliminado"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Restaurar - limpiar deleted_at
            instance.deleted_at = None
            instance.save(update_fields=['deleted_at'])
            
            serializer = self.get_serializer(instance)
            return Response({
                "message": f"Estado '{instance.name}' restaurado correctamente",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
            
        except AppointmentStatus.DoesNotExist:
            return Response({
                "error": "Estado no encontrado"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "error": f"Error al restaurar el estado: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def all_including_deleted(self, request):
        """
        Obtiene todos los estados incluyendo los eliminados (soft delete).
        Útil para administración y debugging.
        """
        try:
            # Incluir todos los registros, incluso los eliminados
            queryset = AppointmentStatus.objects.all()
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                "message": "Estados obtenidos (incluyendo eliminados)",
                "data": serializer.data
            })
        except Exception as e:
            return Response({
                "error": f"Error al obtener estados: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
