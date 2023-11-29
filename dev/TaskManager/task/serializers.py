from django.contrib.auth.models import User, Group
from .models import Task
from rest_framework import serializers

class TaskSerializer(serializers.HyperlinkedModelSerializer):

    project_slug = serializers.SlugRelatedField(
        read_only=True,
        source='project',
        slug_field='slug'
    )

    project = serializers.HyperlinkedRelatedField(
        view_name='project-detail',
        read_only=True,
        lookup_field='slug')

    users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'status', 'estimated_time', 'label',
                  'project', 'users', 'slug', 'project_slug']
        read_only_fields = ['project', 'project_slug', ]