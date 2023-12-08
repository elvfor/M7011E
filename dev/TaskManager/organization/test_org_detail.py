from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Organization


class OrganizationDetailTest(APITestCase):
    """Tests for OrganizationDetail view."""

    def setUp(self):
        self.client = APIClient()

        # Worker
        self.user_worker = User.objects.create_user(username='worker', password='testpass123')
        self.worker_group = Group.objects.create(name='Worker')
        self.user_worker.groups.add(self.worker_group)

        # Project Leader
        self.user_proj_leader = User.objects.create_user(username='proj_leader', password='testpass123')
        self.proj_leader_group = Group.objects.create(name='Project Leader')
        self.user_proj_leader.groups.add(self.proj_leader_group)

        # Organization Leader
        self.user_org_leader = User.objects.create_user(username='org_leader', password='testpass123')
        self.org_leader_group = Group.objects.create(name='Organization Leader')
        self.user_org_leader.groups.add(self.org_leader_group)

        # Organization Leader (not in org)
        self.user_org_leader2 = User.objects.create_user(username='org_leader2', password='testpass123')
        self.user_org_leader2.groups.add(self.org_leader_group)

        # Organization
        self.organization = Organization.objects.create(name='Test Organization 2',
                                                        slug='test-org-2')
        self.organization.users.add(self.user_worker)
        self.organization.users.add(self.user_proj_leader)
        self.organization.users.add(self.user_org_leader)
        self.url = f'/api/v1/organizations/{self.organization.slug}/'

    def test_get_org_detail_worker(self):
        """Test Worker is Unauthorized to get organization details"""
        self.client.force_authenticate(user=self.user_worker)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_org_detail_proj_leader(self):
        """Test Project Leader is Unauthorized to get organization details"""
        self.client.force_authenticate(user=self.user_proj_leader)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_org_detail_org_leader(self):
        """Test that Organization Leader can get organization details"""
        self.client.force_authenticate(user=self.user_org_leader)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_org_detail_org_leader_not_auth(self):
        """Test that an unauthorized user can not get organization details"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_org_detail_org_leader_not_in_org(self):
        """Test that Organization Leader not in organization cannot get organization details"""
        self.client.force_authenticate(user=self.user_org_leader2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_organization(self):
        """Test updating the organization for authenticated organization leader"""
        self.client.force_authenticate(user=self.user_org_leader)

        payload = {'name': 'Test Organization 3',
                   'slug': 'test-org-3'}

        response = self.client.patch(self.url, payload)

        self.organization.refresh_from_db()
        self.assertEqual(self.organization.name, payload['name'])
        self.assertEqual(self.organization.slug, payload['slug'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_organization(self):
        """Test deleting the organization for authenticated organization leader"""
        self.client.force_authenticate(user=self.user_org_leader)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Organization.objects.count(), 0)
