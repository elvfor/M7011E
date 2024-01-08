from django.test import TestCase

# Create your tests here.

from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Task
from project.models import Project
from organization.models import Organization


class TaskListTest(APITestCase):
    """Tests for TaskList view."""

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

        self.org.users.add(self.user_worker, self.user_proj_leader)

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
        # self.url = f'/api/v1/projects/{self.task.slug}/tasks/'
        # Set the project URL
        self.url = f'/api/v1/projects/{self.proj.slug}/tasks/'

    def test_get_task_list_worker(self):
        """Test worker is authorized to get task-list"""
        self.client_worker.force_authenticate(user=self.user_worker)
        response = self.client_worker.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_task_list_worker_not_in_proj(self):
        """Test worker not in proj can not get task-list"""
        self.client.force_authenticate(user=self.user_worker2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_task_list_proj_leader(self):
        """Test proj-leader in proj can get task-list"""
        self.client.force_authenticate(user=self.user_proj_leader)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data['name'], self.task.name)

    def test_get_task_list_org_leader(self):
        """Test org-leader can not get task-list"""
        self.client.force_authenticate(user=self.user_org_leader)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_task_list_not_authorized(self):
        """Test user not authorized can not get task-list"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_task_worker(self):
        """Test worker in proj can create a new Task."""
        self.client.force_authenticate(user=self.user_worker)

        payload = {
            'name': 'New Task',
            'description': 'A new task',
            'status': 'Backlog',
            'estimated_time': '5',
            'project': self.proj.slug,
            'label': 'bug',
            'users': [self.user_worker.id],
            'slug': 'test-task-2'
        }
        response = self.client.post(self.url, payload)

        # Print response content for debugging
        print(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.filter(name='New Task').count(), 1)
        self.assertEqual(Project.objects.filter(name='New Task').first().name, 'New Task')

    def test_post_proj_leader(self):
        """Test Project leader can create a new Task."""
        self.client.force_authenticate(user=self.user_proj_leader)

        payload = {
            'name': 'New Task',
            'description': 'A new task',
            'status': 'Backlog',
            'estimated_time': '5',
            'project': self.proj.slug,
            'label': 'bug',
            'users': [self.user_proj_leader.id],
            'slug': 'test-proj-2'
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.filter(name='New Task').count(), 1)
        self.assertEqual(Project.objects.filter(name='New Task').first().name, 'New Task')

    def test_post_org_leader(self):
        """Test Org leader can not create a new Task."""
        self.client.force_authenticate(user=self.user_org_leader)

        payload = {
            'name': 'New Task',
            'description': 'A new task',
            'status': 'Backlog',
            'estimated_time': '5',
            # 'project': self.proj.slug,
            'label': 'bug',
            'users': [self.user_org_leader.id],
            'slug': 'slugNewTask'
        }
        response = self.client.post(self.url, payload)

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
