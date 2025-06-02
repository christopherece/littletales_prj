from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import LearningActivity, ActivityResource, ActivityProgress, DevelopmentMilestone, MilestoneProgress, Notification
from .forms import LearningActivityForm, ActivityResourceForm, ActivityProgressForm, DevelopmentMilestoneForm, MilestoneProgressForm
from children.models import Child
from django.contrib.auth import get_user_model
from .forms import NotificationPreferencesForm

@login_required
def activity_list(request):
    """View to list all learning activities"""
    activities = LearningActivity.objects.all().order_by('category', 'title')
    return render(request, 'early_learning/activity_list.html', {
        'activities': activities,
        'unreads': Notification.objects.filter(user=request.user).filter(read=False).count()
    })

@login_required
def activity_detail(request, pk):
    """View to show activity details and resources"""
    activity = get_object_or_404(LearningActivity, pk=pk)
    resources = ActivityResource.objects.filter(activity=activity)
    return render(request, 'early_learning/activity_detail.html', {
        'activity': activity,
        'resources': resources,
        'unreads': Notification.objects.filter(user=request.user).filter(read=False).count()
    })

@login_required
def add_activity_progress(request, activity_pk, child_pk):
    """View to record progress for a child on an activity"""
    activity = get_object_or_404(LearningActivity, pk=activity_pk)
    child = get_object_or_404(Child, pk=child_pk)
    
    try:
        progress = ActivityProgress.objects.get(child=child, activity=activity)
    except ActivityProgress.DoesNotExist:
        progress = ActivityProgress(child=child, activity=activity)
    
    if request.method == 'POST':
        form = ActivityProgressForm(request.POST, instance=progress)
        if form.is_valid():
            progress = form.save(commit=False)
            progress.completed = 'completed' in request.POST
            if progress.completed:
                progress.completion_date = timezone.now()
                # Create notification for activity completion
                Notification.objects.create(
                    user=request.user,
                    child=child,
                    notification_type='activity_completed',
                    title=f'Activity Completed: {activity.title}',
                    message=f'{child.first_name} has completed the activity "{activity.title}" in the {activity.get_category_display()} category.'
                )
            progress.save()
            messages.success(request, f'Progress for {child.first_name} updated successfully')
            return redirect('child_progress', child_pk=child.pk)
    else:
        form = ActivityProgressForm(instance=progress)
    
    return render(request, 'early_learning/add_activity_progress.html', {
        'form': form,
        'activity': activity,
        'child': child,
        'unreads': Notification.objects.filter(user=request.user).filter(read=False).count()
    })

@login_required
def milestone_list(request):
    """View to list all development milestones"""
    milestones = DevelopmentMilestone.objects.all().order_by('age_group', 'category', 'title')
    return render(request, 'early_learning/milestone_list.html', {
        'milestones': milestones,
        'unreads': Notification.objects.filter(user=request.user).filter(read=False).count()
    })

@login_required
def add_milestone_progress(request, milestone_pk, child_pk):
    """View to record progress for a child on a milestone"""
    milestone = get_object_or_404(DevelopmentMilestone, pk=milestone_pk)
    child = get_object_or_404(Child, pk=child_pk)
    
    try:
        progress = MilestoneProgress.objects.get(child=child, milestone=milestone)
    except MilestoneProgress.DoesNotExist:
        progress = MilestoneProgress(child=child, milestone=milestone)
    
    if request.method == 'POST':
        form = MilestoneProgressForm(request.POST, instance=progress)
        if form.is_valid():
            progress = form.save(commit=False)
            progress.achieved = 'achieved' in request.POST
            if progress.achieved:
                progress.achievement_date = timezone.now()
                # Create notification for milestone achievement
                Notification.objects.create(
                    user=request.user,
                    child=child,
                    notification_type='milestone_achieved',
                    title=f'Milestone Achieved: {milestone.title}',
                    message=f'{child.first_name} has achieved the milestone "{milestone.title}" in the {milestone.get_category_display()} category.'
                )
            progress.save()
            messages.success(request, f'Milestone progress for {child.first_name} updated successfully')
            return redirect('child_progress', child_pk=child.pk)
    else:
        form = MilestoneProgressForm(instance=progress)
    
    return render(request, 'early_learning/add_milestone_progress.html', {
        'form': form,
        'milestone': milestone,
        'child': child,
        'unreads': Notification.objects.filter(user=request.user).filter(read=False).count()
    })

@login_required
def child_progress(request, child_pk):
    """View to show all progress for a specific child"""
    child = get_object_or_404(Child, pk=child_pk)
    activity_progress = ActivityProgress.objects.filter(child=child).order_by('-updated_at')
    milestone_progress = MilestoneProgress.objects.filter(child=child).order_by('-updated_at')
    
    return render(request, 'early_learning/child_progress.html', {
        'child': child,
        'activity_progress': activity_progress,
        'milestone_progress': milestone_progress,
        'unreads': Notification.objects.filter(user=request.user).filter(read=False).count()
    })

@login_required
def notifications(request):
    """View to show all notifications for the user"""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'early_learning/notifications.html', {
        'notifications': notifications,
        'unreads': Notification.objects.filter(user=request.user).filter(read=False).count()
    })

@login_required
def mark_notification_read(request, notification_id):
    """Mark a notification as read"""
    notification = get_object_or_404(Notification, pk=notification_id, user=request.user)
    notification.mark_as_read()
    return redirect('notifications')

@login_required
def mark_all_read(request):
    """Mark all notifications as read"""
    Notification.objects.filter(user=request.user).update(read=True)
    return redirect('notifications')

@login_required
def search_activities(request):
    """View to search learning activities"""
    query = request.GET.get('q', '')
    activities = LearningActivity.objects.all()
    
    if query:
        activities = activities.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query) |
            Q(age_group__icontains=query)
        )
    
    return render(request, 'early_learning/activity_list.html', {
        'activities': activities,
        'query': query,
        'unreads': Notification.objects.filter(user=request.user).filter(read=False).count()
    })

@login_required
def notification_preferences(request):
    """View to manage notification preferences"""
    try:
        preferences = NotificationPreferences.objects.get(user=request.user)
    except NotificationPreferences.DoesNotExist:
        preferences = NotificationPreferences.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = NotificationPreferencesForm(request.POST, instance=preferences)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notification preferences updated successfully')
            return redirect('notification_preferences')
    else:
        form = NotificationPreferencesForm(instance=preferences)
    
    return render(request, 'early_learning/notification_preferences.html', {
        'form': form,
        'unreads': Notification.objects.filter(user=request.user).filter(read=False).count()
    })
