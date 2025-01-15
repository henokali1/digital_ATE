from django import forms
from django.contrib.auth.models import User
from .models import JobCard

class JobCardForm(forms.ModelForm):
    assigned_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label="Assigned To"
    )
    class Meta:
        model = JobCard
        fields = ['task_description', 'assigned_users', 'priority_level', 'maintenance_type', 'location', 'status']
        exclude = ['created_at', 'created_by', 'updated_at']
