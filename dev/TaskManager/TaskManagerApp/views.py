from django.http import HttpResponse
from .serializers import *
from .models import *
from rest_framework import generics, viewsets, permissions


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = [permissions.IsAuthenticated]

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = [permissions.IsAuthenticated]

class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    #permission_classes = [permissions.IsAuthenticated]


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    #permission_classes = [permissions.IsAuthenticated]

class GroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    #permission_classes = [permissions.IsAuthenticated]


class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    #permission_classes = [permissions.IsAuthenticated]


class OrganizationList(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    #permission_classes = [permissions.IsAuthenticated]

class OrganizationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    lookup_field = 'slug'
    # permission_classes = [permissions.IsAuthenticated]


class ProjectList(generics.ListCreateAPIView):
    #queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        organization = self.kwargs['organization']
        return Project.objects.filter(organization__slug=organization)

    def perform_create(self, serializer):
        organization = Organization.objects.get(slug=self.kwargs['organization'])
        serializer.save(organization=organization)

class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    #queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'slug'
    #permission_classes = [permissions.IsAuthenticated]

class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    #permission_classes = [permissions.IsAuthenticated]

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'slug'
    #permission_classes = [permissions.IsAuthenticated]