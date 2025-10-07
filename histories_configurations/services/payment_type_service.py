from ..models.payment_type import PaymentType

def list_active():
    return PaymentType.objects.filter(deleted_at__isnull=True)

def create(**kwargs):
    return PaymentType.objects.create(**kwargs)

def update(instance: PaymentType, **kwargs):
    for k,v in kwargs.items():
        setattr(instance, k, v)
    instance.save()
    return instance

def delete(instance: PaymentType):
    """Elimina completamente un DocumentType."""
    instance.delete()
    return instance
