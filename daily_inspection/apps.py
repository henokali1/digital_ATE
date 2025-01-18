
# daily_inspection/apps.py
from django.apps import AppConfig

class DailyInspectionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'daily_inspection'
    
    def ready(self):
        import daily_inspection.signals
