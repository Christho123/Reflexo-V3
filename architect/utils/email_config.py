# Configuración de email para referencia
# NOTA: Esta configuración se ha movido directamente a settings.py
# para evitar problemas de importación circular
EMAIL_CONFIG = {
    'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
    'EMAIL_HOST': 'smtp.gmail.com',
    'EMAIL_PORT': 587,
    'EMAIL_USE_TLS': True,
    'EMAIL_HOST_USER': 'reflexoperu1@gmail.com',
    'EMAIL_HOST_PASSWORD': 'lund mcye hgxm gbcl',
    'DEFAULT_FROM_EMAIL': 'Django Entorno <reflexoperu1@gmail.com>'
}
