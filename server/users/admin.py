from django.contrib import admin
from django.contrib.admin import register
from .models import Users

# Register your models here.

@register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'date_joined']
    list_display_links = ['id', 'username']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'date_joined']
    readonly_fields = ['id', 'date_joined']
    exclude = ['password', 'last_login']