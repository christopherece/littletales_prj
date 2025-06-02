from django.contrib import admin
from .models import LearningActivity, ActivityResource, ActivityProgress, DevelopmentMilestone, MilestoneProgress, Notification

@admin.register(LearningActivity)
class LearningActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'age_group', 'created_at')
    list_filter = ('category', 'age_group')
    search_fields = ('title', 'description')
    ordering = ('category', 'title')

@admin.register(ActivityResource)
class ActivityResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'activity', 'created_at')
    list_filter = ('activity__category',)
    search_fields = ('title', 'description')
    ordering = ('-created_at',)

@admin.register(ActivityProgress)
class ActivityProgressAdmin(admin.ModelAdmin):
    list_display = ('child', 'activity', 'completed', 'updated_at')
    list_filter = ('completed', 'activity__category')
    search_fields = ('child__first_name', 'activity__title')
    ordering = ('-updated_at',)

@admin.register(DevelopmentMilestone)
class DevelopmentMilestoneAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'age_group', 'created_at')
    list_filter = ('category', 'age_group')
    search_fields = ('title', 'description')
    ordering = ('age_group', 'category', 'title')

@admin.register(MilestoneProgress)
class MilestoneProgressAdmin(admin.ModelAdmin):
    list_display = ('child', 'milestone', 'achieved', 'updated_at')
    list_filter = ('achieved', 'milestone__category')
    search_fields = ('child__first_name', 'milestone__title')
    ordering = ('-updated_at',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'child', 'notification_type', 'title', 'read', 'created_at')
    list_filter = ('notification_type', 'read', 'created_at')
    search_fields = ('user__username', 'child__first_name', 'title', 'message')
    ordering = ('-created_at',)
    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        queryset.update(read=True)
    mark_as_read.short_description = "Mark selected notifications as read"

    def mark_as_unread(self, request, queryset):
        queryset.update(read=False)
    mark_as_unread.short_description = "Mark selected notifications as unread"
