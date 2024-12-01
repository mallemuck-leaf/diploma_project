from task.models import Priority, Person
from task_api.serializers.priority_serializers import PriorityAdminSerializer
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status


class CreatePrioritiesTest(TestCase):
    def setUp(self):
        '''
        Create users and data for tests.
        '''
        user = User.objects.create_user(username='testuser', password='pass123word')
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        self.url = '/api/v1/priorities/'
        self.user = Person.objects.first()
        self.data = {'name': 'priority_1'}

    def test_user_create_priorities(self):
        '''
        Create priority for user (created by user)
        '''
        response = self.client.post(self.url, self.data)
        priority = Priority.objects.first()
        serializer = PriorityAdminSerializer(priority)
        self.assertEqual(serializer.data['created_by']['user']['username'], self.user.user.username)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_invalid_create_priorities(self):
        '''
        Invalid create priority by user
        Not data
        '''
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CreateAdminPrioritiesTest(TestCase):
    def setUp(self):
        '''
        Create users and data for tests.
        '''
        user = User.objects.create_user(username='testuser', password='pass123word', is_staff=True)
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        self.url = '/api/v1/priorities/'
        self.user = Person.objects.first()
        self.data = {'name': 'priority_1'}

    def test_admin_create_priorities(self):
        '''
        Create priority for user (created by admin)
        '''
        response = self.client.post(self.url, self.data)
        priority = Priority.objects.first()
        serializer = PriorityAdminSerializer(priority)
        self.assertEqual(serializer.data['created_by']['user']['username'], self.user.user.username)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_invalid_create_priorities(self):
        '''
        Invalid create priority by user
        Not data
        '''
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CreateAnonimousPrioritiesTest(TestCase):
    def setUp(self):
        '''
        Create users and data for tests.
        Not authenticated!
        '''
        User.objects.create_user(username='testuser', password='pass123word')
        self.client = APIClient()
        self.url = '/api/v1/priorities/'
        self.data = {'name': 'priority_1'}

    def test_anonimous_create_priorities(self):
        '''
        Create priority (created by anonimous user) is blocked
        access must be blocked (status 403 forbidden)
        '''
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
