from django.http import HttpResponse
from .serializers import *
from .models import Project
from rest_framework import generics, viewsets, permissions
from organization.models import Organization
from django.shortcuts import get_object_or_404
class ProjectList(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        organization_slug = self.kwargs['organization']
        return Project.objects.filter(organization__slug=organization_slug)

    def perform_create(self, serializer):
        organization = Organization.objects.get(slug=self.kwargs['organization'])
        serializer.save(organization=organization)

class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    lookup_field = 'slug'
    queryset = Project.objects.all()