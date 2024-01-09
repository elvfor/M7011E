from django.contrib.auth.models import User, Group
from .models import Task
from rest_framework import serializers
from project.models import Project



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
        fields = ('id', 'name', 'description', 'status', 'estimated_time', 'label',
                  'project', 'users', 'slug', 'project_slug')
        read_only_fields = ['project', 'project_slug']

    def validate_users(self, value):
        """
        Validate that users are in the project as the task.
        """
        instance = self.instance
        task_project = None

        if instance is not None:
            task_project = instance.project

        elif 'slug' in self.context['view'].kwargs:
            project_slug = self.context['view'].kwargs['slug']
            try:
                task_project = Project.objects.get(slug=project_slug)
            except Project.DoesNotExist:
                raise serializers.ValidationError("Invalid Project provided in the URL.")

        for user in value:
            if user not in task_project.users.all():
                raise serializers.ValidationError(
                    f"User {user.username} is not part of the Project Task is in."
                )

        return value