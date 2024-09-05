from django.contrib import admin
from .models import Mails

# Register your models here.

@admin.register(Mails)
class MailsAdmin(admin.ModelAdmin):
    pass
