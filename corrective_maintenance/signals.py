# corrective_maintenance/signals.py
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.files import File
from .models import CorrectiveMaintenance
from logbook.models import LogEntry

@receiver(post_save, sender=CorrectiveMaintenance)
def create_logentry(sender, instance, created, **kwargs):
    """
    Signal to create a LogEntry when a CorrectiveMaintenance is created
    """
    if created:
        # Create new LogEntry
        log_entry = LogEntry.objects.create(
            date=instance.end_date,
            time=instance.end_time,
            location=instance.location,
            remarks=instance.remarks,
        )
        
        # Handle photo if it exists
        if instance.photo:
            log_entry.photos = instance.photo
            log_entry.save()
        
        # Store the log entry ID in instance for use in m2m_changed signal
        instance._log_entry_id = log_entry.id

@receiver(m2m_changed, sender=CorrectiveMaintenance.completed_by.through)
def update_log_initials(sender, instance, action, pk_set, **kwargs):
    """
    Signal to update LogEntry initials when CorrectiveMaintenance completed_by is changed
    """
    if action == "post_add" and hasattr(instance, '_log_entry_id'):
        # Get the associated log entry
        try:
            log_entry = LogEntry.objects.get(id=instance._log_entry_id)
            # Set the initials
            log_entry.initials.set(instance.completed_by.all())
        except LogEntry.DoesNotExist:
            pass
