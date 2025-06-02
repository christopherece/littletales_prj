from django import forms
from .models import Child, LearningActivity
from django.utils import timezone

class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['first_name', 'last_name', 'date_of_birth', 'profile_picture', 'interests']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'interests': forms.Textarea(attrs={'rows': 3}),
        }

class LearningActivityForm(forms.ModelForm):
    activity_type = forms.ChoiceField(
        choices=[
            ('academic', 'Academic Achievement'),
            ('creative', 'Creative Work'),
            ('physical', 'Physical Activity'),
            ('social', 'Social Interaction'),
            ('emotional', 'Emotional Development'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    
    class Meta:
        model = LearningActivity
        fields = ['title', 'description', 'activity_type']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
