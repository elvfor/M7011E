from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Project
from django.contrib.auth import get_user_model


class ProjectDetailTest(APITestCase):
    """Test for ProjectDetail view."""

    def setUp(self):
        self.client = APIClient()
        # Create users
        self.superuser = get_user_model().objects.create_superuser(username='superusertest', password='testpass123')

        self.user_worker = User.objects.create_user(username='worker',
                                                    password='testpass123')
        self.user_worker2 = User.objects.create_user(username='worker2',
                                                     password='testpass123')
        self.user_proj_leader = User.objects.create_user(username='proj_leader',
                                                         password='testpass123')
        self.user_org_leader = User.objects.create_user(username='org_leader',
                                                        password='testpass123')
        # create test Project
        self.project = Project.objects.create(name='Test Project',
                                              slug='test-project',
                                              )
        # add some users to project
        self.project.users.add(self.user_worker)
        self.project.users.add(self.user_proj_leader)

        # create Groups and add users to said groups
        self.worker_group = Group.objects.create(name='Worker')
        self.proj_leader_group = Group.objects.create(name='Project Leader')
        self.org_leader_group = Group.objects.create(name='Organization Leader')
        self.user_worker.groups.add(self.worker_group)
        self.user_worker2.groups.add(self.worker_group)
        self.user_proj_leader.groups.add(self.proj_leader_group)
        self.user_org_leader.groups.add(self.org_leader_group)

        self.url = f'/api/v1/projects/{self.project.slug}/'

    def test_get_proj_detail_worker(self):
        """Test worker in proj can get proj-detail"""
        self.client.force_authenticate(user=self.user_worker)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['name'], self.project.name)

    def test_get_proj_detail_superuser(self):
        """Test superuser can get proj-detail"""
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['name'], self.project.name)
    def test_get_proj_detail_worker_not_in_proj(self):
        """Test worker not in proj can not get proj-detail"""
        self.client.force_authenticate(user=self.user_worker2)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_proj_detail_proj_leader(self):
        """Test proj-leader in proj can get proj-detail"""
        self.client.force_authenticate(user=self.user_proj_leader)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.project.name)

    def test_get_proj_detail_not_authenticated(self):
        """Test proj-leader in proj can get proj-detail"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_proj_detail_org_leader(self):
        """Test org-leader can not get proj-detail"""
        self.client.force_authenticate(user=self.user_org_leader)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_proj_proj_leader(self):
        """Test Proj leader can update project it is in."""
        self.client.force_authenticate(user=self.user_proj_leader)
        payload = {'name': 'Updated Project'}
        response = self.client.patch(self.url, payload)

        self.project.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.project.name, 'Updated Project')

    def test_update_proj_superuser(self):
        """Test superuser can update project it is in."""
        self.client.force_authenticate(user=self.superuser)
        payload = {'name': 'Updated Project'}
        response = self.client.patch(self.url, payload)

        self.project.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.project.name, 'Updated Project')

    def test_delete_proj_as_proj_leader(self):
        """Test can deleta a project as a proj leader."""
        self.client.force_authenticate(user=self.user_proj_leader)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), 0)

    def test_delete_proj_as_superuser(self):
        """Test can deleta a project as a superuser."""
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), 0)


    def test_update_proj_worker(self):
        """Test Worker can not update project it is in."""
        self.client.force_authenticate(user=self.user_worker)
        payload = {'name': 'Updated Project'}
        response = self.client.patch(self.url, payload)

        self.project.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
