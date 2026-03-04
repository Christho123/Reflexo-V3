from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from ..models import Ticket
from ..serializers import TicketSerializer
from ..services import TicketService


class TicketViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar los tickets.
    """
    
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        'ticket_number', 
        'payment_type', 
        'status', 
    ]
    search_fields = [
        'ticket_number', 
        'description'
    ]
    ordering_fields = [
        'payment_date', 
        'amount', 
        'created_at', 
        'updated_at'
    ]
    ordering = ['-payment_date']
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = TicketService()
    
    def get_queryset(self):
        """
        Filtra el queryset según los parámetros de la request.
        """
        queryset = Ticket.objects.all()
        
        # Filtros adicionales
        payment_date = self.request.query_params.get('payment_date', None)
        if payment_date:
            queryset = queryset.filter(payment_date__date=payment_date)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        """
        Crea un nuevo ticket.
        """
        return self.service.create(request.data)
    
    def update(self, request, *args, **kwargs):
        """
        Actualiza un ticket existente.
        """
        ticket_id = kwargs.get('pk')
        return self.service.update(ticket_id, request.data)
    
    def destroy(self, request, *args, **kwargs):
        """
        Elimina un ticket de forma permanente.
        """
        ticket_id = kwargs.get('pk')
        return self.service.delete(ticket_id)
    
    def list(self, request, *args, **kwargs):
        """
        Lista todos los tickets con filtros y paginación.
        """
        filters = {}
        pagination = {}
        
        # Extraer filtros de query params
        for field in ['status', 'payment_type', 'appointment']:
            value = request.query_params.get(field)
            if value:
                filters[field] = value
        
        # Extraer parámetros de paginación
        page = request.query_params.get('page')
        page_size = request.query_params.get('page_size')
        if page or page_size:
            pagination['page'] = int(page) if page else 1
            pagination['page_size'] = int(page_size) if page_size else 10
        
        return self.service.list_all(filters, pagination)
    
    @action(detail=False, methods=['get'])
    def paid(self, request):
        """
        Obtiene los tickets pagados.
        """
        filters = {}
        for field in ['payment_type', 'appointment']:
            value = request.query_params.get(field)
            if value:
                filters[field] = value
        
        return self.service.get_paid_tickets(filters)
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """
        Obtiene los tickets pendientes.
        """
        filters = {}
        for field in ['payment_type', 'appointment']:
            value = request.query_params.get(field)
            if value:
                filters[field] = value
        
        return self.service.get_pending_tickets(filters)
    
    @action(detail=False, methods=['get'])
    def cancelled(self, request):
        """
        Obtiene los tickets cancelados.
        """
        queryset = self.get_queryset().filter(status='cancelled')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_as_paid(self, request, pk=None):
        """
        Marca un ticket como pagado.
        """
        ticket_id = pk
        return self.service.mark_as_paid(ticket_id)
    
    @action(detail=True, methods=['post'])
    def mark_as_cancelled(self, request, pk=None):
        """
        Marca un ticket como cancelado.
        """
        ticket_id = pk
        return self.service.mark_as_cancelled(ticket_id)
    
    @action(detail=False, methods=['get'])
    def by_payment_method(self, request):
        """
        Obtiene tickets agrupados por método de pago.
        """
        payment_type = request.query_params.get('payment_type')
        if not payment_type:
            return Response(
                {'error': 'Se requiere payment_type'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        filters = {'payment_type': payment_type}
        return self.service.list_all(filters)
    
    @action(detail=False, methods=['get'])
    def by_ticket_number(self, request):
        """
        Obtiene un ticket por su número.
        """
        ticket_number = request.query_params.get('ticket_number')
        if not ticket_number:
            return Response(
                {'error': 'Se requiere ticket_number'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return self.service.get_by_ticket_number(ticket_number)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Obtiene estadísticas de tickets.
        """
        total_tickets = Ticket.objects.count()
        paid_tickets = Ticket.objects.filter(status='paid').count()
        pending_tickets = Ticket.objects.filter(status='pending').count()
        cancelled_tickets = Ticket.objects.filter(status='cancelled').count()
        
        # Calcular montos totales
        from django.db.models import Sum
        total_amount = Ticket.objects.filter(status='paid').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        stats = {
            'total_tickets': total_tickets,
            'paid_tickets': paid_tickets,
            'pending_tickets': pending_tickets,
            'cancelled_tickets': cancelled_tickets,
            'paid_percentage': (paid_tickets / total_tickets * 100) if total_tickets > 0 else 0,
            'total_amount_paid': float(total_amount),
        }
        
        return Response(stats)
