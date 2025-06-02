from django import forms
from django.utils.translation import gettext_lazy as _
from .models import (
    LearningActivity, 
    ActivityResource, 
    ActivityProgress, 
    DevelopmentMilestone, 
    MilestoneProgress,
    NotificationPreferences
)
from children.models import Child

class LearningActivityForm(forms.ModelForm):
    class Meta:
        model = LearningActivity
        fields = ['title', 'description', 'category', 'age_group', 'duration', 'materials_needed', 'learning_outcomes']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'materials_needed': forms.Textarea(attrs={'rows': 3}),
            'learning_outcomes': forms.Textarea(attrs={'rows': 3}),
        }
        help_texts = {
            'duration': _('Duration in minutes'),
            'materials_needed': _('List any materials needed for this activity'),
            'learning_outcomes': _('Describe what children will learn from this activity'),
        }

class ActivityResourceForm(forms.ModelForm):
    class Meta:
        model = ActivityResource
        fields = ['title', 'description', 'file']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }

class ActivityProgressForm(forms.ModelForm):
    class Meta:
        model = ActivityProgress
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class DevelopmentMilestoneForm(forms.ModelForm):
    class Meta:
        model = DevelopmentMilestone
        fields = ['title', 'description', 'category', 'age_group']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class MilestoneProgressForm(forms.ModelForm):
    class Meta:
        model = MilestoneProgress
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class NotificationPreferencesForm(forms.ModelForm):
    """Form for managing notification preferences"""

    class Meta:
        model = NotificationPreferences
        fields = [
            # Email preferences
            'email_enabled', 'email_frequency',
            'email_priority_threshold',
            
            # Notification type preferences
            'activity_completed_enabled', 'milestone_achieved_enabled',
            'new_activity_enabled', 'progress_update_enabled',
            'reminder_enabled', 'alert_enabled',
            
            # Sound preferences
            'sound_enabled', 'sound_type',
            
            # Browser notification preferences
            'browser_notifications_enabled', 'browser_notification_frequency',
            
            # Time-based preferences
            'quiet_hours_enabled', 'quiet_hours_start', 'quiet_hours_end',
        ]
        widgets = {
            'quiet_hours_start': forms.TimeInput(attrs={'type': 'time'}),
            'quiet_hours_end': forms.TimeInput(attrs={'type': 'time'}),
        }
        help_texts = {
            'email_priority_threshold': _('Only send emails for notifications with priority equal to or higher than this level'),
            'quiet_hours_enabled': _('Enable quiet hours to prevent notifications during specified times'),
            'quiet_hours_start': _('Start time for quiet hours'),
            'quiet_hours_end': _('End time for quiet hours'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Group related fields in fieldsets
        self.fieldsets = {
            'Email Preferences': {
                'fields': ['email_enabled', 'email_frequency', 'email_priority_threshold'],
                'description': 'Control how and when you receive email notifications'
            },
            'Notification Types': {
                'fields': [
                    'activity_completed_enabled', 'milestone_achieved_enabled',
                    'new_activity_enabled', 'progress_update_enabled',
                    'reminder_enabled', 'alert_enabled'
                ],
                'description': 'Select which types of notifications you want to receive'
            },
            'Sound Preferences': {
                'fields': ['sound_enabled', 'sound_type'],
                'description': 'Control sound notifications'
            },
            'Browser Notifications': {
                'fields': ['browser_notifications_enabled', 'browser_notification_frequency'],
                'description': 'Control browser notifications'
            },
            'Quiet Hours': {
                'fields': ['quiet_hours_enabled', 'quiet_hours_start', 'quiet_hours_end'],
                'description': 'Set times when you don\'t want to receive notifications'
            }
        }
        
        # Add fieldset classes to fields
        for fieldset_name, fieldset in self.fieldsets.items():
            for field_name in fieldset['fields']:
                self.fields[field_name].widget.attrs.update({
                    'class': f'fieldset-{fieldset_name.lower().replace(" ", "-")}'
                })

    def clean(self):
        cleaned_data = super().clean()
        
        # Validate quiet hours
        quiet_hours_enabled = cleaned_data.get('quiet_hours_enabled')
        quiet_hours_start = cleaned_data.get('quiet_hours_start')
        quiet_hours_end = cleaned_data.get('quiet_hours_end')
        
        if quiet_hours_enabled and (not quiet_hours_start or not quiet_hours_end):
            raise forms.ValidationError(
                _('You must specify both start and end times for quiet hours')
            )
        
        return cleaned_data
