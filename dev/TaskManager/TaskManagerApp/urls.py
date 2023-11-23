from django.urls import path
from .views import *

urlpatterns = [
    path('users/', UserList.as_view(), name='user_list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user_detail'),

    path('groups/', GroupList.as_view(), name='group_list'),
    path('groups/<int:pk>/', GroupDetail.as_view(), name='group_detail'),

    path('organizations/', OrganizationList.as_view(), name='organization_list'),
    path('organizations/<slug:slug>/', OrganizationDetail.as_view(), name='organization_detail'),

    path('userprofiles/', UserProfileList.as_view(), name='userprofile_list'),
    path('userprofiles/<int:pk>/', UserProfileDetail.as_view(), name='userprofile_detail'),

    path('organizations/<slug:organization>/projects/', ProjectList.as_view(), name='project_list'),
    path('projects/<slug:slug>/', ProjectDetail.as_view(), name='project_detail'),

    path('projects/<slug:project>/tasks/', TaskList.as_view(), name='task_list'),
    path('tasks/<slug:slug>/', TaskDetail.as_view(), name='task_detail'),

]
