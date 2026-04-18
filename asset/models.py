 # asset/models.py
from django.db import models
from location.models import Location
import uuid
from django.contrib.auth.models import User

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
    installation_date = models.DateField(blank=True, null=True)
    oem_life_span = models.PositiveIntegerField(default=10, help_text="OEM recommended life span in years")

    def save(self, *args, **kwargs):
        if not self.tag_id:  # Only generate a tag_id if it doesn't already exist
            self.tag_id = f"TAG-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    @property
    def end_of_life_date(self):
        if self.installation_date and self.oem_life_span:
            try:
                return self.installation_date.replace(year=self.installation_date.year + self.oem_life_span)
            except ValueError:
                return self.installation_date.replace(year=self.installation_date.year + self.oem_life_span, day=28)
        return None

    @property
    def lifecycle_status(self):
        """Returns 'expired', 'nearing' (within 1 year), or 'active'."""
        from django.utils import timezone
        eol = self.end_of_life_date
        if not eol:
            return 'unknown'
        today = timezone.now().date()
        if today > eol:
            return 'expired'
        from datetime import date
        one_year_ahead = today.replace(year=today.year + 1)
        if today >= eol.replace(year=eol.year - 1):
            return 'nearing'
        return 'active'

    def __str__(self):
        return f'{self.name} - {self.position_rack} | {self.serial_number}'

class AssetHistory(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='history')
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    remarks = models.TextField(blank=True)
    photo = models.ImageField(upload_to='asset_history_photos/', blank=True, null=True)
    document = models.FileField(upload_to='asset_history_documents/', blank=True, null=True)

    def __str__(self):
        return f"History for {self.asset.name} at {self.timestamp}"


class CalibrationHistory(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='calibration_history')
    calibration_date = models.DateField()
    next_calibration_date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-calibration_date']

    def __str__(self):
        return f"Calibration – {self.asset.name} on {self.calibration_date}"


class CalibrationDocument(models.Model):
    calibration = models.ForeignKey(CalibrationHistory, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to='calibration_certificates/')
    name = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or str(self.document)
