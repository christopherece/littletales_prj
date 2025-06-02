from django.urls import path
from . import views
from .views import (
    PostListView, PostDetailView, PostCreateView,
    PostUpdateView, PostDeleteView, UserPostListView,
    AnnouncementDetailView, AnnouncementCreateView,
    AnnouncementUpdateView, AnnouncementDeleteView,
    CommunityPostListView, CommunityPostDetailView, CommunityPostCreateView,
    CommunityPostUpdateView, CommunityPostDeleteView
)

urlpatterns = [
    path('', views.home_feed, name='home'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comment/', views.add_comment, name='add-comment'),
    path('post/<int:pk>/like/', views.like_post, name='like-post'),
    path('announcements/', AnnouncementCreateView.as_view(), name='announcements'),
    path('announcements/new/', AnnouncementCreateView.as_view(), name='create-announcement'),
    path('announcements/<int:pk>/', AnnouncementDetailView.as_view(), name='announcement-detail'),
    path('announcements/<int:pk>/update/', AnnouncementUpdateView.as_view(), name='announcement-update'),
    path('announcements/<int:pk>/delete/', AnnouncementDeleteView.as_view(), name='announcement-delete'),
    path('community-posts/', CommunityPostListView.as_view(), name='community-post-list'),
    path('community-post/new/', CommunityPostCreateView.as_view(), name='community-post-create'),
    path('community-post/<int:pk>/', CommunityPostDetailView.as_view(), name='community-post-detail'),
    path('community-post/<int:pk>/update/', CommunityPostUpdateView.as_view(), name='community-post-update'),
    path('community-post/<int:pk>/delete/', CommunityPostDeleteView.as_view(), name='community-post-delete'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark-notification-read'),
    path('notifications/<int:notification_id>/mark-read/', views.mark_notification_read_ajax, name='mark-notification-read-ajax'),
]
