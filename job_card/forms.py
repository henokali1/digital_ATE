from django import forms
from .models import JobCard

class JobCardForm(forms.ModelForm):
    class Meta:
        model = JobCard
        fields = ['task_description', 'assigned_users', 'priority_level', 'maintenance_type', 'location', 'status']
        exclude = ['created_at', 'created_by', 'updated_at']
        widgets = {
            'assigned_users': forms.CheckboxSelectMultiple(),
        }
