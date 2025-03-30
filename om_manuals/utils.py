import os
import logging
from django.conf import settings
from om_manuals.models import Manual

logger = logging.getLogger(__name__)

def index_manuals():
    """
    Walks the manuals directory, creates or updates Manual records.
    """
    indexed_count = 0
    updated_count = 0

    manuals_path = os.path.join(settings.MEDIA_ROOT, 'manuals')

    for root, subdirs, files in os.walk(manuals_path):
        section = os.path.basename(root) if root != manuals_path else None  # Top-level folders are the sections.
        relative_path = os.path.relpath(root, manuals_path)
        folder_name = relative_path if relative_path != '.' else None #folder name

        for file in files:
            file_path = os.path.join(root, file)
            relative_file_path = os.path.relpath(file_path, settings.MEDIA_ROOT) #relative path to base_dir
            title = os.path.splitext(file)[0] # Title from file name
            file_type = os.path.splitext(file)[1]

            try:
                manual, created = Manual.objects.get_or_create(
                    file_path=relative_file_path,
                    defaults={
                        'title': title,
                        'section': section,
                        'folder': folder_name,
                        'file_type': file_type,
                    }
                )
                if not created:
                    #Update existing records
                    manual.title = title
                    manual.section = section
                    manual.folder = folder_name
                    manual.file_type = file_type
                    manual.save()
                    updated_count += 1
                else:
                    indexed_count += 1
                
            except Exception as e:
                logger.error(f"Error indexing {file_path}: {e}")

    logger.info(f"Indexed {indexed_count} new manuals. Updated {updated_count} existing manuals.")

def remove_deleted_manuals():
    """
    Removes Manual records that no longer exist in the manuals directory.
    """
    deleted_count = 0

    manuals_path = os.path.join(settings.MEDIA_ROOT, 'manuals')

    # Build a set of existing file paths
    existing_file_paths = set()
    for root, _, files in os.walk(manuals_path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_file_path = os.path.relpath(file_path, settings.MEDIA_ROOT)
            existing_file_paths.add(relative_file_path)

    # Find Manual records that are not in the existing file paths
    manuals_to_delete = Manual.objects.exclude(file_path__in=existing_file_paths)

    # Delete the Manual records
    deleted_count = manuals_to_delete.count()
    manuals_to_delete.delete()

    logger.info(f"Removed {deleted_count} deleted manuals from the index.")
