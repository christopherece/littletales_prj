from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Child(models.Model):
    """Model for child profiles"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='children')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)
    date_of_birth = models.DateField()
    profile_picture = models.ImageField(upload_to='children/profiles/', blank=True, null=True)
    interests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['first_name', 'last_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        """Calculate child's age"""
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
    
    @property
    def profile_picture_url(self):
        """Get URL for profile picture with default if none exists"""
        try:
            if self.profile_picture and hasattr(self.profile_picture, 'url'):
                return self.profile_picture.url
        except Exception:
            pass
        return '/static/img/default-child.png'
    
    def get_absolute_url(self):
        return reverse('child-detail', kwargs={'pk': self.pk})


class LearningActivity(models.Model):
    """Model for learning activities/achievements"""
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=200)
    description = models.TextField()
    activity_type = models.CharField(max_length=50, choices=[
        ('academic', 'Academic Achievement'),
        ('creative', 'Creative Work'),
        ('physical', 'Physical Activity'),
        ('social', 'Social Development'),
        ('emotional', 'Emotional Development')
    ])
    media = models.FileField(upload_to='children/activities/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.child.first_name}"
    
    @property
    def media_url(self):
        """Get URL for media with default if none exists"""
        try:
            if self.media and hasattr(self.media, 'url'):
                return self.media.url
        except Exception:
            pass
        return '/static/img/default-activity.png'


class LearningGoal(models.Model):
    """Model for learning goals set by parents/teachers"""
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=200)
    description = models.TextField()
    target_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.child.first_name}"


class ProgressNote(models.Model):
    """Model for progress notes"""
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='progress_notes')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='notes')
    content = models.TextField()
    media = models.FileField(upload_to='children/notes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Note for {self.child.first_name} - {self.created_at.date()}"
    
    @property
    def media_url(self):
        """Get URL for media with default if none exists"""
        try:
            if self.media and hasattr(self.media, 'url'):
                return self.media.url
        except Exception:
            pass
        return '/static/img/default-note.png'
