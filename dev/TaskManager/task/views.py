from .serializers import *
from .models import Task
from project.models import Project
from rest_framework import generics, viewsets, permissions
class TaskList(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    def get_queryset(self):
        #organization_slug = self.kwargs['organization']
        project_slug = self.kwargs['project']
        return Task.objects.filter(project__slug=project_slug)

    def perform_create(self, serializer):
        project = Project.objects.get(slug=self.kwargs['project'])
        serializer.save(project=project)

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    lookup_field = 'slug'
    queryset = Task.objects.all()