# corrective_maintenance/apps.py
from django.apps import AppConfig

class CorrectiveMaintenanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'corrective_maintenance'

    def ready(self):
        import corrective_maintenance.signals  # Import the signals module
