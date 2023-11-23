from django.http import HttpResponse
from .serializers import *
from .models import Organization, Project, Task, User, UserProfile
from rest_framework import generics, viewsets, permissions
from django.shortcuts import get_object_or_404


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = [permissions.IsAuthenticated]

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer


class GroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class OrganizationList(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class OrganizationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    lookup_field = 'slug'

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

