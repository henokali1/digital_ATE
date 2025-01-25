from django.apps import AppConfig


class JobCardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'job_card'

    def ready(self):
        import job_card.signals