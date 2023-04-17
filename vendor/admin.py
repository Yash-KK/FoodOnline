from django.contrib import admin

#MODEL
from .models import (
    Vendor
)
# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_approved']
    list_editable = ['is_approved']
admin.site.register(Vendor, VendorAdmin)

