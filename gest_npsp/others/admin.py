from django.contrib import admin
from .models import ContactModel

@admin.register(ContactModel)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'sujet', 'message',)
    ordering = ('nom', 'email')
    search_fields = ('nom', 'email')