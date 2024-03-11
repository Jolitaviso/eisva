from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from . import models


class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'owner', 'created_at', 'recent_communications']
    list_display_links = ['id', 'name']
    list_filter = ['owner', 'created_at']
    search_fields = ['name', 'owner' 'description', 'owner__last_name', 'owner__username']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['owner']
    fieldsets = (
        (None, {
            'fields': (
                'name', 'owner', 'youtube_video','description',
            ),
        }),
        (_('temporal tracking').title(), {
            'fields': ('created_at', 'updated_at'),
        }),
    )
 
    def recent_communications(self, obj: models.Blog):
        return "; ".join(obj.communications.order_by('-created_at').values_list('name', flat=True)[:3])
    recent_communications.short_description = _('recent communications')
    
    

class CommunicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'blog', 'owner', 'created_at']
    list_filter =  ['created_at']
    search_fields = ['name', 'description', 'blog__name', 'owner__last_name', 'owner__username']
    list_editable = ['owner', 'blog']
    readonly_fields = ['id', 'created_at', 'updated_at']
    autocomplete_fields = ['owner']
    fieldsets = (
        (_("general").title(), {
            "fields": (
                'name',
                'description',
            ),
        }),
        (_("ownership").title(), {
            "fields": (
                'owner',
                 'blog',
            ),
        }),
        (_("temporal tracking").title(), {
            "fields": (
                ('created_at', 'updated_at', 'id'),
            ),
        }),
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner','communication', 'created_at']
    list_filter =  ['created_at', 'owner']
    search_fields = ['title', 'note', 'owner__last_name', 'owner__username']
    readonly_fields = ['id', 'created_at', 'updated_at']
    autocomplete_fields = ['communication', 'owner']
    fieldsets = (
        (_("general").title(), {
            "fields": (
                'title',
                'note',
            ),
        }),
        (_("ownership").title(), {
            "fields": (
                'owner',
            ),
        }),
        (_("temporal tracking").title(), {
            "fields": (
                ('created_at', 'updated_at', 'id'),
            ),
        }),
    )
    
class BlogLikeAdmin(admin.ModelAdmin):
    list_display = ['blog', 'user', 'like']
    
class CommunicationLikeAdmin(admin.ModelAdmin):
    list_display = ['communication', 'user', 'like']    

    
admin.site.register(models.Blog, BlogAdmin)
admin.site.register(models.Communication, CommunicationAdmin)
admin.site.register(models.Comment, CommentAdmin)