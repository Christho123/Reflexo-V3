from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from ..models import AppointmentStatus
from ..serializers import AppointmentStatusSerializer


class AppointmentStatusService:
    """
    Servicio para gestionar las operaciones de estados de citas.
    """
    
    def create(self, data):
        """
        Crea un nuevo estado de cita.
        
        Args:
            data (dict): Datos del estado a crear
            
        Returns:
            Response: Respuesta con el estado creado o error
        """
        # Implementación para crear un nuevo estado de cita
        serializer = AppointmentStatusSerializer(data=data)
        if serializer.is_valid():
            status_obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_by_id(self, status_id):
        """
        Obtiene un estado de cita por su ID.
        
        Args:
            status_id (int): ID del estado
            
        Returns:
            Response: Respuesta con el estado o error si no existe
        """
        try:
            status_obj = AppointmentStatus.objects.get(id=status_id)
            serializer = AppointmentStatusSerializer(status_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AppointmentStatus.DoesNotExist:
            return Response({'error': 'Estado de cita no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    def update(self, status_id, data):
        """
        Actualiza un estado de cita existente.
        
        Args:
            status_id (int): ID del estado a actualizar
            data (dict): Nuevos datos del estado
            
        Returns:
            Response: Respuesta con el estado actualizado o error
        """
        try:
            status_obj = AppointmentStatus.objects.get(id=status_id)
            serializer = AppointmentStatusSerializer(status_obj, data=data, partial=True)
            if serializer.is_valid():
                status_obj = serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AppointmentStatus.DoesNotExist:
            return Response({'error': 'Estado de cita no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, status_id):
        """
        Elimina un estado de cita de forma permanente.
        
        Args:
            status_id (int): ID del estado a eliminar
            
        Returns:
            Response: Respuesta de confirmación o error
        """
        try:
            status_obj = AppointmentStatus.objects.get(id=status_id)
            
            # Verificar si hay citas que usan este estado antes de eliminar
            if status_obj.appointment_set.exists():
                return Response(
                    {'error': 'No se puede eliminar el estado porque tiene citas asociadas.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            status_obj.delete() # Hard delete
            return Response({'message': 'Estado de cita eliminado permanentemente'}, status=status.HTTP_204_NO_CONTENT)
        except AppointmentStatus.DoesNotExist:
            return Response({'error': 'Estado de cita no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    def list_all(self, filters=None):
        """
        Lista todos los estados de citas.
        
        Args:
            filters (dict): Filtros a aplicar
            
        Returns:
            Response: Respuesta con la lista de estados
        """
        queryset = AppointmentStatus.objects.all()
        if filters:
            # Aquí podrías aplicar filtros adicionales si los hubiera
            pass
        serializer = AppointmentStatusSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_by_name(self, name):
        """
        Obtiene un estado de cita por su nombre.
        
        Args:
            name (str): Nombre del estado
            
        Returns:
            Response: Respuesta con el estado o error si no existe
        """
        try:
            status_obj = AppointmentStatus.objects.get(name=name)
            serializer = AppointmentStatusSerializer(status_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AppointmentStatus.DoesNotExist:
            return Response({'error': 'Estado de cita no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    def get_active_statuses(self):
        """
        Obtiene todos los estados activos.
        
        Returns:
            Response: Respuesta con los estados activos
        """
        queryset = AppointmentStatus.objects.all() # Asumiendo que todos los estados son "activos" ahora que no hay soft-delete
        serializer = AppointmentStatusSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
