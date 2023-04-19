from django.contrib import admin

#MODEL
from .models import (
    Vendor,
    OpeningHour
)
# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_approved']
    list_editable = ['is_approved']

class OpeningHourAdmin(admin.ModelAdmin):
    list_display = ['vendor', 'day', 'from_hour', 'to_hour', 'is_closed']
    list_display_links = ['vendor', 'day']
    list_editable = ['is_closed']

admin.site.register(Vendor, VendorAdmin)
admin.site.register(OpeningHour, OpeningHourAdmin)

