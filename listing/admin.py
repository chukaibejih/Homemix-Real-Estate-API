from django.contrib import admin
from .models import Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['seller', 'city', 'state', 'property_type', 'price']
    list_filter = ['status', 'city', 'state', 'property_type']
    date_hierarchy = 'posted'
    ordering = ['status', 'posted', 'price']
