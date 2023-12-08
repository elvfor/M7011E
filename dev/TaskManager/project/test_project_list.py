from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Project
from organization.models import Organization


class ProjectListTest(APITestCase):
    """Test for ProjectDetail view."""

    def setUp(self):
        self.client = APIClient()

        # create users
        self.user_worker = User.objects.create_user(username='worker',
                                                    password='testpass123')
        self.user_worker2 = User.objects.create_user(username='worker2',
                                                     password='testpass123')
        self.user_proj_leader = User.objects.create_user(username='proj_leader',
                                                         password='testpass123')
        self.user_org_leader = User.objects.create_user(username='org_leader',
                                                        password='testpass123')

        self.organization = Organization.objects.create(name='Test Organization',
                                                        slug='test-org')
        self.project = Project.objects.create(name='Test Project',
                                              slug='test-project',
                                              organization=self.organization)
        self.project2 = Project.objects.create(name='Test Project2',
                                               slug='test-project2',
                                               organization=self.organization)
        # add certain users to orgs + projs
        self.organization.users.add(self.user_worker)
        self.organization.users.add(self.user_proj_leader)

        self.project.users.add(self.user_worker)
        self.project2.users.add(self.user_worker)
        self.project.users.add(self.user_proj_leader)

        # create Groups and add users to said groups
        self.worker_group = Group.objects.create(name='Worker')
        self.proj_leader_group = Group.objects.create(name='Project Leader')
        self.org_leader_group = Group.objects.create(name='Organization Leader')
        self.user_worker.groups.add(self.worker_group)
        self.user_worker2.groups.add(self.worker_group)
        self.user_proj_leader.groups.add(self.proj_leader_group)
        self.user_org_leader.groups.add(self.org_leader_group)

        self.url = f'/api/v1/organizations/{self.organization.slug}/projects/'

    def test_get_project_list_worker_in_org(self):
        """Test worker in org can get projects list"""
        self.client.force_authenticate(user=self.user_worker)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 2)

    def test_get_project_list_worker_not_in_org(self):
        """Test worker not in org can not get projects list"""
        self.client.force_authenticate(user=self.user_worker2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_project_list_org_leader_in_org(self):
        """Test orgleader in org can not get projects list"""
        self.client.force_authenticate(user=self.user_org_leader)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_project_list_org_leader_in_org(self):
        """Test orgleader in org can not get projects list"""
        self.client.force_authenticate(user=self.user_org_leader)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_project_list_proj_leader_in_org(self):
        """Test proj leader in org can get projects list"""
        self.client.force_authenticate(user=self.user_proj_leader)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 1)

    def test_get_project_list_not_authenticated(self):
        """Test no one can get Project list when not authenticated"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_project_proj_leader(self):
        """Test Project leader can create a new Project."""
        self.client.force_authenticate(user=self.user_proj_leader)

        payload = {
            'name': 'New Project22',
            'users': self.user_proj_leader.id,
            'slug': 'slugNewProject22',
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.filter(name='New Project22').count(), 1)
        self.assertEqual(Project.objects.filter(name='New Project22').first().name, 'New Project22')

    def test_post_project_org_leader(self):
        """Test Organization leader can not create a new Project."""
        self.client.force_authenticate(user=self.user_org_leader)

        payload = {
            'name': 'New Project',
            'users': self.user_proj_leader.id,
            'slug': 'slugNewProject',

        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_project_worker(self):
        """Test Worker can not create a new Project."""
        self.client.force_authenticate(user=self.user_worker)

        payload = {
            'name': 'New Project',
            'users': self.user_proj_leader.id,
            'slug': 'slugNewProject',

        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
