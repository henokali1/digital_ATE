from django import forms
from .models import SparePart, SparePartPhoto, CalibrationHistory, MaintenanceHistory, MaintenancePhoto
from location.models import Location

class SparePartForm(forms.ModelForm):
    class Meta:
        model = SparePart
        # Exclude created_by and updated_by from the form
        exclude = ['created_at', 'updated_at', 'created_by', 'updated_by', 'position_rack']  # Or specify the fields you want to include
        # widgets = {
        #     'description': forms.Textarea(attrs={'rows': 3}),
        #     'installation_date': forms.DateInput(attrs={'type': 'date'}),
        # }

class SparePartPhotoForm(forms.ModelForm):
    class Meta:
        model = SparePartPhoto
        fields = ['photo']

SparePartPhotoFormSet = forms.inlineformset_factory(
    SparePart, SparePartPhoto, form=SparePartPhotoForm,
    extra=3, can_delete=True  # Start with 3 empty photo upload fields
)

class CalibrationHistoryForm(forms.ModelForm):
    class Meta:
        model = CalibrationHistory
        fields = ['date', 'remarks', 'calibration_certificate']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class MaintenanceHistoryForm(forms.ModelForm):
    class Meta:
        model = MaintenanceHistory
        fields = ['date', 'remarks']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class MaintenancePhotoForm(forms.ModelForm):
    class Meta:
        model = MaintenancePhoto
        fields = ['photo']

MaintenancePhotoFormSet = forms.inlineformset_factory(
    MaintenanceHistory, MaintenancePhoto, form=MaintenancePhotoForm,
    extra=1, can_delete=True
)

class UploadCSVForm(forms.Form):
    csv_file = forms.FileField(label="CSV File")

class SparePartFilterForm(forms.Form):
    section = forms.ChoiceField(choices=[('', 'All Sections')] + list(SparePart.SECTION_CHOICES), required=False)
    location = forms.ModelChoiceField(queryset=Location.objects.all(), required=False, empty_label="All Locations")
    shelf_number = forms.CharField(max_length=50, required=False)
    shelf_level = forms.CharField(max_length=50, required=False)
    box_number = forms.CharField(max_length=50, required=False)
    status = forms.ChoiceField(choices=[('', 'All Statuses')] + list(SparePart.STATUS_CHOICES), required=False)