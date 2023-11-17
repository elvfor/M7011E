from django.contrib.auth.models import User, Group
from .models import Organization, Task, Project, UserProfile
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='organization-detail', lookup_field='slug')
    #organization_slug = serializers.SlugRelatedField(read_only=True, slug_field='slug')

    class Meta:
        model = Organization
        fields = ['url', 'id', 'name', 'slug']


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['url', 'user', 'organization']

class ProjectSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='project-detail', lookup_field='slug')

    class Meta:
        model = Project
        fields = ['url', 'id', 'name', 'users', 'slug']

class TaskSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='task-detail', lookup_field='slug')

    class Meta:
        model = Task
        fields = ['url', 'id', 'name', 'description', 'status', 'estimated_time', 'label', 'project', 'users', 'slug']
