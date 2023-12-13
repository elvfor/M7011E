from django.test import TestCase

# Create your tests here.

from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Task
from project.models import Project
from organization.models import Organization

class TaskDetailTest(APITestCase):
    """Tests for TaskDetail view."""

    def setUp(self):
        self.client_worker = APIClient()

        # Create users
        self.user_worker = User.objects.create_user(username='worker', password='testpass123')
        self.user_worker2 = User.objects.create_user(username='worker2', password='testpass123')
        self.user_proj_leader = User.objects.create_user(username='proj_leader', password='testpass123')
        self.user_org_leader = User.objects.create_user(username='org_leader', password='testpass123')

        # Create groups
        self.worker_group = Group.objects.create(name='Worker')
        self.proj_leader_group = Group.objects.create(name='Project Leader')
        self.org_leader_group = Group.objects.create(name='Organization Leader')

        # Add some users to groups
        self.user_worker.groups.add(self.worker_group)
        self.user_proj_leader.groups.add(self.proj_leader_group)
        self.user_org_leader.groups.add(self.org_leader_group)

        # Create an organization
        self.org = Organization.objects.create(
            name='Test Org 2',
            slug='test-org-2')

        # Create a project associated with the organization
        self.proj = Project.objects.create(
            name='Test Proj 2',
            organization=self.org,
            slug='test-proj-2')

        # Adding users to the project
        self.proj.users.add(self.user_worker, self.user_proj_leader)

        # Create a task associated with the project
        self.task = Task.objects.create(
            name='Test Task 2',
            description='Test',
            status='Backlog',
            estimated_time='5',
            project=self.proj,
            label='Bug',
            slug='test-task-2')

        # Add users to the task
        self.task.users.set([self.user_worker, self.user_proj_leader])

        # Set the task URL
        self.url = f'/api/v1/tasks/{self.task.slug}/'

    def test_get_task_detail_worker(self):
        """Test worker in proj can get task-detail"""
        self.client.force_authenticate(user=self.user_worker)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['name'], self.task.name)

    def test_get_task_detail_worker_not_in_proj(self):
        """Test worker not in proj can not get task-detail"""
        self.client.force_authenticate(user=self.user_worker2)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_task_detail_proj_leader(self):
        """Test proj leader in proj can get task-detail"""
        self.client.force_authenticate(user=self.user_proj_leader)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['name'], self.task.name)

    def test_get_task_detail_org_leader(self):
        """Test org leader in proj can not get task-detail"""
        self.client.force_authenticate(user=self.user_org_leader)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_task_detail_not_authorized(self):
        """Test not authorized user can not get task-detail"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_task_detail_worker(self):
        """Test worker in proj can delete task."""
        self.client.force_authenticate(user=self.user_worker)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_delete_task_detail_worker_not_in_proj(self):
        """Test worker not in proj can not delete task."""
        self.client.force_authenticate(user=self.user_worker2)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_task_detail_proj_leader(self):
        """Test proj-leader in proj can delete task."""
        self.client.force_authenticate(user=self.user_proj_leader)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
