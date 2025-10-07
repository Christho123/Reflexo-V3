from ..models.diagnosis import Diagnosis

def list_active():
    """Obtiene los Diagnosis que no están marcados como eliminados."""
    return Diagnosis.objects.filter(deleted_at__isnull=True)

def create(**kwargs):
    """Crea un nuevo Diagnosis con los datos proporcionados."""
    return Diagnosis.objects.create(**kwargs)

def update(instance: Diagnosis, **kwargs):
    """Actualiza los atributos de un Diagnosis existente."""
    for k, v in kwargs.items():
        setattr(instance, k, v)
    instance.save()
    return instance

def delete(instance: Diagnosis):
    """Elimina completamente un Diagnosis."""
    instance.delete()
    return instance
