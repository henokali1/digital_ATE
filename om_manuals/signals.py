import os
import time
import logging
import threading
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_migrate
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from om_manuals.utils import index_manuals, remove_deleted_manuals

logger = logging.getLogger(__name__)

class ManualsDirectoryEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        # Avoid indexing temporary files created by editors
        if event.is_directory or event.src_path.endswith(('~', '.tmp')):
            return

        logger.info(f"Detected event: {event.event_type} {event.src_path}")
        index_manuals()
        remove_deleted_manuals()

def start_watching():
    event_handler = ManualsDirectoryEventHandler()
    manuals_path = os.path.join(settings.MEDIA_ROOT, 'manuals') # this is needed
    observer = Observer()
    observer.schedule(event_handler, manuals_path, recursive=True)
    observer.start()
    logger.info(f"Watching manuals directory: {manuals_path}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

@receiver(post_migrate)
def setup_manuals_watcher(sender, **kwargs):
    if sender.name == 'om_manuals':
        index_manuals()
        remove_deleted_manuals()
        thread = threading.Thread(target=start_watching, daemon=True)
        thread.start()
        logger.info("Started manuals directory watcher thread.")
