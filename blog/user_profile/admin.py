from django.contrib import admin
from . import models
from django.utils.translation import gettext_lazy as _


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'description']  
    list_editable = ['description'] 
    
    
class MessageAdmin(admin.ModelAdmin):
    list_display = ['text', 'sender', 'timestamp']
    list_display_links = ['text', 'sender']
    list_filter = ['sender']
    search_fields = ['text',]
    date_hierarchy = 'timestamp'
    readonly_fields = ['timestamp']
    fieldsets = (
        (_("general"), {
            "fields": (
                'sender',
                'text',
                'image',
                'document',
                'receiver',
            ),
        }),
        (_("temporal tracking"), {
            "fields": (
                ('timestamp'),
            ),
        }),
    )

admin.site.register(models.Profile)
admin.site.register(models.Message, MessageAdmin)