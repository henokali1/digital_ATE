from django import forms
from django.contrib.auth.models import User
from .models import JobCard
from .models import JobCardMessage, JobCardImage

class JobCardForm(forms.ModelForm):
    assigned_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(userprofile__ate_staff=True),
        widget=forms.CheckboxSelectMultiple,
        label="Assigned To"
    )
    class Meta:
        model = JobCard
        fields = ['image', 'task_description', 'assigned_users', 'priority_level', 'maintenance_type', 'location', 'status', 'start_date', 'due_date','remarks', 'requires_oem_support'] # Add 'requires_oem_support'
        exclude = ['created_at', 'created_by', 'updated_at','acknowledged', 'acknowledged_at']
        widgets ={
             'start_date': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
        }
        
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


class JobCardMessageForm(forms.ModelForm):
    class Meta:
        model = JobCardMessage
        fields = ['message']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].widget.attrs.update({'class': 'form-control', 'rows': '3'})

class CSVImportForm(forms.Form):
    csv_file = forms.FileField(
        label='Select CSV File',
        help_text='File must be in CSV format with required headers',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.csv'
        })
    )