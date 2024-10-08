from django.urls import path  # Use django.urls.path
from . import views

app_name = 'groups'

urlpatterns = [
    path('', views.ListGroups.as_view(), name='all'),
    path('new/', views.CreateGroup.as_view(), name='create'),
    path('posts/in/<slug>/', views.SingleGroup.as_view(), name='single'),  # Removed '-w' for clarity
    path('join/in/<slug>/', views.JoinGroup.as_view(), name='join'),
    path('leave/in/<slug>/', views.LeaveGroup.as_view(), name='leave'),
]
