from django.http import HttpResponse
from .serializers import *
from .models import Task
from rest_framework import generics, viewsets, permissions
from django.shortcuts import get_object_or_404

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
