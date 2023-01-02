from django.contrib import admin
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'role']
    list_filter = ['premium', 'created_at', 'role']
    search_fields = ['email', 'first_name', 'last_name']