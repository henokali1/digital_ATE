from django.db import models
from django.contrib.auth.models import User
from location.models import Location
from asset.models import Asset

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
    date = models.DateField()
    time = models.TimeField()
    section = models.CharField(max_length=50, choices=SECTION_CHOICES)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    PPM_Form = models.FileField(upload_to='uploads/forms/')
    photo = models.ImageField(upload_to='uploads/photos/', blank=True, null=True) 
    remarks = models.TextField()

    def __str__(self):
        return f"{self.asset} - {self.date}"
