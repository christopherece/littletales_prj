from django.urls import path
from . import views

app_name = 'children'

urlpatterns = [
    path('dashboard/', views.child_dashboard, name='dashboard'),
    path('child/add/', views.add_child, name='add-child'),
    path('child/<int:pk>/', views.child_detail, name='child-detail'),
    path('child/<int:pk>/edit/', views.edit_child, name='edit'),
    path('child/<int:pk>/delete/', views.delete_child, name='delete'),
    path('notification/<int:pk>/read/', views.mark_notification_read, name='mark-read'),
]
