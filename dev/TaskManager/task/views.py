from .serializers import *
from .models import Task
from project.models import Project
#from rest_framework import generics, viewsets, permissions
from rest_framework import generics, viewsets, authentication, permissions

class IsWorker(permissions.BasePermission):
    message = {'detail': 'You must be a worker to do this.'}

    def has_permission(self, request, view):
        group_name = "Worker"  # Set your group name here
        return request.user.groups.filter(name=group_name).exists()


class TaskList(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, (IsWorker | IsProjLeader | IsOrgLeader)]

    def get_queryset(self):
        #organization_slug = self.kwargs['organization']
        project_slug = self.kwargs['project']
        return Task.objects.filter(project__slug=project_slug)

    def perform_create(self, serializer):
        project = Project.objects.get(slug=self.kwargs['project'])
        serializer.save(project=project)

    def get_queryset(self):
        worker = self.request.user
        return worker.tasks.all()


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    lookup_field = 'slug'
    queryset = Task.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, (IsWorker | IsProjLeader | IsOrgLeader)]



