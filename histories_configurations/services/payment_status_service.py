from ..models.payment_status import PaymentStatus

def list_active():
    return PaymentStatus.objects.filter(deleted_at__isnull=True)

def create(**kwargs):
    return PaymentStatus.objects.create(**kwargs)

def update(instance: PaymentStatus, **kwargs):
    for k,v in kwargs.items():
        setattr(instance, k, v)
    instance.save()
    return instance

def delete(instance: PaymentStatus):
    """Elimina completamente un DocumentType."""
    instance.delete()
    return instance
