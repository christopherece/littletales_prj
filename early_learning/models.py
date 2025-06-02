from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from children.models import Child

# Early Learning Activity Categories
ACTIVITY_CATEGORIES = (
    ('language', 'Language Development'),
    ('math', 'Mathematics'),
    ('science', 'Science'),
    ('social', 'Social Studies'),
    ('physical', 'Physical Development'),
    ('creative', 'Creative Arts'),
    ('emotional', 'Emotional Development'),
)

# Age Groups
AGE_GROUPS = (
    ('0-2', '0-2 years'),
    ('3-5', '3-5 years'),
    ('6-8', '6-8 years'),
    ('9-12', '9-12 years'),
)

# Notification Types
NOTIFICATION_TYPES = (
    ('activity_completed', 'Activity Completed'),
    ('milestone_achieved', 'Milestone Achieved'),
    ('new_activity', 'New Activity Available'),
    ('progress_update', 'Progress Update'),
    ('reminder', 'Reminder'),
    ('alert', 'Alert'),
)

# Notification Categories
NOTIFICATION_CATEGORIES = (
    ('learning', 'Learning'),
    ('development', 'Development'),
    ('achievement', 'Achievement'),
    ('system', 'System'),
)

# Notification Priority Levels
NOTIFICATION_PRIORITIES = (
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
    ('critical', 'Critical'),
)

# Notification Templates
NOTIFICATION_TEMPLATES = {
    'activity_completed': 'Your child has completed the activity: {activity_title}',
    'milestone_achieved': 'Your child has achieved the milestone: {milestone_title}',
    'new_activity': 'New activity available: {activity_title}',
    'progress_update': 'Progress update for {child_name}: {message}',
    'reminder': 'Reminder: {message}',
    'alert': 'Important Alert: {message}',
}

class Notification(models.Model):
    """Model for user notifications"""
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='early_learning_notifications')
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='early_learning_notifications', null=True, blank=True)
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    category = models.CharField(max_length=50, choices=NOTIFICATION_CATEGORIES, default='learning')
    priority = models.CharField(max_length=20, choices=NOTIFICATION_PRIORITIES, default='medium')
    title = models.CharField(max_length=200)
    message = models.TextField()
    email_sent = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.title} - {self.get_notification_type_display()}"

    def mark_as_read(self):
        self.read = True
        self.save()

    def mark_as_unread(self):
        self.read = False
        self.save()

    def send_email_notification(self):
        """Send email notification if not already sent"""
        if not self.email_sent and self.user.email:
            # Get user's notification preferences
            preferences = NotificationPreferences.objects.filter(user=self.user).first()
            
            # If no preferences exist, create default preferences
            if not preferences:
                preferences = NotificationPreferences.objects.create(user=self.user)
            
            # Check if email should be sent based on preferences
            if preferences.should_send_email(self):
                from django.core.mail import send_mail
                from django.template.loader import render_to_string
                from django.utils import timezone
                
                # Get the template for this notification type
                template = NOTIFICATION_TEMPLATES.get(self.notification_type, self.message)
                
                # Check quiet hours
                if preferences.quiet_hours_enabled:
                    current_time = timezone.now().time()
                    if preferences.quiet_hours_start <= preferences.quiet_hours_end:
                        if preferences.quiet_hours_start <= current_time <= preferences.quiet_hours_end:
                            return  # Don't send during quiet hours
                    else:  # Quiet hours span midnight
                        if not (preferences.quiet_hours_end <= current_time <= preferences.quiet_hours_start):
                            return
                
                # Render the email template
                html_message = render_to_string('early_learning/email_notification.html', {
                    'notification': self,
                    'template': template,
                    'child': self.child,
                })
                
                send_mail(
                    subject=f"{self.get_priority_display()} - {self.title}",
                    message=self.message,
                    from_email='notifications@littletales.com',
                    recipient_list=[self.user.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                self.email_sent = True
                self.save()

class LearningActivity(models.Model):
    """Model for educational activities"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=ACTIVITY_CATEGORIES)
    age_group = models.CharField(max_length=10, choices=AGE_GROUPS)
    duration = models.IntegerField(help_text='Duration in minutes')
    materials_needed = models.TextField(blank=True)
    learning_outcomes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'title']
    
    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

class ActivityResource(models.Model):
    """Model for educational resources"""
    activity = models.ForeignKey(LearningActivity, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='early_learning/resources/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class ActivityProgress(models.Model):
    """Model to track child's progress through activities"""
    child = models.ForeignKey('children.Child', on_delete=models.CASCADE, related_name='activity_progress')
    activity = models.ForeignKey(LearningActivity, on_delete=models.CASCADE, related_name='progress')
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['child', 'activity']
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.child.first_name} - {self.activity.title}"

class DevelopmentMilestone(models.Model):
    """Model for tracking developmental milestones"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    age_group = models.CharField(max_length=10, choices=AGE_GROUPS)
    category = models.CharField(max_length=50, choices=ACTIVITY_CATEGORIES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['age_group', 'category', 'title']
    
    def __str__(self):
        return f"{self.title} ({self.get_age_group_display()})"

class MilestoneProgress(models.Model):
    """Model to track child's progress through milestones"""
    child = models.ForeignKey('children.Child', on_delete=models.CASCADE, related_name='milestone_progress')
    milestone = models.ForeignKey(DevelopmentMilestone, on_delete=models.CASCADE, related_name='progress')
    achieved = models.BooleanField(default=False)
    achievement_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['child', 'milestone']
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.child.first_name} - {self.milestone.title}"

class NotificationPreferences(models.Model):
    """Model for user notification preferences"""
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='notification_preferences')
    
    # Email preferences
    email_enabled = models.BooleanField(default=True)
    email_frequency = models.CharField(max_length=20, choices=[
        ('immediate', 'Immediate'),
        ('daily', 'Daily Summary'),
        ('weekly', 'Weekly Summary'),
        ('never', 'Never')
    ], default='immediate')
    
    # Notification type preferences
    activity_completed_enabled = models.BooleanField(default=True)
    milestone_achieved_enabled = models.BooleanField(default=True)
    new_activity_enabled = models.BooleanField(default=True)
    progress_update_enabled = models.BooleanField(default=True)
    reminder_enabled = models.BooleanField(default=True)
    alert_enabled = models.BooleanField(default=True)
    
    # Priority threshold for email notifications
    email_priority_threshold = models.CharField(max_length=20, choices=NOTIFICATION_PRIORITIES, default='medium')
    
    # Sound preferences
    sound_enabled = models.BooleanField(default=True)
    sound_type = models.CharField(max_length=20, choices=[
        ('soft', 'Soft'),
        ('medium', 'Medium'),
        ('loud', 'Loud'),
        ('custom', 'Custom')
    ], default='medium')
    
    # Browser notification preferences
    browser_notifications_enabled = models.BooleanField(default=True)
    browser_notification_frequency = models.CharField(max_length=20, choices=[
        ('immediate', 'Immediate'),
        ('hourly', 'Hourly'),
        ('daily', 'Daily')
    ], default='immediate')
    
    # Time-based preferences
    quiet_hours_enabled = models.BooleanField(default=False)
    quiet_hours_start = models.TimeField(null=True, blank=True)
    quiet_hours_end = models.TimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Notification Preferences'
        verbose_name_plural = 'Notification Preferences'
    
    def __str__(self):
        return f"Preferences for {self.user.username}"
    
    def should_send_email(self, notification):
        """Determine if an email should be sent based on preferences"""
        if not self.email_enabled:
            return False
            
        if notification.priority < self.email_priority_threshold:
            return False
            
        if notification.notification_type == 'activity_completed' and not self.activity_completed_enabled:
            return False
        if notification.notification_type == 'milestone_achieved' and not self.milestone_achieved_enabled:
            return False
        if notification.notification_type == 'new_activity' and not self.new_activity_enabled:
            return False
        if notification.notification_type == 'progress_update' and not self.progress_update_enabled:
            return False
        if notification.notification_type == 'reminder' and not self.reminder_enabled:
            return False
        if notification.notification_type == 'alert' and not self.alert_enabled:
            return False
            
        return True
