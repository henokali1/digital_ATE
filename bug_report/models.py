from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class BugReport(models.Model):
    SEVERITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    steps_to_reproduce = models.TextField(blank=True, null=True)
    expected_behavior = models.TextField(blank=True, null=True)
    actual_behavior = models.TextField(blank=True, null=True)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='Medium')
    screenshot = models.FileField(upload_to='bug_report_screenshots/', blank=True, null=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_reported = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_reported'] # Sort by date reported, newest first