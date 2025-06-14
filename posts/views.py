from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Q
from django.contrib.sessions.models import Session
from .models import Post, Comment, Announcement, CommunityPost, Notification
from django.contrib.auth.models import User
from users.models import Profile
from django.contrib import messages
from .forms import PostForm, AnnouncementForm, CommunityPostForm

class AnnouncementDetailView(LoginRequiredMixin, DetailView):
    model = Announcement
    template_name = 'posts/announcement_detail.html'
    context_object_name = 'announcement'
    
    def get_queryset(self):
        return Announcement.objects.filter(is_active=True)


class AnnouncementCreateView(LoginRequiredMixin, CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'posts/announcement_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user.profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('announcement-detail', kwargs={'pk': self.object.pk})

class CommunityPostListView(LoginRequiredMixin, ListView):
    model = CommunityPost
    template_name = 'posts/community_post_list.html'
    context_object_name = 'community_posts'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        return CommunityPost.objects.all()

def home_feed(request):
    """Combined feed view showing posts, announcements, and community posts"""
    # Get the latest posts, announcements, and community posts
    posts = Post.objects.all().order_by('-created_at')[:5]
    announcements = Announcement.objects.filter(is_active=True).order_by('-created_at')[:5]
    community_posts = CommunityPost.objects.all().order_by('-created_at')[:5]

    # Combine and sort all items by created_at
    feed_items = sorted(
        list(posts) + list(announcements) + list(community_posts),
        key=lambda x: x.created_at,
        reverse=True
    )[:10]  # Show top 10 items

    # Get active users (users with active sessions)
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_ids = []
    for session in active_sessions:
        data = session.get_decoded()
        user_id = data.get('_auth_user_id')
        if user_id:
            user_ids.append(user_id)
    
    active_users = User.objects.filter(id__in=user_ids).order_by('-last_login')[:10]
    
    context = {
        'feed_items': feed_items,
        'is_paginated': True,
        'page_obj': feed_items,
        'active_users': active_users
    }
    return render(request, 'posts/home.html', context)

@require_GET
def notifications_count(request):
    """Return count of unread notifications for the current user"""
    if not request.user.is_authenticated:
        return JsonResponse({'count': 0})
    
    count = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).count()
    
    return JsonResponse({'count': count})


class CommunityPostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = CommunityPost
    form_class = CommunityPostForm
    template_name = 'posts/community_post_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Set created_by before saving
        form.instance.created_by = self.request.user.profile
        # Save the form instance
        self.object = form.save()
        # Redirect to success URL
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('community-post-detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        # Check if user is a teacher
        return self.request.user.profile.user_type == 'teacher'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context data if needed
        return context

class CommunityPostDetailView(LoginRequiredMixin, DetailView):
    model = CommunityPost
    template_name = 'posts/community_post_detail.html'
    context_object_name = 'community_post'

    def get_queryset(self):
        return CommunityPost.objects.all()

class CommunityPostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CommunityPost
    form_class = CommunityPostForm
    template_name = 'posts/community_post_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user.profile
        return super().form_valid(form)

    def test_func(self):
        community_post = self.get_object()
        return community_post.created_by == self.request.user.profile

    def get_success_url(self):
        return reverse('community-post-detail', kwargs={'pk': self.object.pk})

class CommunityPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CommunityPost
    template_name = 'posts/community_post_confirm_delete.html'
    success_url = reverse_lazy('community-post-list')

    def test_func(self):
        community_post = self.get_object()
        return community_post.created_by == self.request.user.profile

class AnnouncementUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'posts/announcement_form.html'
    
    def test_func(self):
        announcement = self.get_object()
        return announcement.created_by == self.request.user.profile
    
    def get_queryset(self):
        return Announcement.objects.filter(is_active=True)


class AnnouncementDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Announcement
    template_name = 'posts/announcement_confirm_delete.html'
    success_url = reverse_lazy('home')
    
    def test_func(self):
        announcement = self.get_object()
        return announcement.created_by == self.request.user.profile
    
    def get_queryset(self):
        return Announcement.objects.filter(is_active=True)

# Home view to display all posts
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/home.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 5
    login_url = 'login'  # Redirect to login page if not authenticated
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Combine posts and announcements in the feed
        posts = Post.objects.all()
        announcements = Announcement.objects.filter(
            is_active=True,
            event_date__gte=timezone.now()
        ).order_by('event_date')
        
        # Combine and sort by created_at
        feed_items = sorted(
            list(posts) + list(announcements),
            key=lambda x: x.created_at if hasattr(x, 'created_at') else x.event_date,
            reverse=True
        )[:50]  # Limit to 50 items
        
        context['feed_items'] = feed_items
        
        # Get currently logged in users (users with active sessions)
        active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        logged_in_user_ids = []
        
        # Extract user IDs from session data
        for session in active_sessions:
            data = session.get_decoded()
            user_id = data.get('_auth_user_id')
            if user_id:
                logged_in_user_ids.append(int(user_id))
        
        # Get all users who are currently logged in
        active_profiles = Profile.objects.filter(user_id__in=logged_in_user_ids).order_by('-user__last_login')[:10]  # Top 10 logged in users
        
        # Mark all as online and add post count
        for profile in active_profiles:
            profile.is_online = True
            profile.post_count = Post.objects.filter(author=profile).count()
        
        context['active_profiles'] = active_profiles
        
        # Add unread notifications count for the current user
        if self.request.user.is_authenticated:
            context['unread_notifications'] = Notification.objects.filter(
                recipient=self.request.user,
                is_read=False
            ).count()
            
        return context

# User's posts view
class UserPostListView(ListView):
    model = Post
    template_name = 'posts/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        profile = get_object_or_404(Profile, user=user)
        return Post.objects.filter(author=profile).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        profile = get_object_or_404(Profile, user=user)
        context['user_profile'] = profile
        return context

# Post detail view
class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        return context

# Create post view
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'posts/post_form.html'
    form_class = PostForm
    
    def form_valid(self, form):
        # Save the form with commit=False to handle author and media
        post = form.save(commit=False)
        post.author = self.request.user.profile
        # Handle file upload
        if self.request.FILES.get('media'):
            post.media = self.request.FILES['media']
        post.save()
        messages.success(self.request, 'Your post has been created!')
        return redirect('home')
    
    def form_invalid(self, form):
        # If form is invalid
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{field}: {error}')
        return self.render_to_response(self.get_context_data(form=form))
    
    def post(self, request, *args, **kwargs):
        # Get the form
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

# Update post view
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'posts/post_form.html'
    fields = ['title', 'content', 'image']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Delete post view
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('home')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Add comment to post
@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            # Create the comment
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )
            
            # Create notification for post owner (if not the same as comment author)
            if post.author != request.user:
                Notification.objects.create(
                    recipient=post.author,
                    notification_type='comment',
                    actor=request.user,
                    post=post
                )
                
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Comment cannot be empty!')
    
    return redirect('post-detail', pk=pk)

# Like/unlike post
@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
        
        # Remove any existing like notification
        Notification.objects.filter(
            recipient=post.author,
            notification_type='like',
            actor=request.user,
            post=post
        ).delete()
    else:
        post.likes.add(request.user)
        liked = True
        
        # Create notification for post owner (if not the same as like author)
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                notification_type='like',
                actor=request.user,
                post=post
            )
    
    return JsonResponse({
        'liked': liked,
        'count': post.get_like_count()
    })

# Notifications view
@login_required
def notifications(request):
    # Get all notifications for the current user
    notifications_list = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    
    # Mark all as read if requested
    if request.GET.get('mark_all_read'):
        notifications_list.update(is_read=True)
        messages.success(request, 'All notifications marked as read.')
        return redirect('notifications')
    
    return render(request, 'posts/notifications.html', {'notifications': notifications_list})

# Mark notification as read
@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    
    # Redirect to the post that the notification is about
    return redirect('post-detail', pk=notification.post.pk)

# AJAX endpoint to mark notification as read
@login_required
def mark_notification_read_ajax(request, notification_id):
    if request.method == 'POST':
        notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)
