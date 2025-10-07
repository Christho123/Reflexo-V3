from typing import Iterable, Optional
from django.utils import timezone
from ..models.contraceptive_method import ContraceptiveMethod


def list_active() -> Iterable[ContraceptiveMethod]:
    return ContraceptiveMethod.objects.filter(deleted_at__isnull=True).order_by("name")


def get_by_id(pk: int) -> Optional[ContraceptiveMethod]:
    try:
        return ContraceptiveMethod.objects.get(pk=pk, deleted_at__isnull=True)
    except ContraceptiveMethod.DoesNotExist:
        return None


def create(**kwargs) -> ContraceptiveMethod:
    return ContraceptiveMethod.objects.create(**kwargs)


def update(instance: ContraceptiveMethod, **kwargs) -> ContraceptiveMethod:
    for field_name, value in kwargs.items():
        setattr(instance, field_name, value)
    instance.save()
    return instance


def soft_delete(instance: ContraceptiveMethod) -> ContraceptiveMethod:
    instance.deleted_at = timezone.now()
    instance.save(update_fields=["deleted_at"]) 
    return instance



