# daily_inspection/models.py
from django.db import models
from django.contrib.auth import get_user_model
from asset.models import Asset
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

class DailyInspection(models.Model):
    SHIFT_CHOICES = [
        ('Day', 'Day Shift'),
        ('Night', 'Night Shift'),
    ]
    
    STATUS_CHOICES = [
        ('Ok', 'Ok'),
        ('Warning', 'Warning'),
        ('Alarm', 'Alarm'),
        ('Done', 'Done'),
        ('Off', 'Off'),
        ('Unserviceable', 'Unserviceable'),
    ]
    
    COMPLETED_STATUSES = ['Ok', 'Warning', 'Alarm', 'Done', 'Unserviceable']
    
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    inspected_at = models.DateTimeField(auto_now_add=True)
    inspected_by = models.ForeignKey(User, on_delete=models.CASCADE)
    shift = models.CharField(max_length=5, choices=SHIFT_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    remarks = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='inspection_photos/', blank=True, null=True)
    inspection_progress = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage of completed inspections for the shift"
    )

    class Meta:
        ordering = ['-inspected_at']
        
    def __str__(self):
        return f"{self.asset.name} - {self.shift} Inspection on {self.inspected_at.date()}"

    @staticmethod
    def calculate_shift_progress(shift, date=None):
        """
        Calculate the inspection progress for a specific shift
        Returns the progress percentage
        """
        if date is None:
            date = timezone.now().date()

        # Get all inspections for this shift and date
        inspections = DailyInspection.objects.filter(
            inspected_at__date=date,
            shift=shift
        )
        
        # Count completed inspections (those with status in COMPLETED_STATUSES)
        completed_count = inspections.filter(
            status__in=DailyInspection.COMPLETED_STATUSES
        ).count()
        
        # Get total required inspections for the shift
        if shift == 'Day':
            total_required = Asset.objects.filter(
                morning_shift_daily_inspection_required=True
            ).count()
        else:
            total_required = Asset.objects.filter(
                night_shift_daily_inspection_required=True
            ).count()
        
        if total_required == 0:
            return 100.0
            
        progress = (completed_count * 100.0) / total_required
        return min(100.0, progress)  # Ensure we don't exceed 100%

@receiver(post_save, sender=DailyInspection)
def update_inspection_progress(sender, instance, **kwargs):
    """
    Signal handler to update inspection progress when an inspection is saved
    """
    # Calculate new progress
    progress = DailyInspection.calculate_shift_progress(
        instance.shift,
        instance.inspected_at.date()
    )
    
    # Update progress for all inspections in this shift
    DailyInspection.objects.filter(
        inspected_at__date=instance.inspected_at.date(),
        shift=instance.shift
    ).update(inspection_progress=progress)