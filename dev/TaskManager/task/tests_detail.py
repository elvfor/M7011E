from django.test import TestCase

# Create your tests here.

from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Task


class TaskDetailTest(APITestCase):
    """Tests for TaskDetail view."""

    def setUp(self):
        self.client_worker = APIClient()

        # Worker
        self.user_worker = User.objects.create_user(username='worker', password='testpass123')
        self.worker_group = Group.objects.create(name='Worker')
        self.user_worker.groups.add(self.worker_group)

        # Project Leader
        self.user_proj_leader = User.objects.create_user(username='proj_leader', password='testpass123')
        self.proj_leader_group = Group.objects.create(name='Project Leader')
        self.user_proj_leader.groups.add(self.proj_leader_group)

        # Task
        self.task = Task.objects.create(name='Test Task 2', slug='test-org-2')
        self.task.users.set([self.user_worker])
        self.url = f'/api/v1/organizations/projects/tasks{self.tasks.slug}/' #FIXA

    def test_retrieve_task_detail_worker(self):
        """Test Worker is Unauthorized to get task details"""
        self.client.force_authenticate(user=self.user_worker)
        response_worker = self.client_worker.get(self.url)
        self.assertEqual(response_worker.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_proj_detail_proj_leader(self):
        """Test that Organization Leader can get organization details"""
        self.client.force_authenticate(user=self.user_proj_leader)
        response_worker = self.client_worker.get(self.url)
        self.assertEqual(response_worker.status_code, status.HTTP_200_OK)