from django.contrib import admin
from django.utils.html import format_html

#MODEL
from .models import (
    FoodItem,
    Category
)
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['vendor', 'name']
    prepopulated_fields = {"slug": ("name",)}  
    list_display_links = ['vendor', 'name']

class FoodItemAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" width=30/>'.format(obj.image.url))
    image_tag.short_description = 'Image'

    list_display = ['vendor', 'image_tag','category', 'food_title', 'price', 'is_available']
    prepopulated_fields = {"slug": ("food_title",)}  
    list_display_links = ['vendor', 'category']
    list_editable = ['is_available']

admin.site.register(Category, CategoryAdmin)
admin.site.register(FoodItem, FoodItemAdmin)



