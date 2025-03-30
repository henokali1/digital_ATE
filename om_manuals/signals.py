# signals.py
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
        if event.is_directory or event.src_path.endswith(('~', '.tmp', '.swp', '.DS_Store')):
            return
            
        # Add debouncing to prevent multiple events from triggering multiple reindexes
        time.sleep(0.5)

        logger.info(f"Detected event: {event.event_type} {event.src_path}")
        
        # Only reindex if the event is in the manuals directory
        manuals_path = os.path.join(settings.MEDIA_ROOT, 'manuals')
        if os.path.abspath(event.src_path).startswith(os.path.abspath(manuals_path)):
            index_manuals()
            remove_deleted_manuals()

def start_watching():
    # Make sure manuals directory exists
    manuals_path = os.path.join(settings.MEDIA_ROOT, 'manuals')
    if not os.path.exists(manuals_path):
        os.makedirs(manuals_path)
        logger.info(f"Created manuals directory: {manuals_path}")
    
    event_handler = ManualsDirectoryEventHandler()
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

# Manual function to start the watcher
def start_watcher_thread():
    index_manuals()
    remove_deleted_manuals()
    thread = threading.Thread(target=start_watching, daemon=True)
    thread.start()
    logger.info("Started manuals directory watcher thread.")
    return thread

@receiver(post_migrate)
def setup_manuals_watcher(sender, **kwargs):
    if sender.name == 'om_manuals':
        start_watcher_thread()