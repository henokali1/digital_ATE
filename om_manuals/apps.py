from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class OmManualsConfig(AppConfig):
    name = 'om_manuals'
    verbose_name = 'Manuals'

    def ready(self):
        import om_manuals.signals  # Import signals
        
        # Don't start the watcher when running management commands
        import sys
        if 'runserver' in sys.argv:
            try:
                # Start the watcher thread here to ensure it runs when the server starts
                from om_manuals.signals import start_watcher_thread
                start_watcher_thread()
                logger.info("Manual watcher started during application startup.")
            except Exception as e:
                logger.error(f"Error starting manual watcher: {e}")