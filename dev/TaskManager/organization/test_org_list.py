from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Organization


class OrganizationListTest(APITestCase):
    """Test for ProjectDetail view."""

    def setUp(self):
        self.client = APIClient()

        # Superuser
        self.superuser = get_user_model().objects.create_superuser(username='superusertest', password='testpass123')

        # Worker
        self.user_worker = User.objects.create_user(username='worker', password='testpass123')
        self.worker_group = Group.objects.create(name='Worker')
        self.user_worker.groups.add(self.worker_group)

        # Organization Leader
        self.user_org_leader = User.objects.create_user(username='org_leader', password='testpass123')
        self.org_leader_group = Group.objects.create(name='Organization Leader')
        self.user_org_leader.groups.add(self.org_leader_group)

        # Organization
        self.organization = Organization.objects.create(name='Test Organization 2',
                                                        slug='test-org-2')

        self.organization.users.add(self.user_worker)
        self.organization.users.add(self.user_org_leader)
        self.url = f'/api/v1/organizations/'

        # Task
        # self.task = Task.objects.create(name='',
        #                                                slug='tasks')

    def test_retrieve_org_list_worker(self):
        """Test that a Worker can not get organization list"""
        self.client.force_authenticate(user=self.user_worker)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_org_list_org_leader(self):
        """Test that an Organization Leader can not get organization list"""
        self.client.force_authenticate(user=self.user_worker)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_org_list_superuser(self):
        """Test that a Superuser can get organization list"""
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_org_list_superuser_not_auth(self):
        """Test that an unauthorized user can not get organization list"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
