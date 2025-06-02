from django.urls import path
from . import views

app_name = 'early_learning'

urlpatterns = [
    # Activity URLs
    path('activities/', views.activity_list, name='activity_list'),
    path('activities/<int:pk>/', views.activity_detail, name='activity_detail'),
    path('activities/<int:activity_pk>/child/<int:child_pk>/progress/', 
         views.add_activity_progress, name='add_activity_progress'),
    path('activities/search/', views.search_activities, name='search_activities'),
    # Milestone URLs
    path('milestones/', views.milestone_list, name='milestone_list'),
    path('milestones/<int:milestone_pk>/child/<int:child_pk>/progress/', 
         views.add_milestone_progress, name='add_milestone_progress'),
    # Child Progress URLs
    path('child/<int:child_pk>/progress/', views.child_progress, name='child_progress'),
    # Notification URLs
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_read, name='mark_all_read'),
    path('notification-preferences/', views.notification_preferences, name='notification_preferences'),
]
