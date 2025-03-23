# preventive_maintenance/models.py
from django.db import models
from django.contrib.auth.models import User
from location.models import Location
from asset.models import Asset
from datetime import datetime, timedelta

class PreventiveMaintenance(models.Model):
    SECTION_CHOICES = [
        ('Communication', 'Communication'),
        ('Navigation', 'Navigation'),
        ('Surveillance', 'Surveillance'),
        ('Aviation Networks', 'Aviation Networks'),
        ('Miscellaneous', 'Miscellaneous'),
    ]

    logged_at = models.DateTimeField(auto_now_add=True)
    logged_by = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    duration = models.FloatField(editable=False, default=0)  # Auto-calculated in hours
    section = models.CharField(max_length=50, choices=SECTION_CHOICES)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    asset = models.ManyToManyField(Asset, related_name='preventive_maintenances') # Changed to ManyToMany
    PPM_Form = models.FileField(upload_to='uploads/forms/')
    photo = models.ImageField(upload_to='uploads/photos/', blank=True, null=True)
    remarks = models.TextField()
    task_description = models.TextField(blank=True, null=True) 
    completed_by = models.ManyToManyField(User, related_name='preventive_maintenance_completed_by')

    def save(self, *args, **kwargs):
        # Calculate duration in hours
        start_datetime = datetime.combine(self.start_date, self.start_time)
        end_datetime = datetime.combine(self.end_date, self.end_time)
        self.duration = round((end_datetime - start_datetime).total_seconds() / 3600, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.pk}"
