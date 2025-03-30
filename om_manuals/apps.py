from django.apps import AppConfig

class OmManualsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'om_manuals'

    def ready(self):
        import om_manuals.signals
