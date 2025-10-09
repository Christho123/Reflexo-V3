from typing import Iterable, Optional
from django.utils import timezone
from ..models.diu_type import DIUType


def list_active() -> Iterable[DIUType]:
    return DIUType.objects.filter(deleted_at__isnull=True).order_by("name")


def get_by_id(pk: int) -> Optional[DIUType]:
    try:
        return DIUType.objects.get(pk=pk, deleted_at__isnull=True)
    except DIUType.DoesNotExist:
        return None


def create(**kwargs) -> DIUType:
    return DIUType.objects.create(**kwargs)


def update(instance: DIUType, **kwargs) -> DIUType:
    for field_name, value in kwargs.items():
        setattr(instance, field_name, value)
    instance.save()
    return instance


def soft_delete(instance: DIUType) -> DIUType:
    instance.deleted_at = timezone.now()
    instance.save(update_fields=["deleted_at"]) 
    return instance




