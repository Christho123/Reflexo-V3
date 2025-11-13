from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from ..models import Ticket
from ..serializers import TicketSerializer
from django.utils import timezone
import re


class TicketService:
    """
    Servicio para gestionar las operaciones de tickets.
    """
    
    @transaction.atomic
    def create(self, data):
        """
        Crea un nuevo ticket.
        
        Args:
            data (dict): Datos del ticket a crear
            
        Returns:
            Response: Respuesta con el ticket creado o error
        """
        try:
            # Validar datos requeridos
            required_fields = ['appointment', 'amount']
            for field in required_fields:
                if field not in data:
                    return Response(
                        {'error': f'El campo {field} es requerido'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Generar número de ticket único si no se proporciona
            if 'ticket_number' not in data:
                data['ticket_number'] = self.generate_ticket_number()
            
            # Usar el serializer para crear el ticket (maneja correctamente las relaciones)
            serializer = TicketSerializer(data=data)
            if serializer.is_valid():
                ticket = serializer.save()
                
                return Response({
                    'message': 'Ticket creado exitosamente',
                    'ticket': serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {'error': 'Datos inválidos', 'details': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
        except Exception as e:
            return Response(
                {'error': f'Error al crear el ticket: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def get_by_id(self, ticket_id):
        """
        Obtiene un ticket por su ID.
        
        Args:
            ticket_id (int): ID del ticket
            
        Returns:
            Response: Respuesta con el ticket o error si no existe
        """
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            serializer = TicketSerializer(ticket)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Ticket.DoesNotExist:
            return Response(
                {'error': 'Ticket no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error al obtener el ticket: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @transaction.atomic
    def update(self, ticket_id, data):
        """
        Actualiza un ticket existente.
        
        Args:
            ticket_id (int): ID del ticket a actualizar
            data (dict): Nuevos datos del ticket
            
        Returns:
            Response: Respuesta con el ticket actualizado o error
        """
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            
            # Usar el serializer para actualizar (maneja correctamente las relaciones)
            serializer = TicketSerializer(ticket, data=data, partial=True)
            if serializer.is_valid():
                ticket = serializer.save()
                
                return Response({
                    'message': 'Ticket actualizado exitosamente',
                    'ticket': serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': 'Datos inválidos', 'details': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
        except Ticket.DoesNotExist:
            return Response(
                {'error': 'Ticket no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error al actualizar el ticket: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def delete(self, ticket_id):
        """
        Elimina un ticket de forma permanente.
        
        Args:
            ticket_id (int): ID del ticket a eliminar
            
        Returns:
            Response: Respuesta de confirmación o error
        """
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            ticket.delete()
            
            return Response({
                'message': 'Ticket eliminado permanentemente'
            }, status=status.HTTP_200_OK)
            
        except Ticket.DoesNotExist:
            return Response(
                {'error': 'Ticket no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error al eliminar el ticket: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def list_all(self, filters=None, pagination=None):
        """
        Lista todos los tickets con filtros opcionales.
        
        Args:
            filters (dict): Filtros a aplicar
            pagination (dict): Configuración de paginación
            
        Returns:
            Response: Respuesta con la lista de tickets
        """
        try:
            queryset = Ticket.objects.all()
            
            # Aplicar filtros
            if filters:
                if 'status' in filters:
                    queryset = queryset.filter(status=filters['status'])
                if 'payment_type' in filters:
                    queryset = queryset.filter(payment_type=filters['payment_type'])
                if 'appointment' in filters:
                    queryset = queryset.filter(appointment=filters['appointment'])
                if 'payment_date' in filters:
                    queryset = queryset.filter(payment_date__date=filters['payment_date'])
            
            # Aplicar paginación básica
            if pagination:
                page = pagination.get('page', 1)
                page_size = pagination.get('page_size', 10)
                start = (page - 1) * page_size
                end = start + page_size
                queryset = queryset[start:end]
            
            serializer = TicketSerializer(queryset, many=True)
            return Response({
                'count': queryset.count(),
                'results': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error al listar los tickets: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def get_by_ticket_number(self, ticket_number):
        """
        Obtiene un ticket por su número.
        
        Args:
            ticket_number (str): Número del ticket
            
        Returns:
            Response: Respuesta con el ticket o error si no existe
        """
        try:
            ticket = Ticket.objects.get(ticket_number=ticket_number)
            serializer = TicketSerializer(ticket)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Ticket.DoesNotExist:
            return Response(
                {'error': 'Ticket no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error al obtener el ticket: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def get_paid_tickets(self, filters=None):
        """
        Obtiene los tickets pagados.
        
        Args:
            filters (dict): Filtros adicionales
            
        Returns:
            Response: Respuesta con los tickets pagados
        """
        try:
            queryset = Ticket.objects.filter(status='paid')
            
            # Aplicar filtros adicionales
            if filters:
                if 'payment_type' in filters:
                    queryset = queryset.filter(payment_type=filters['payment_type'])
                if 'appointment' in filters:
                    queryset = queryset.filter(appointment=filters['appointment'])
                if 'payment_date' in filters:
                    queryset = queryset.filter(payment_date__date=filters['payment_date'])
            
            serializer = TicketSerializer(queryset, many=True)
            return Response({
                'count': queryset.count(),
                'results': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error al obtener tickets pagados: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def get_pending_tickets(self, filters=None):
        """
        Obtiene los tickets pendientes.
        
        Args:
            filters (dict): Filtros adicionales
            
        Returns:
            Response: Respuesta con los tickets pendientes
        """
        try:
            queryset = Ticket.objects.filter(status='pending')
            
            # Aplicar filtros adicionales
            if filters:
                if 'payment_type' in filters:
                    queryset = queryset.filter(payment_type=filters['payment_type'])
                if 'appointment' in filters:
                    queryset = queryset.filter(appointment=filters['appointment'])
                if 'payment_date' in filters:
                    queryset = queryset.filter(payment_date__date=filters['payment_date'])
            
            serializer = TicketSerializer(queryset, many=True)
            return Response({
                'count': queryset.count(),
                'results': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error al obtener tickets pendientes: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @transaction.atomic
    def mark_as_paid(self, ticket_id):
        """
        Marca un ticket como pagado.
        
        Args:
            ticket_id (int): ID del ticket
            
        Returns:
            Response: Respuesta de confirmación o error
        """
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            ticket.mark_as_paid()
            serializer = TicketSerializer(ticket)
            
            return Response({
                'message': 'Ticket marcado como pagado exitosamente',
                'ticket': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Ticket.DoesNotExist:
            return Response(
                {'error': 'Ticket no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error al marcar ticket como pagado: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @transaction.atomic
    def mark_as_cancelled(self, ticket_id):
        """
        Marca un ticket como cancelado.
        
        Args:
            ticket_id (int): ID del ticket
            
        Returns:
            Response: Respuesta de confirmación o error
        """
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            ticket.mark_as_cancelled()
            serializer = TicketSerializer(ticket)
            
            return Response({
                'message': 'Ticket marcado como cancelado exitosamente',
                'ticket': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Ticket.DoesNotExist:
            return Response(
                {'error': 'Ticket no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error al marcar ticket como cancelado: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def generate_ticket_number(self):
        """
        Genera un número único de ticket en formato secuencial TKT-001, TKT-002, etc.
        
        Args:
            None
            
        Returns:
            str: Número de ticket único
        """
        # Obtener el último ticket creado
        last_ticket = Ticket.objects.order_by('-id').first()
        
        if last_ticket:
            # Extraer el número del último ticket
            try:
                # Buscar el patrón TKT-XXX en el número del ticket
                match = re.search(r'TKT-(\d+)', last_ticket.ticket_number)
                if match:
                    last_number = int(match.group(1))
                    next_number = last_number + 1
                else:
                    # Si no encuentra el patrón, empezar desde 1
                    next_number = 1
            except (ValueError, AttributeError):
                # Si hay algún error, empezar desde 1
                next_number = 1
        else:
            # Si no hay tickets, empezar desde 1
            next_number = 1
        
        # Formatear el número con ceros a la izquierda (ej: 001, 002, 010, 100)
        return f'TKT-{next_number:03d}'
