from django import forms

#MODEL
from .models import (
    Vendor
)


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name','license', 'is_approved']
