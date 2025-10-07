from ..models.document_type import DocumentType

def list_active():
    """Obtiene los DocumentTypes que no están marcados como eliminados."""
    return DocumentType.objects.filter(deleted_at__isnull=True)

def create(**kwargs):
    """Crea un nuevo DocumentType con los datos proporcionados."""
    return DocumentType.objects.create(**kwargs)

def update(instance: DocumentType, **kwargs):
    """Actualiza los atributos de un DocumentType existente."""
    for k, v in kwargs.items():
        setattr(instance, k, v)
    instance.save()
    return instance

def delete(instance: DocumentType):
    """Elimina completamente un DocumentType."""
    instance.delete()
    return instance
