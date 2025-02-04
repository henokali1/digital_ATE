from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class FeatureRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending Review', 'Pending Review'),
        ('Approved', 'Approved'),
        ('In Progress', 'In Progress'),
        ('Implemented', 'Implemented'),
        ('Rejected', 'Rejected'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to='feature_requests/', blank=True, null=True)
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    date_requested = models.DateTimeField(default=timezone.now, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending Review')
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title