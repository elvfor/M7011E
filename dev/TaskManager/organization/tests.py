from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Organization


class OrganizationDetailTest(APITestCase):
    """Test for ProjectDetail view."""

    def setUp(self):
        self.client = APIClient()
        self.user_worker = User.objects.create_user(username='worker',
                                                    password='testpass123')
        self.organization = Organization.objects.create(name='Test Organization 2',
                                                        slug='test-org-2')
        self.organization.users.set([self.user_worker])
        self.worker_group = Group.objects.create(name='Worker')
        self.user_worker.groups.add(self.worker_group)

        self.client.force_authenticate(user=self.user_worker)

        self.url = f'/api/v1/organizations/{self.organization.slug}/'

    def test_forbidden_retrieve_organization_detail(self):
        # Make a GET request to retrieve the organization detail
        response = self.client.get(self.url)

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Check if the serialized data in the response matches the expected data
        # self.assertEqual(response.data['name'], self.organization.name)
