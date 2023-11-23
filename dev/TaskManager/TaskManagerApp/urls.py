from django.urls import path
from .views import *

urlpatterns = [
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),

    path('groups/', GroupList.as_view(), name='group-list'),
    path('groups/<int:pk>/', GroupDetail.as_view(), name='group-detail'),

    path('organizations/', OrganizationList.as_view(), name='organization-list'),
    path('organizations/<slug:slug>/', OrganizationDetail.as_view(), name='organization-detail'),

    path('userprofiles/', UserProfileList.as_view(), name='userprofile-list'),
    path('userprofiles/<int:pk>/', UserProfileDetail.as_view(), name='userprofile-detail'),

    path('organizations/<slug:organization>/projects/', ProjectList.as_view(), name='project-list'),
    path('projects/<slug:slug>/', ProjectDetail.as_view(), name='project-detail'),

    path('projects/<slug:project>/tasks/', TaskList.as_view(), name='task-list'),
    path('tasks/<slug:slug>/', TaskDetail.as_view(), name='task-detail'),

]
