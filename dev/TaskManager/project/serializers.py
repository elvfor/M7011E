from django.contrib.auth.models import User, Group
from .models import Project
from rest_framework import serializers
from organization.models import Organization

from django.urls import reverse
class ProjectSerializer(serializers.HyperlinkedModelSerializer):

    organization_slug = serializers.SlugRelatedField(
        read_only=True,
        source='organization',
        slug_field='slug'
    )

    organization = serializers.HyperlinkedRelatedField(
        view_name='organization-detail',
        read_only=True,
        lookup_field='slug')

    users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Project
        fields = ('organization_slug', 'organization', 'id', 'name', 'users', 'slug')
        read_only_fields = ['organization', 'organization_slug', ]

    def validate_users(self, value):
        """
        Validate that users belong to the same organization as the project.
        """
        instance = self.instance
        project_organization = None

        if instance is not None:
            project_organization = instance.organization

        elif 'slug' in self.context['view'].kwargs:
            organization_slug = self.context['view'].kwargs['slug']
            try:
                project_organization = Organization.objects.get(slug=organization_slug)
            except Organization.DoesNotExist:
                raise serializers.ValidationError("Invalid organization provided in the URL.")

        # Perform organization validation for each user
        for user in value:
            if user not in project_organization.users.all():
                raise serializers.ValidationError(
                    f"User {user.username} does not belong to the project's organization."
                )

        return value