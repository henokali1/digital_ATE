from django.db import models
import os

class Manual(models.Model):
    title = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)  # Full path relative to MEDIA_ROOT
    section = models.CharField(max_length=255, blank=True, null=True) # Section: Communication, Navigation, etc.
    folder = models.CharField(max_length=255, blank=True, null=True) # subfolder name
    file_type = models.CharField(max_length=50, blank=True, null=True)  # .pdf, .doc, etc.
    indexed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def file_name(self):
        return os.path.basename(self.file_path)
