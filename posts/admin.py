from django.contrib import admin
from .models import Post, Comment, Announcement, Notification
from django.utils.html import format_html

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'show_media')
    list_filter = ('created_at', 'post_type')
    search_fields = ('title', 'content', 'author__username')
    date_hierarchy = 'created_at'
    readonly_fields = ('show_media_preview',)
    
    def show_media(self, obj):
        if obj.media:
            if obj.media.url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                return format_html('<img src="{}" style="max-height: 50px;">', obj.media.url)
            elif obj.media.url.lower().endswith(('.mp4', '.mov', '.avi', '.webm')):
                return format_html('<video width="50" height="50" controls><source src="{}" type="video/mp4"></video>', obj.media.url)
            else:
                return format_html('<a href="{}">File</a>', obj.media.url)
        return '-'
    show_media.short_description = 'Media'
    
    def show_media_preview(self, obj):
        if obj.media:
            if obj.media.url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                return format_html('<img src="{}" style="max-width: 300px; max-height: 300px;">', obj.media.url)
            elif obj.media.url.lower().endswith(('.mp4', '.mov', '.avi', '.webm')):
                return format_html('<video width="300" height="300" controls><source src="{}" type="video/mp4"></video>', obj.media.url)
            else:
                return format_html('<a href="{}">File</a>', obj.media.url)
        return '-'
    show_media_preview.short_description = 'Media Preview'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username', 'post__title')
    date_hierarchy = 'created_at'

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'is_active', 'created_by')
    list_filter = ('is_active', 'event_date')
    search_fields = ('title', 'content')
    date_hierarchy = 'event_date'
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new announcement
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'notification_type', 'actor', 'post', 'created_at', 'is_read')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('recipient__username', 'actor__username', 'post__title')
    date_hierarchy = 'created_at'
