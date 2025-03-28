from django.db import models
from django.contrib.auth.models import User
from location.models import Location
from preventive_maintenance.models import PreventiveMaintenance
from corrective_maintenance.models import CorrectiveMaintenance
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

    MAINTENANCE_TYPE = [
        ('Preventive', 'Preventive'),
        ('Corrective', 'Corrective'),
        ('Not Required', 'Not Required'),
    ]

    created_at = models.DateTimeField(default=now, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    job_card_number = models.CharField(
        max_length=50, unique=True, editable=False
    )
    task_description = models.CharField(max_length=255)
    assigned_users = models.ManyToManyField(User, related_name='assigned_jobs', blank=True)
    priority_level = models.CharField(max_length=10, choices=PRIORITY_CHOICES, blank=True, null=True)
    maintenance_type = models.CharField(max_length=15, choices=MAINTENANCE_TYPE, default='Not Required')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Pending')
    preventive_maintenance_id = models.ForeignKey(PreventiveMaintenance, on_delete=models.CASCADE, blank=True, null=True)
    corrective_maintenance_id = models.ForeignKey(CorrectiveMaintenance, on_delete=models.CASCADE, blank=True, null=True)
    acknowledged = models.BooleanField(default=False, editable=False)
    acknowledged_at = models.DateTimeField(null=True, blank=True, editable=False)
    remarks = models.TextField(blank=True, null=True)
    time_to_acknowledge = models.DurationField(null=True, blank=True, editable=False)
    completed_at = models.DateTimeField(null=True, blank=True, editable=False)
    time_to_complete = models.DurationField(null=True, blank=True, editable=False)
    
    start_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)

    requires_oem_support = models.BooleanField(default=False)
    image = models.ImageField(upload_to='job_card_images/', blank=True, null=True)  # Add image field
    status_update_image = models.ImageField(upload_to='job_card_status_images/', blank=True, null=True) # image for status update
    def save(self, *args, **kwargs):
        if not self.job_card_number:
            self.job_card_number = f"JC-{uuid.uuid4().hex[:8]}-{now().strftime('%d-%m-%Y')}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.job_card_number} - {self.task_description}"

class JobCardMessage(models.Model):
    job_card = models.ForeignKey('JobCard', on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']

class JobCardImage(models.Model):
    message = models.ForeignKey(JobCardMessage, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='job_card_chat/')
    uploaded_at = models.DateTimeField(auto_now_add=True)