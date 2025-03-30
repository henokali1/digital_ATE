# watcher.py
import os
import time
import logging
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from om_manuals.utils import index_manuals, remove_deleted_manuals

logger = logging.getLogger(__name__)

class ManualsDirectoryEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        # Avoid indexing temporary files created by editors
        if event.is_directory or event.src_path.endswith(('~', '.tmp')):
            return

        # Add a small delay to avoid file system events that might still be in progress
        time.sleep(0.5)
        
        logger.info(f"Detected event: {event.event_type} {event.src_path}")
        index_manuals()
        remove_deleted_manuals()

def start_watching():
    # Make sure the manuals directory exists
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

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Start the watcher
    logger.info("Starting manual watcher...")
    start_watching()
