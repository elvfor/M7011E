from django.http import Http404
from .serializers import *
from .models import Project
from rest_framework import generics, authentication, permissions
from organization.models import Organization
from organization.views import IsOrgLeader, IsPartOfOrg
from rest_framework.permissions import IsAdminUser

from rest_framework import permissions


class SafePermissions(permissions.BasePermission):
    message = {'detail': 'You do not have permission to do this.'}

    def has_permission(self, request, view):
        if self.is_safe_method(request):
            return True
        else:
            return self.is_proj_leader(request, view)
        return False

    def is_safe_method(self, request):
        return request.method in permissions.SAFE_METHODS

    def is_proj_leader(self, request, view):
        group_name = "Project Leader"
        return request.user.groups.filter(name=group_name).exists()


class IsWorker(permissions.BasePermission):
    message = {'detail': 'You must be a worker to do this.'}

    def has_permission(self, request, view):
        group_name = "Worker"  # Set your group name here
        return request.user.groups.filter(name=group_name).exists()


class IsPartOfProj(permissions.BasePermission):
    message = {'detail': 'You must be part of this Project.'}

    def has_permission(self, request, view):
        project_slug = view.kwargs['slug']  # Assuming 'project' is the parameter name in your URL

        try:
            project = Project.objects.get(slug=project_slug)
        except Project.DoesNotExist:
            return Http404

        return request.user in project.users.all()


class IsProjLeader(permissions.BasePermission):
    message = {'detail': 'You must be a Project Leader to do this.'}

    def has_permission(self, request, view):
        group_name = "Project Leader"  # Set your group name here
        return request.user.groups.filter(name=group_name).exists()


class ProjectList(generics.ListCreateAPIView):
    """Manage Projects in entered Organization."""
    serializer_class = ProjectSerializer

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, (IsOrgLeader | IsWorker | IsProjLeader | IsAdminUser),
                          (IsPartOfOrg | IsAdminUser), (SafePermissions | IsAdminUser)]

    # def get_queryset(self):
    #    organization = Organization.objects.get(slug=self.kwargs['slug'])
    #    return Project.objects.filter(organization=organization)
    def get_queryset(self):
        organization = Organization.objects.get(slug=self.kwargs['slug'])

        if self.request.user.is_superuser:
            # Return all projects if the user is a superuser
            return Project.objects.all()
        if self.request.user.groups.filter(name='Organization Leader').exists():
            return Project.objects.filter(organization=organization)
        else:
            # Return projects for regular users
            return Project.objects.filter(users=self.request.user, organization=organization)

    def perform_create(self, serializer):
        organization = Organization.objects.get(slug=self.kwargs['slug'])
        serializer.save(organization=organization)


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    """Manage entered Project and view its Tasks."""
    serializer_class = ProjectSerializer
    lookup_field = 'slug'
    queryset = Project.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, (IsWorker | IsProjLeader | IsAdminUser),
                          (SafePermissions | IsAdminUser), (IsPartOfProj | IsAdminUser)]
