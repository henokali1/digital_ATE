# corrective_maintenance/models.py
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from location.models import Location
from asset.models import Asset

class CorrectiveMaintenance(models.Model):
    TYPE_CHOICES = [
        ('General Problem', 'General Problem'),
        ('Outage', 'Outage'),
        ('Warning', 'Warning'),
        ('Alarm', 'Alarm'),
    ]

    SECTION_CHOICES = [
        ('Communication', 'Communication'),
        ('Navigation', 'Navigation'),
        ('Surveillance', 'Surveillance'),
        ('Aviation Networks', 'Aviation Networks'),
        ('Miscellaneous', 'Miscellaneous'),
    ]

    logged_at = models.DateTimeField(auto_now_add=True)
    logged_by = models.ForeignKey(User, on_delete=models.CASCADE)
    # job_card_id = models.ForeignKey(JobCard, on_delete=models.CASCADE, blank=True, null=True)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    duration = models.FloatField(editable=False)  # Auto-calculated in hours
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    section = models.CharField(max_length=50, choices=SECTION_CHOICES)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    asset = models.ManyToManyField(Asset, related_name='corrective_maintenances') 
    corrective_action = models.TextField()
    preventive_action = models.TextField(blank=True, null=True)
    root_cause = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    task_description = models.TextField(blank=True, null=True) 
    completed_by = models.ManyToManyField(User, related_name='correctie_maintenance_completed_by')
    photo = models.ImageField(upload_to='uploads/corrective_photos/', blank=True, null=True)
    ROSI_NO = models.CharField(max_length=50, blank=True, null=True)
    incident_report = models.FileField(upload_to='uploads/incident_reports/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Calculate duration in hours
        start_datetime = datetime.combine(self.start_date, self.start_time)
        end_datetime = datetime.combine(self.end_date, self.end_time)
        self.duration = round((end_datetime - start_datetime).total_seconds() / 3600, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.pk}"
