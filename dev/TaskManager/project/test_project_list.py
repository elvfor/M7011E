from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Project
from organization.models import Organization


class ProjectListTest(APITestCase):
    """Test for ProjectDetail view."""

    def setUp(self):
        self.client = APIClient()
        self.user_worker = User.objects.create_user(username='worker',
                                                    password='testpass123')
        self.organization = Organization.objects.create(name='Test Organization',
                                                        slug='test-org')
        self.organization.users.set([self.user_worker])
        self.project = Project.objects.create(name='Test Project',
                                              slug='test-project',
                                              organization=self.organization)
        self.project.users.set([self.user_worker])
        self.worker_group = Group.objects.create(name='Worker')
        self.user_worker.groups.add(self.worker_group)

        self.client.force_authenticate(user=self.user_worker)
        # self.url = reverse('projects:project-detail',
        #                    kwargs={'slug': self.project.slug})
        self.url = f'/api/v1/organizations/{self.organization.slug}/projects/'

    def test_retrieve_user_project_list(self):
        # Make a GET request to retrieve the project detail
        response = self.client.get(self.url)

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the serialized data in the response matches the expected data
        self.assertEqual(len(response.data), 1)
