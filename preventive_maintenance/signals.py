# preventive_maintenance/signals.py
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.files.base import ContentFile
from .models import PreventiveMaintenance
from logbook.models import LogEntry

@receiver(post_save, sender=PreventiveMaintenance)
def create_log_entry(sender, instance, created, **kwargs):
    """
    Signal handler to create a LogEntry when a new PreventiveMaintenance is created
    """
    if created:
        # Create the log entry
        log_entry = LogEntry.objects.create(
            date=instance.end_date,
            time=instance.end_time,
            location=instance.location,
            remarks=instance.remarks
        )
        
        # Copy photo if it exists
        if instance.photo:
            # Copy the photo file to the new LogEntry
            photo_name = instance.photo.name.split('/')[-1]  # Get the original filename
            log_entry.photos.save(
                photo_name,
                ContentFile(instance.photo.read()),
                save=True
            )
        
        # Store reference to log entry for m2m signal
        instance._log_entry = log_entry

@receiver(m2m_changed, sender=PreventiveMaintenance.completed_by.through)
def update_log_entry_initials(sender, instance, action, reverse, model, pk_set, **kwargs):
    """
    Signal handler to update the LogEntry initials when the completed_by field is updated
    """
    if hasattr(instance, '_log_entry') and action == "post_add":
        log_entry = instance._log_entry
        log_entry.initials.set(instance.completed_by.all())
