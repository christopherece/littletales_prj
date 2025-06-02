from django.contrib import admin
from .models import Child, LearningActivity

@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'age', 'date_of_birth', 'created_at')
    list_filter = ('date_of_birth', 'created_at')
    search_fields = ('first_name', 'last_name', 'user__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'first_name', 'last_name', 'date_of_birth', 'profile_picture', 'interests')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

@admin.register(LearningActivity)
class LearningActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'child', 'activity_type', 'get_completion_status', 'created_at')
    list_filter = ('activity_type', 'created_at')
    search_fields = ('title', 'child__first_name', 'child__last_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Activity Details', {
            'fields': ('child', 'title', 'description', 'activity_type', 'completed')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "child":
            kwargs["queryset"] = Child.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_completion_status(self, obj):
        try:
            return obj.completed
        except AttributeError:
            return False
    get_completion_status.boolean = True
    get_completion_status.short_description = 'Completed'
    get_completion_status.admin_order_field = 'completed'
