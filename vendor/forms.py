from django import forms

#MODEL
from .models import (
    Vendor,
    OpeningHour
)


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name','license', 'is_approved']

class OpeningHourForm(forms.ModelForm):
    class Meta:
        model = OpeningHour
        fields = ['day', 'from_hour', 'to_hour', 'is_closed']