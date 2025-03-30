# watcher.py (at your project root)
import os
import time
import logging
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digital_ATE.settings')  # Use your actual settings module
django.setup()

from django.conf import settings
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from om_manuals.utils import index_manuals, remove_deleted_manuals

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class ManualsDirectoryEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        # Avoid indexing temporary files
        if event.is_directory or event.src_path.endswith(('~', '.tmp', '.swp', '.DS_Store')):
            return
        
        # Add debouncing 
        time.sleep(0.5)
        
        logger.info(f"Detected event: {event.event_type} {event.src_path}")
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

if __name__ == "__main__":
    logger.info("Starting manual watcher...")
    index_manuals()
    remove_deleted_manuals()
    start_watching()
