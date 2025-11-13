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
    """
    
    queryset = AppointmentStatus.objects.all()
    serializer_class = AppointmentStatusSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['name']
    
    def get_queryset(self):
        """
        Filtra el queryset según los parámetros de la request.
        """
        try:
            queryset = AppointmentStatus.objects.all()
            
            return queryset
        except Exception as e:
            print(f"Error en get_queryset: {e}")
            raise
    
    def destroy(self, request, *args, **kwargs):
        """
        Elimina un estado de cita de forma permanente.
        """
        try:
            instance = self.get_object()
            
            # Verificar si hay citas que usan este estado antes de eliminar
            if instance.appointment_set.exists():
                return Response(
                    {'error': f"No se puede eliminar el estado '{instance.name}' porque tiene {instance.appointment_set.count()} cita(s) asociada(s). Primero asigne otro estado a esas citas."
                    }, status=status.HTTP_400_BAD_REQUEST)
                
            instance.delete() # Hard delete
            return Response({'message': f"Estado '{instance.name}' eliminado permanentemente"}, status=status.HTTP_204_NO_CONTENT)
            
        except AppointmentStatus.DoesNotExist:
            return Response({'error': 'Estado no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f"Error al eliminar el estado: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
