# ubi_geo/apps.py
from django.apps import AppConfig

class UbiGeoConfig(AppConfig):   # <-- SIN guion bajo
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ubi_geo'
