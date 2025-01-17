from django.db import models
from location.models import Location

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
    serial_number = models.CharField(max_length=50, unique=True)
    tag_id = models.CharField(max_length=50, unique=True)
    section = models.CharField(max_length=50, choices=SECTION_CHOICES, default='Communication')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='In Use')
    manufacturer = models.CharField(max_length=50, blank=True, null=True)
    model_number = models.CharField(max_length=50, blank=True, null=True)
    part_number = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    remarks = models.CharField(max_length=250, blank=True, null=True)
    photo = models.ImageField(upload_to='assets_photos/', blank=True, null=True)

    def __str__(self):
        return self.name
