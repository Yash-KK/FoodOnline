from django import forms


#MODEL
from .models import (
    User,
    UserProfile
)


class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())    

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Password and Confirm Password do not match!"
            )
        
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)        
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name...'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name...'
        self.fields['username'].widget.attrs['placeholder'] = 'Username....'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'

        self.fields['password'].widget.attrs['placeholder'] = 'Password...'
        self.fields['confirm_password'].widget.attrs['placeholder'] = 'Confirm Password....'

class UserProfileForm(forms.ModelForm):    
    class Meta:
        model = UserProfile
        fields = ['profile_pic', 'cover_photo', 'address_line', 'country', 'state', 'city', 'pincode', 'latitude', 'longitude']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['latitude'].widget.attrs['readonly'] = True
            self.fields['longitude'].widget.attrs['readonly'] = True