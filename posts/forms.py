from django import forms
from .models import Post
import os
import logging

logger = logging.getLogger(__name__)

class PostForm(forms.ModelForm):
    image = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={
        'accept': 'image/*,video/*,.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx'
    }), max_length=500)

    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            try:
                logger.info(f"Processing file: {image.name}")
                # Check file size
                if image.size > 50 * 1024 * 1024:  # 50MB limit
                    raise forms.ValidationError('File size must be less than 50MB')
                
                # Check file type
                valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mov', '.avi', '.webm', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']
                extension = os.path.splitext(image.name)[1].lower()
                if extension not in valid_extensions:
                    raise forms.ValidationError(f'File type not supported. Please upload a file with one of these extensions: {", ".join(valid_extensions)}')
                
                # Set the upload_to path based on the file type
                if extension in ['.jpg', '.jpeg', '.png', '.gif']:
                    image.name = f'images/{image.name}'
                elif extension in ['.mp4', '.mov', '.avi', '.webm']:
                    image.name = f'videos/{image.name}'
                else:
                    image.name = f'documents/{image.name}'
                
                # Set the upload_to path in the form instance
                self.instance.image.name = f'post_media/{image.name}'
                
                logger.info(f"File processed successfully: {image.name}")
                return image
            except Exception as e:
                logger.error(f'Error processing file: {str(e)}')
                raise forms.ValidationError(f'Error processing file: {str(e)}')
        return image
