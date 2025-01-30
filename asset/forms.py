# asset/forms.py
from django import forms
from .models import Asset, PositionRack, AssetHistory
from location.models import Location

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = [
            # Basic Information
            'name', 'serial_number', 'tag_id',
            # Classification
            'section', 'status',
            # Location Information
            'location', 'position_rack',
            # Technical Details
            'manufacturer', 'model_number', 'part_number',
            # Maintenance Requirements
            'morning_shift_daily_inspection_required',
            'night_shift_daily_inspection_required',
            'preventive_maintenance_required',
            'corrective_maintenance_required',
            # Additional Information
            'remarks', 'photo', 'installation_date'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter asset name'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter serial number'}),
            'tag_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Leave blank for auto-generation'}),
            'section': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
            'position_rack': forms.Select(attrs={'class': 'form-select'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter manufacturer name'}),
            'model_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter model number'}),
            'part_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter part number'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter any additional remarks'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'installation_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        }
        labels = {
            'morning_shift_daily_inspection_required': 'Morning Shift Inspection',
            'night_shift_daily_inspection_required': 'Night Shift Inspection',
            'preventive_maintenance_required': 'Preventive Maintenance',
            'corrective_maintenance_required': 'Corrective Maintenance',
        }
        help_texts = {
            'tag_id': 'Leave blank for automatic generation',
            'position_rack': 'Select the position or rack where the asset is located',
            'status': 'Current operational status of the asset',
            'section': 'Sectoin with in the ATE Department the asset belongs to',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make certain fields optional
        optional_fields = ['manufacturer', 'model_number', 'part_number', 'remarks', 'photo', 'installation_date']
        for field in optional_fields:
            self.fields[field].required = False

        # Add Bootstrap switch classes to boolean fields
        boolean_fields = [
            'morning_shift_daily_inspection_required',
            'night_shift_daily_inspection_required',
            'preventive_maintenance_required',
            'corrective_maintenance_required'
        ]
        for field in boolean_fields:
            self.fields[field].widget.attrs.update({'class': 'form-check-input'})

    def clean_serial_number(self):
        serial_number = self.cleaned_data.get('serial_number')
        if serial_number:
            # Check if serial number exists for other assets
            if Asset.objects.filter(serial_number=serial_number).exclude(id=self.instance.id).exists():
                raise forms.ValidationError('This serial number is already in use.')
        return serial_number

    def clean_tag_id(self):
        tag_id = self.cleaned_data.get('tag_id')
        if tag_id:
            # Check if tag ID exists for other assets
            if Asset.objects.filter(tag_id=tag_id).exclude(id=self.instance.id).exists():
                raise forms.ValidationError('This tag ID is already in use.')
        return tag_id

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            # Validate file size (max 5MB)
            if photo.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Image file size must be less than 5MB.')
            # Validate file extension
            valid_extensions = ['.jpg', '.jpeg', '.png']
            import os
            ext = os.path.splitext(photo.name)[1].lower()
            if ext not in valid_extensions:
                raise forms.ValidationError('Unsupported file extension. Please use .jpg, .jpeg or .png')
        return photo

class CSVImportForm(forms.Form):
    csv_file = forms.FileField(
        label='Select CSV File',
        help_text='File must be in CSV format with required headers',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.csv'
        })
    )

class AssetHistoryForm(forms.ModelForm):
    class Meta:
        model = AssetHistory
        fields = ['remarks', 'photo', 'document']
        widgets = {
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter remarks about the asset'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'document': forms.FileInput(attrs={'class': 'form-control'}),
        }
