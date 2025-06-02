from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class SiteConfig(models.Model):
    # Site Branding
    logo = models.ImageField(
        upload_to='site_config/', 
        null=True, 
        blank=True,
        help_text='Upload the site logo (30x30px recommended)'
    )
    logo_name = models.CharField(
        max_length=50, 
        default='LittleTales',
        help_text='Name of your site'
    )
    favicon = models.ImageField(
        upload_to='site_config/', 
        null=True, 
        blank=True,
        help_text='Upload a favicon (16x16px recommended)'
    )
    
    # Welcome Page Content
    welcome_title = models.CharField(
        max_length=100, 
        default='Welcome to LittleTales',
        help_text='Main welcome page title'
    )
    welcome_subtitle = models.CharField(
        max_length=200, 
        default='A place for sharing children\'s learning journeys',
        help_text='Welcome page subtitle text'
    )
    
    sign_in_text = models.CharField(
        max_length=200, 
        default='Already have an account? Sign in to share and track your child\'s progress.',
        help_text='Text for the sign in section'
    )
    register_text = models.CharField(
        max_length=200, 
        default='New here? Join our community today to document your child\'s learning journey.',
        help_text='Text for the register section'
    )
    
    connect_heading = models.CharField(
        max_length=50, 
        default='Track Progress',
        help_text='Heading for the progress tracking feature'
    )
    connect_description = models.TextField(
        default='Monitor your child\'s development and achievements in real-time.',
        help_text='Description for the progress tracking feature'
    )
    
    share_heading = models.CharField(
        max_length=50, 
        default='Share Moments',
        help_text='Heading for the sharing feature'
    )
    share_description = models.TextField(
        default='Capture and share your child\'s learning moments with family and teachers.',
        help_text='Description for the sharing feature'
    )
    
    learn_heading = models.CharField(
        max_length=50, 
        default='Development',
        help_text='Heading for the development feature'
    )
    learn_description = models.TextField(
        default='Track academic, social, and emotional development milestones.',
        help_text='Description for the development feature'
    )
    
    def __str__(self):
        return self.logo_name
    
    @classmethod
    def get_default_content(cls):
        """Get or create default welcome content"""
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls.objects.create(
                logo_name='LittleTales',
                welcome_title='Welcome to LittleTales',
                welcome_subtitle='A place for sharing children\'s learning journeys',
                sign_in_text='Already have an account? Sign in to share and track your child\'s progress.',
                register_text='New here? Join our community today to document your child\'s learning journey.',
                connect_heading='Track Progress',
                connect_description='Monitor your child\'s development and achievements in real-time.',
                share_heading='Share Moments',
                share_description='Capture and share your child\'s learning moments with family and teachers.',
                learn_heading='Development',
                learn_description='Track academic, social, and emotional development milestones.'
            )
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if self.pk is None:
            try:
                existing = SiteConfig.objects.get()
                self.pk = existing.pk
            except SiteConfig.DoesNotExist:
                pass
        super().save(*args, **kwargs)
