from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

#MODELS
from .models import (
    User,
    UserProfile
)
# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'role', 'is_active')
    list_display_links =('email', 'username')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'country', 'state', 'pincode']
    list_display_links = ['user']

admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

