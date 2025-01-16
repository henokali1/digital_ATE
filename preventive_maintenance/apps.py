# preventive_maintenance/apps.py
from django.apps import AppConfig


class PreventiveMaintenanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'preventive_maintenance'

    def ready(self):
        try:
            import preventive_maintenance.signals  # noqa
        except ImportError:
            pass
