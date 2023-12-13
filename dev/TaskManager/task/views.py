from django.http import Http404

from .serializers import *
from .models import Task
from project.models import Project
from project.views import IsWorker, IsProjLeader, IsPartOfProj
from rest_framework import generics, authentication, permissions
from rest_framework.permissions import IsAdminUser


class IsUserInProj(permissions.BasePermission):
    message = {'detail': 'Can not view task for a project you are not in.'}

    def has_permission(self, request, view):
        task_slug = view.kwargs['slug']
        try:
            task = Task.objects.get(slug=task_slug)
            project = task.project
        except Task.DoesNotExist:
            raise Http404

        return request.user in project.users.all()

class IsUserInProj_project(permissions.BasePermission):
    message = {'detail': 'Can not Manage Tasks for Project you are not in.'}

    def has_permission(self, request, view):
        project_slug = view.kwargs['slug']
        try:
            project = Project.objects.get(slug=project_slug)
        except Project.NotExist:
            raise Http404

        return request.user in project.users.all()

class TaskList(generics.ListCreateAPIView):
    """Manage entered Project Tasks."""
    serializer_class = TaskSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, (IsWorker | IsProjLeader | IsAdminUser), (IsUserInProj_project | IsAdminUser)]

    def get_queryset(self):
        project = Project.objects.get(slug=self.kwargs['slug'])
        return Task.objects.filter(project=project)

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        project = Project.objects.get(slug=self.kwargs['slug'])
        serializer.save(project=project)

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    """Manage Tasks."""
    serializer_class = TaskSerializer
    lookup_field = 'slug'
    queryset = Task.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, (IsWorker | IsProjLeader | IsAdminUser), (IsUserInProj | IsAdminUser)]
