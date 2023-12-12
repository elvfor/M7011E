from django.contrib.auth.models import User, Group
from .models import Project
from rest_framework import serializers
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
        if self.instance is not None:
            project_organization = self.instance.organization
            for user in value:
                if user.organization != project_organization:
                    raise serializers.ValidationError(
                        f"User {user.username} does not belong to the project's organization."
                    )
        return value
