# daily_inspection/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import DailyInspection, Asset

@receiver(post_save, sender=DailyInspection)
def update_inspection_progress(sender, instance, created, **kwargs):
    """Update inspection progress for all inspections in the same shift when a new inspection is created"""
    if created:
        current_date = timezone.now().date()
        related_inspections = DailyInspection.objects.filter(
            inspected_at__date=current_date,
            shift=instance.shift
        ).exclude(pk=instance.pk)
        
        for inspection in related_inspections:
            # inspection.calculate_inspection_progress()
            inspection.save()
