from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, GroupViewSet, OrganizationViewSet, UserProfileViewSet, ProjectViewSet, TaskViewSet

from django.urls import path
from .views import UserViewSet, GroupViewSet, OrganizationViewSet, UserProfileViewSet, ProjectViewSet, TaskViewSet

urlpatterns = [
    path('users/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    path('users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='user-detail'),

    path('groups/', GroupViewSet.as_view({'get': 'list', 'post': 'create'}), name='group-list'),
    path('groups/<int:pk>/', GroupViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='group-detail'),

    path('organizations/', OrganizationViewSet.as_view({'get': 'list', 'post': 'create'}), name='organization-list'),
    path('organizations/<int:pk>/', OrganizationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='organization-detail'),

    path('userprofiles/', UserProfileViewSet.as_view({'get': 'list', 'post': 'create'}), name='userprofile-list'),
    path('userprofiles/<int:pk>/', UserProfileViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='userprofile-detail'),

    path('projects/', ProjectViewSet.as_view({'get': 'list', 'post': 'create'}), name='project-list'),
    path('projects/<int:pk>/', ProjectViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='project-detail'),

    path('tasks/', TaskViewSet.as_view({'get': 'list', 'post': 'create'}), name='task-list'),
    path('tasks/<int:pk>/', TaskViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='task-detail'),
]
