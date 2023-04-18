from django.contrib import admin

from .models import (
    Cart
)
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ['fooditem', 'quantity', 'user']
    list_display_links = ['fooditem']
admin.site.register(Cart, CartAdmin)

