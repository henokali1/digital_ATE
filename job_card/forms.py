from django import forms
from django.contrib.auth.models import User
from .models import JobCard

class JobCardForm(forms.ModelForm):
    assigned_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Assigned To"
    )
    class Meta:
        model = JobCard
        fields = ['task_description', 'assigned_users', 'priority_level', 'maintenance_type', 'location', 'status', 'remarks']
        exclude = ['created_at', 'created_by', 'updated_at','acknowledged', 'acknowledged_at']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_users'].label_from_instance = self.user_full_name

    def user_full_name(self, user):
        return f'{user.first_name} {user.last_name}'
    
    def clean(self):
         cleaned_data = super().clean()
         status = cleaned_data.get('status')
         maintenance_type = cleaned_data.get('maintenance_type')
         preventive_maintenance = self.instance.preventive_maintenance_id
         corrective_maintenance = self.instance.corrective_maintenance_id
         
         if status == 'Completed':
             if maintenance_type == 'Preventive' and not preventive_maintenance:
                 raise forms.ValidationError("A preventive maintenance record must be created before marking the job card as completed.")
             if maintenance_type == 'Corrective' and not corrective_maintenance:
                  raise forms.ValidationError("A corrective maintenance record must be created before marking the job card as completed.")
         return cleaned_data