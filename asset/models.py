# asset/models.py
from django.db import models
from location.models import Location
import uuid


class PositionRack(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Name of the rack or position")

    def __str__(self):
        return self.name

class Asset(models.Model):
    STATUS_CHOICES = [
        ('In Use', 'In Use'),
        ('Spare', 'Spare'),
        ('Under Maintenance', 'Under Maintenance'),
        ('Unserviceable', 'Unserviceable'),
    ]

    SECTION_CHOICES = [
        ('Communication', 'Communication'),
        ('Navigation', 'Navigation'),
        ('Surveillance', 'Surveillance'),
        ('Aviation Networks', 'Aviation Networks'),
        ('Miscellaneous', 'Miscellaneous'),
    ]

    name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=50, unique=True, editable=True, blank=True)
    tag_id = models.CharField(max_length=50, unique=True, editable=True, blank=True)
    section = models.CharField(max_length=50, choices=SECTION_CHOICES, default='Surveillance')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    position_rack = models.ForeignKey(PositionRack, on_delete=models.SET_NULL, blank=True, null=True, help_text="Position or rack where the asset is located")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='In Use')
    manufacturer = models.CharField(max_length=50, blank=True, null=True)
    model_number = models.CharField(max_length=50, blank=True, null=True)
    part_number = models.CharField(max_length=50, blank=True, null=True)
    morning_shift_daily_inspection_required = models.BooleanField(default=False)
    night_shift_daily_inspection_required = models.BooleanField(default=False)
    preventive_maintenance_required = models.BooleanField(default=True)
    corrective_maintenance_required = models.BooleanField(default=False)
    remarks = models.CharField(max_length=250, blank=True, null=True)
    photo = models.ImageField(upload_to='assets_photos/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.tag_id:  # Only generate a tag_id if it doesn't already exist
            self.tag_id = f"TAG-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
