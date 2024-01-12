from django.urls import path

from .views import organizations_view, projects_view, organization_users_view

app_name = 'main'

urlpatterns = [
    path('organizations/', organizations_view, name='organizations_view'),
    path('projects/', projects_view, name='projects_view'),
    path('organization_users/', organization_users_view, name='organization_users_view'),
]