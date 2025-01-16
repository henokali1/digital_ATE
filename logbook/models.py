# logbook/models.py
from django.db import models
from django.contrib.auth.models import User
from location.models import Location

class LogEntry(models.Model):
    logged_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    time = models.TimeField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    initials = models.ManyToManyField(User, related_name='logbook_entries')
    photos = models.ImageField(upload_to='logbook_photos/', blank=True)
    remarks = models.TextField()

    def __str__(self):
        initials_list = ", ".join([user.username for user in self.initials.all()])
        return f"Log Entry by {initials_list} on {self.date}"
