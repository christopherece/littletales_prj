from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Child, LearningActivity
from early_learning.models import Notification
from posts.models import CommunityPost
from .forms import ChildForm, LearningActivityForm

@login_required
def child_dashboard(request):
    """Main dashboard showing all children and recent activities"""
    children = Child.objects.filter(user=request.user)
    recent_activities = LearningActivity.objects.filter(
        child__user=request.user
    ).order_by('-created_at')[:5]
    
    unread_notifications = Notification.objects.filter(
        user=request.user,
        read=False
    ).order_by('-created_at')
    
    # Get recent community posts
    recent_community_posts = CommunityPost.objects.all().order_by('-created_at')[:5]
    
    context = {
        'children': children,
        'recent_activities': recent_activities,
        'unread_notifications': unread_notifications,
        'recent_community_posts': recent_community_posts,
    }
    return render(request, 'children/dashboard.html', context)

@login_required
def child_detail(request, pk):
    """Detail view for a specific child"""
    child = get_object_or_404(Child, pk=pk, user=request.user)
    activities = LearningActivity.objects.filter(child=child).order_by('-created_at')
    
    if request.method == 'POST':
        form = LearningActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.child = child
            activity.save()
            messages.success(request, 'Activity added successfully!')
            return redirect('child-detail', pk=pk)
    else:
        form = LearningActivityForm()
    
    context = {
        'child': child,
        'activities': activities,
        'form': form,
    }
    return render(request, 'children/child_detail.html', context)

@login_required
def add_child(request):
    """Add a new child profile"""
    if request.method == 'POST':
        form = ChildForm(request.POST, request.FILES)
        if form.is_valid():
            child = form.save(commit=False)
            child.user = request.user
            child.save()
            messages.success(request, 'Child added successfully!')
            return redirect('children:dashboard')
    else:
        form = ChildForm()
    
    return render(request, 'children/add_child.html', {'form': form})

@login_required
def edit_child(request, pk):
    """Edit an existing child profile"""
    child = get_object_or_404(Child, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = ChildForm(request.POST, request.FILES, instance=child)
        if form.is_valid():
            form.save()
            messages.success(request, 'Child profile updated successfully!')
            return redirect('child-detail', pk=pk)
    else:
        form = ChildForm(instance=child)
    
    return render(request, 'children/edit_child.html', {'form': form})

@login_required
def delete_child(request, pk):
    """Delete a child profile"""
    child = get_object_or_404(Child, pk=pk, user=request.user)
    if request.method == 'POST':
        child.delete()
        messages.success(request, 'Child profile deleted successfully!')
        return redirect('children:dashboard')
    
    return render(request, 'children/delete_child.html', {'child': child})

@login_required
def mark_notification_read(request, pk):
    """Mark a notification as read"""
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.mark_as_read()
    return redirect('child-dashboard')
