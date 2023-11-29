from django.http import HttpResponse
from .serializers import *
from .models import Project
from rest_framework import generics, authentication, permissions
from organization.models import Organization
from organization.views import IsOrgLeader, IsPartOfOrg
#from task.views import isWorker
from django.shortcuts import get_object_or_404
class IsPartOfProj(permissions.BasePermission):
    sage = {'detail': 'You must be part of this Project.'}

    def has_permission(self, request, view):
        project_slug = view.kwargs['project']  # Assuming 'project' is the parameter name in your URL

        try:
            project = Project.objects.get(slug=project_slug)
        except Project.DoesNotExist:
            return False

        return request.user in project.members.all()
class IsProjLeader(permissions.BasePermission):
    message = {'detail': 'You must be a Project Leader to do this.'}

    def has_permission(self, request, view):
        group_name = "Project_Leader"  # Set your group name here
        return request.user.groups.filter(name=group_name).exists()

class ProjectList(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOrgLeader, IsPartOfOrg]
    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(users=user)

    def perform_create(self, serializer):
        organization = Organization.objects.get(slug=self.kwargs['organization'])
        serializer.save(organization=organization)

class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    lookup_field = 'slug'
    queryset = Project.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, (IsProjLeader | IsOrgLeader), IsPartOfOrg]
    #permission_classes = [permissions.IsAuthenticated, (IsProjLeader | IsOrgLeader | IsWorker)]