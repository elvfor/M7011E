from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import *
#from TaskManagerApp import views

urlpatterns = [
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),

    path('groups/', GroupList.as_view(), name='group-list'),
    path('groups/<int:pk>/', GroupDetail.as_view(), name='group-detail'),

    path('organizations/', OrganizationList.as_view(), name='organization-list'),
    path('organizations/<slug:slug>/', OrganizationDetail.as_view(), name='organization-detail'),

    path('userprofiles/', UserProfileList.as_view(), name='userprofile-list'),
    path('userprofiles/<int:pk>/', UserProfileDetail.as_view(), name='userprofile-detail'),

    path('projects/', ProjectList.as_view(), name='project-list'),
    path('projects/<int:pk>/', ProjectDetail.as_view(), name='project-detail'),

    path('tasks/', TaskList.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetail.as_view(), name='task-detail'),
]
