from django import forms
from .models import JobCard

class JobCardForm(forms.ModelForm):
    class Meta:
        model = JobCard
        fields = ['task_description', 'assigned_users', 'priority_level', 'location', 'status']
        widgets = {
            'assigned_users': forms.CheckboxSelectMultiple(),
        }
