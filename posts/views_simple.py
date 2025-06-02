from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
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
                post.author = request.user
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
        form = PostForm(initial={'author': request.user})
        return render(request, 'posts/post_form.html', {'form': form})
    
    return render(request, 'posts/post_form.html')
