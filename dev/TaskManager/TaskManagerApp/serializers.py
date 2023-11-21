from django.contrib.auth.models import User, Group
from .models import Organization, Task, Project, UserProfile
from rest_framework import serializers
from django.urls import reverse


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Organization
        fields = ['id', 'name', 'slug']


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['url', 'user', 'organization']

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    organization_slug = serializers.SlugRelatedField(
        read_only=True,
        source='organization',
        slug_field='slug'
    )

    organization = serializers.HyperlinkedIdentityField(
        view_name='organization_detail',
        read_only=True,
        lookup_field='slug')

    organization = serializers.CharField(source='get_organization_url', read_only=True)

    class Meta:
        model = Project
        fields = ('organization_slug', 'organization', 'id', 'name', 'users', 'slug')
        read_only_fields = ['organization', ]

    def get_organization(self, obj):
        request = self.context.get('request')
        if request:
            base_url = request.build_absolute_uri('/')  # Get the base URL
            organization_url = reverse('organization_detail', kwargs={'slug': obj.organization.slug})
            return f"{base_url.rstrip('/')}{organization_url}"
        return None

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    project = serializers.HyperlinkedIdentityField(view_name='organization_detail', lookup_field='slug')
    project_slug = serializers.SlugRelatedField(
        read_only=True,
        source='project',
        slug_field='slug'
    )

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'status', 'estimated_time', 'label', 'project', 'users', 'slug', 'project_slug']
