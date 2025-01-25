# job_card/signals.py
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import JobCard
from logbook.models import LogEntry
from django.utils import timezone

@receiver(post_save, sender=JobCard)
def reset_acknowledgement_on_create(sender, instance, created, **kwargs):
    """
    Signal handler to set acknowledged to False on creation of a new job card.
    """
    if created:
        instance.acknowledged = False
        instance.save()

@receiver(m2m_changed, sender=JobCard.assigned_users.through)
def reset_acknowledgement_on_assignment_change(sender, instance, action, reverse, model, pk_set, **kwargs):
    """
    Signal handler to set acknowledged to False when assigned users change
    """
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        instance.acknowledged = False
        instance.acknowledged_at = None
        instance.save()

@receiver(post_save, sender=JobCard)
def reset_acknowledgement_on_status_update(sender, instance,  **kwargs):
    """
    Signal handler to set acknowledged to False when job status is changed
    """
    if not kwargs.get('created',False) and kwargs.get('update_fields') and  'status' in kwargs.get('update_fields') and 'remarks' not in kwargs.get('update_fields'):
       instance.acknowledged = False
       instance.acknowledged_at = None
       instance.save()

@receiver(post_save, sender=JobCard)
def create_log_entry_on_remark_update(sender, instance, **kwargs):
    """
    Signal handler to create LogEntry when a JobCard's remarks field is updated.
    """
    if not kwargs.get('created', False) and kwargs.get('update_fields') and 'remarks' in kwargs.get('update_fields'):
        if instance.remarks:
            current_time = timezone.localtime()
            log_entry = LogEntry.objects.create(
                date = current_time.date(),
                time = current_time.time(),
                location = instance.location,
                remarks = f"[Job Card: {instance.job_card_number}] : {instance.remarks}",
                )
            log_entry.initials.set(instance.assigned_users.all())