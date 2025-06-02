from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from PIL import Image
from children.models import Child

# Create your models here.
class Post(models.Model):
    """Model for sharing children's activities and achievements"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.FileField(upload_to='posts/%(username)s/%(filename)s', blank=True, null=True)
    author = models.ForeignKey('users.Profile', on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField('users.Profile', related_name='liked_posts', blank=True)
    POST_TYPES = (
        ('activity', 'Learning Activity'),
        ('achievement', 'Achievement'),
        ('milestone', 'Developmental Milestone'),
        ('note', 'Progress Note')
    )
    post_type = models.CharField(max_length=20, choices=POST_TYPES, default='note')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
    
    def __str__(self):
        return f"{self.title} by {self.author.user.username} ({self.author.get_user_type_display()})"
    
    @property
    def image_url(self):
        """Return the profile image URL of the author"""
        if self.author and self.author.image:
            return self.author.image.url
        return '/static/img/user-default.png'
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    def get_like_count(self):
        return self.likes.count()
        
    def save(self, *args, **kwargs):
        # Ensure image path is set correctly
        if self.image:
            # The upload_to path is already handled by the FileField
            # We just need to make sure the directory exists
            try:
                import os
                from django.conf import settings
                dir_path = os.path.join(settings.MEDIA_ROOT, 'posts', self.author.username)
                os.makedirs(dir_path, exist_ok=True)
            except Exception as e:
                print(f"Error creating directory: {e}")
        super().save(*args, **kwargs)
        
        # Try to resize if it's an image file
        try:
            if self.image and hasattr(self.image, 'path'):
                file_name = self.image.name.lower()
                if file_name.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')):
                    img = Image.open(self.image.path)
                    if img.height > 800 or img.width > 800:
                        output_size = (800, 800)
                        img.thumbnail(output_size)
                        img.save(self.image.path)
        except Exception as e:
            print(f"Error processing post media: {e}")
            # Continue without failing


class Comment(models.Model):
    """Model for comments on posts"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('users.Profile', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']  # Changed to -created_at to show newest comments first
    
    def __str__(self):
        return f'Comment by {self.author.user.username} ({self.author.get_user_type_display()}) on {self.post.title}'


class Announcement(models.Model):
    """Model for school/center announcements"""
    ANNOUNCEMENT_TYPES = (
        ('general', 'General'),
        ('event', 'Event'),
        ('holiday', 'Holiday'),
        ('emergency', 'Emergency'),
    )
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    event_date = models.DateTimeField()
    announcement_type = models.CharField(max_length=20, choices=ANNOUNCEMENT_TYPES, default='general', null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('users.Profile', on_delete=models.CASCADE, related_name='announcements', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['event_date']
    
    @property
    def is_post(self):
        return False
    
    @property
    def is_announcement(self):
        return True
    
    def __str__(self):
        creator_username = self.created_by.user.username if self.created_by and self.created_by.user else 'Unknown'
        creator_type = self.created_by.get_user_type_display() if self.created_by else 'Unknown'
        return f"{self.title} by {creator_username} ({creator_type}) - {self.get_announcement_type_display()}"
    
    @property
    def image_url(self):
        """Return the profile image URL of the creator, or default image if none exists"""
        if self.created_by and self.created_by.image:
            return self.created_by.image.url
        return '/static/img/user-default.png'
    
    def get_absolute_url(self):
        """Get URL for viewing the announcement"""
        return reverse('announcement-detail', kwargs={'pk': self.pk})
    
    def clean(self):
        """Ensure only teachers can create announcements and validate dates"""
        if self.created_by and self.created_by.user_type != 'teacher':
            raise ValidationError('Only teachers can create announcements')
        
        if self.event_date < timezone.now():
            raise ValidationError('Event date must be in the future')
            
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        # Set is_active to True by default if not already set
        if not hasattr(self, 'is_active') or self.is_active is None:
            self.is_active = True
        self.clean()
        super().save(*args, **kwargs)
    
    @property
    def is_past_event(self):
        return self.event_date < timezone.now()


# Notification model for tracking interactions
class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
    )
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actions')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='notifications')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.actor.username} {self.notification_type}d your post "{self.post.title}"'
