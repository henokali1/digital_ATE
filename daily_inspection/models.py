# daily_inspection/models.py
from django.db import models
from django.contrib.auth.models import User
from asset.models import Asset
from django.utils import timezone


class InspectionIdent(models.Model):
    inspection_ident = models.AutoField(primary_key=True)
    initiated_at = models.DateTimeField(default=timezone.now, editable=False)
    shift = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return f"Inspection ID: {self.inspection_ident} - Shift: {self.shift} - initiated_at: {self.initiated_at}"


class DailyInspection(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    inspection_ident = models.ForeignKey(InspectionIdent, on_delete=models.CASCADE, null=True, blank=True, related_name='daily_inspections')                                                                                                                                                                                                                                                                                                                                                                                                                  
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

    def __str__(self):
        return f'{self.created_at} - {self.shift} - {self.asset}'
