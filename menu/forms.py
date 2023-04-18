from django import forms

#MODEL
from .models import (
    Category,
    FoodItem
)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['category', 'food_title', 'description', 'price', 'image', 'is_available']

    def __init__(self, *args, **kwargs):
        super(FoodItemForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['placeholder'] = field.label