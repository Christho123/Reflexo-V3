import os
from celery import Celery

# Establecer la variable de entorno para Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')

# Crear la instancia de Celery
app = Celery('reflexo')

# Usar la configuración de Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Cargar tareas automáticamente desde todos los archivos tasks.py registrados
app.autodiscover_tasks()

# Configuración de Celery
app.conf.update(
    # Broker de mensajes (Redis)
    broker_url=os.environ.get('REDIS_URL', 'redis://localhost:6379/0'),
    
    # Backend de resultados
    result_backend=os.environ.get('REDIS_URL', 'redis://localhost:6379/0'),
    
    # Configuración de tareas
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    
    # Configuración de workers
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    worker_max_tasks_per_child=1000,
    
    # Configuración de beat (scheduler)
    beat_scheduler='django_celery_beat.schedulers:DatabaseScheduler',
    
    # Configuración de resultados
    result_expires=3600,  # 1 hora
    
    # Configuración de colas
    task_default_queue='default',
    task_routes={
        'appointments_status.tasks.*': {'queue': 'appointments'},
        'company_reports.tasks.*': {'queue': 'reports'},
        'therapists.tasks.*': {'queue': 'therapists'},
    },
    
    # Configuración de monitoreo
    worker_send_task_events=True,
    task_send_sent_event=True,
)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
