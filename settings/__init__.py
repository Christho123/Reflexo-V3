# Importar Celery para que se configure automáticamente
from .celery import app as celery_app

__all__ = ('celery_app',)
