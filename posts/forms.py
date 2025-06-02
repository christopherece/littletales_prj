from django import forms
from .models import Post, Announcement, CommunityPost
import os
import logging
from django.utils import timezone

logger = logging.getLogger(__name__)

class PostForm(forms.ModelForm):
    media = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={
        'accept': 'image/*,video/*,.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx'
    }), max_length=500)

    class Meta:
        model = Post
        fields = ['title', 'content', 'media']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }

class CommunityPostForm(forms.ModelForm):
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={
        'accept': 'image/*'
    }), max_length=500)

    class Meta:
        model = CommunityPost
        fields = ['title', 'content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False

    def clean(self):
        cleaned_data = super().clean()
        if self.user and self.user.is_authenticated:
            profile = self.user.profile
            if profile.user_type != 'teacher':
                raise forms.ValidationError('Only teachers can create community posts')
        return cleaned_data

    def clean_image(self):
        """Validate and process the uploaded image"""
        image = self.cleaned_data.get('image')
        if image:
            try:
                # Check file size (50MB limit)
                if image.size > 50 * 1024 * 1024:
                    raise forms.ValidationError('File size must be less than 50MB')
                
                # Check file type
                valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
                extension = os.path.splitext(image.name)[1].lower()
                if extension not in valid_extensions:
                    raise forms.ValidationError(f'File type not supported. Please upload a file with one of these extensions: {", ".join(valid_extensions)}')
            except Exception as e:
                raise forms.ValidationError(f'Error processing image: {str(e)}')
                
                # Set the upload_to path
                image.name = f'community_posts/{image.name}'
                
                return image
            except Exception as e:
                logger.error(f'Error processing file: {str(e)}')
                raise forms.ValidationError(f'Error processing file: {str(e)}')
        return image

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'event_date', 'announcement_type']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
            'event_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'announcement_type': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        self.created_by = kwargs.pop('created_by', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        event_date = cleaned_data.get('event_date')
        if event_date and event_date < timezone.now():
            raise forms.ValidationError('Event date must be in the future')
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.pk:  # Only set created_by for new instances
            instance.created_by = self.created_by
        if commit:
            instance.save()
        return instance
