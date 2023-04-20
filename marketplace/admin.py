from django.contrib import admin

from .models import (
    Cart,
    Tax
)
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ['fooditem', 'quantity', 'user']
    list_display_links = ['fooditem']

class TaxAdmin(admin.ModelAdmin):
    list_display = ['tax_type', 'tax_percentage', 'is_active']
    list_display_links = ['tax_type', 'tax_percentage']

admin.site.register(Cart, CartAdmin)
admin.site.register(Tax, TaxAdmin)

