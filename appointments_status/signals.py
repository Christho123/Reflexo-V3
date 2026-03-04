from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db import transaction
from .models import Appointment, Ticket
from .services.ticket_service import TicketService

@receiver(post_save, sender=Appointment)
def create_ticket_for_appointment(sender, instance, created, **kwargs):
    """
    Al crear una cita, genera ticket y asigna ticket_number a la cita.
    """
    if not created:
        return

    ticket_service = TicketService()
    ticket_number = ticket_service.generate_ticket_number()  # string

    with transaction.atomic():
        Ticket.objects.create(
            appointment=instance,
            ticket_number=ticket_number,
            amount=instance.payment or 0,
            payment_type=instance.payment_type,
            description=f'Ticket generado automáticamente para cita #{instance.id}',
            status='pending',
        )
        # IMPORTANTE: update() para no disparar otro post_save
        Appointment.objects.filter(pk=instance.pk).update(ticket_number=ticket_number)

@receiver(post_save, sender=Appointment)
def update_ticket_when_appointment_changes(sender, instance, created, **kwargs):
    """
    Si cambia el pago de la cita, sincroniza el ticket existente.
    """
    if created:
        return
    try:
        ticket = Ticket.objects.get(appointment=instance)
    except Ticket.DoesNotExist:
        # Si por alguna razón no existe, lo creamos sin volver a hacer save() en la cita
        ticket_service = TicketService()
        Ticket.objects.create(
            appointment=instance,
            ticket_number=instance.ticket_number or ticket_service.generate_ticket_number(),
            amount=instance.payment or 0,
            payment_type=instance.payment_type,
            description=f'Ticket autogenerado por sincronización para cita #{instance.id}',
            status='pending',
        )
        return

    if instance.payment is not None and ticket.amount != instance.payment:
        ticket.amount = instance.payment
        ticket.save(update_fields=['amount', 'updated_at'])