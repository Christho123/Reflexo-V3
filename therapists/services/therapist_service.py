from ..models.therapist import Therapist
from django.db import models

class TherapistService:
    """
    Servicio para manejar la lógica de negocio de terapeutas
    """
    
    @staticmethod
    def get_active_therapists():
        """Obtiene todos los terapeutas activos"""
        return Therapist.objects.filter(deleted_at__isnull=True)
    
    @staticmethod
    def get_inactive_therapists():
        """Obtiene todos los terapeutas inactivos"""
        return Therapist.objects.filter(deleted_at__isnull=False)
    
    @staticmethod
    def search_therapists(query):
        """Busca terapeutas por diferentes criterios"""
        return Therapist.objects.filter(
            models.Q(name__icontains=query) |
            models.Q(last_name_paternal__icontains=query) |
            models.Q(last_name_maternal__icontains=query) |
            models.Q(document_number__icontains=query) |
            models.Q(email__icontains=query),
            deleted_at__isnull=True
        )
    
    @staticmethod
    def soft_delete_therapist(therapist_id):
        """Marca un terapeuta como inactivo (soft delete)"""
        try:
            therapist = Therapist.objects.get(pk=therapist_id, deleted_at__isnull=True)
            therapist.soft_delete()
            return True
        except Therapist.DoesNotExist:
            return False
    
    @staticmethod
    def restore_therapist(therapist_id):
        """Restaura un terapeuta marcándolo como activo"""
        try:
            therapist = Therapist.objects.get(pk=therapist_id, deleted_at__isnull=False)
            therapist.restore()
            return True
        except Therapist.DoesNotExist:
            return False
