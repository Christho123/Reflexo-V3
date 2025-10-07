from django.apps import AppConfig


class AppointmentsStatusConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appointments_status'
    verbose_name = 'Gestión de Citas y Estados'
    
    def ready(self):
        """
        Importar signals cuando la app esté lista.
        """
        import appointments_status.signals
