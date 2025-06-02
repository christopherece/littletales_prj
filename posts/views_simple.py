from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post, Announcement
from .forms import PostForm, AnnouncementForm
from users.models import Profile
import logging

logger = logging.getLogger(__name__)

@login_required
def create_post(request):
    if request.method == 'POST':
        logger.info(f"Request method: POST\nRequest files: {request.FILES}\nRequest POST data: {request.POST}")
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            logger.info("Form is valid")
            try:
                post = form.save(commit=False)
                post.author = request.user.profile
                post.save()
                logger.info(f"Post created: {post}")
                logger.info(f"Image field: {post.image}")
                messages.success(request, 'Your post has been created!')
                return redirect('home')
            except Exception as e:
                logger.error(f"Error saving post: {str(e)}")
                messages.error(request, f'Error saving post: {str(e)}')
                return render(request, 'posts/post_form.html', {'form': form})
            except Exception as e:
                logger.error(f"Error saving post: {str(e)}")
                messages.error(request, f'Error saving post: {str(e)}')
                return render(request, 'posts/post_form.html', {'form': form})
        else:
            logger.error(f"Form errors: {form.errors}")
            messages.error(request, 'Error creating post: ' + str(form.errors))
            return render(request, 'posts/post_form.html', {'form': form})
    else:
        # Create form with initial author
        form = PostForm(initial={'author': request.user.profile})
        return render(request, 'posts/post_form.html', {'form': form})
    
    return render(request, 'posts/post_form.html')

@login_required
def create_announcement(request):
    """View for creating announcements - only accessible to teachers"""
    if request.user.profile.user_type != 'teacher':
        messages.error(request, 'Only teachers can create announcements')
        return redirect('home')
    
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, created_by=request.user.profile)
        if form.is_valid():
            try:
                announcement = form.save()
                messages.success(request, 'Announcement has been created!')
                return redirect('announcements')
            except Exception as e:
                messages.error(request, f'Error saving announcement: {str(e)}')
                return render(request, 'posts/announcement_form.html', {'form': form})
    else:
        form = AnnouncementForm(created_by=request.user.profile)
    
    return render(request, 'posts/announcement_form.html', {'form': form})

@login_required
def announcements(request):
    """View to display all announcements"""
    announcements = Announcement.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'posts/announcements.html', {'announcements': announcements})
