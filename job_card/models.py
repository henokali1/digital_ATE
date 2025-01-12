from django.db import models
from django.contrib.auth.models import User
from location.models import Location
from django.utils.timezone import now
import uuid

class JobCard(models.Model):
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('On Hold', 'On Hold'),
        ('Rejected', 'Rejected'),
    ]

    created_at = models.DateTimeField(default=now, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    job_card_number = models.CharField(
        max_length=50, unique=True, editable=False
    )
    task_description = models.CharField(max_length=255)
    assigned_users = models.ManyToManyField(User, related_name='assigned_jobs', blank=True)
    priority_level = models.CharField(max_length=10, choices=PRIORITY_CHOICES, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Pending')

    def save(self, *args, **kwargs):
        if not self.job_card_number:
            self.job_card_number = f"JC-{uuid.uuid4().hex[:8]}-{now().strftime('%d-%m-%Y')}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.job_card_number} - {self.task_description}"
