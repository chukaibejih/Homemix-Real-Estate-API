from django.contrib import admin
from .models import User, Property

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'role']
    list_filter = ['premium', 'created_at', 'role']
    search_fields = ['email', 'first_name', 'last_name']


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['seller', 'city', 'state', 'property_type', 'price']
    list_filter = ['status', 'city', 'state', 'property_type']
    date_hierarchy = 'posted'
    ordering = ['status', 'posted', 'price']
