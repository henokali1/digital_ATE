from django.db import models
from django.contrib.auth.models import User
from location.models import Location

class LogEntry(models.Model):
    logged_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    time = models.TimeField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    initials = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logbook_entries')
    photos = models.ImageField(upload_to='logbook_photos/', blank=True)
    remarks = models.TextField()

    def __str__(self):
        return f"Log Entry by {self.initials} on {self.date}"
