# daily_inspection/models.py
from django.db import models
from django.contrib.auth.models import User
from asset.models import Asset
from django.utils import timezone

class DailyInspection(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    STATUS_CHOICES = [
        ('OK', 'Ok'),
        ('WARNING', 'Warning'),
        ('ALARM', 'Alarm'),
        ('DONE', 'Done'),
        ('OFF', 'Off'),
        ('UNSERVICEABLE', 'Unserviceable'),
    ]

    SHIFT_CHOICES = [
        ('DAY', 'Day'),
        ('NIGHT', 'Night'),
    ]

    status = models.CharField(max_length=30, blank=True, null=True) 
    inspected_at = models.DateTimeField(blank=True, null=True)
    inspected_by = models.ManyToManyField(
        User,
        related_name='daily_inspections',
        blank=True
    )
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    shift = models.CharField(max_length=5, choices=SHIFT_CHOICES)
    remarks = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='inspection_photos/', blank=True, null=True)
