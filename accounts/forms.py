from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import UserProfile, Position
from django.contrib.auth.models import User

class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #Make all fields disabled except profile_picture
        for field_name, field in self.fields.items():
            if field_name != 'profile_picture':
                field.widget.attrs['disabled'] = True
                field.widget.attrs['readonly'] = True  # for some widget types
        self.fields['profile_picture'].widget.attrs.update({'class': 'form-control'})


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            # field.widget.attrs['disabled'] = True #Make all fields disabled
            # field.widget.attrs['readonly'] = True #Make all fields readonly