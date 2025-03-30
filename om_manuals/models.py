# models.py
import os
from django.db import models
from django.conf import settings

class Manual(models.Model):
    title = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    section = models.CharField(max_length=255, blank=True, null=True)
    folder = models.CharField(max_length=255, blank=True, null=True)
    file_type = models.CharField(max_length=50, blank=True, null=True)
    indexed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def file_name(self):
        return os.path.basename(self.file_path)

    def file_size(self):
        """Returns the size of the file in bytes, or None if the file doesn't exist."""
        try:
            file_path = os.path.join(settings.MEDIA_ROOT, self.file_path)
            return os.path.getsize(file_path)
        except FileNotFoundError:
            return None

    def readable_file_size(self):
        """Returns a human-readable file size (e.g., '1.2 MB')."""
        size = self.file_size()
        if size is None:
            return "File not found"
        power = 2**10
        n = 0
        power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
        while size > power:
            size /= power
            n += 1
        return f"{size:.2f} {power_labels[n]}B"