from django import forms
from .models import Asset
from location.models import Location

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'serial_number', 'tag_id', 'section', 'location', 'status', 
                 'manufacturer', 'model_number', 'part_number', 'quantity', 'remarks', 'photo']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.NumberInput, forms.Select, forms.Textarea)):
                field.widget.attrs.update({'class': 'form-control'})
            if isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class': 'form-control'})
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})