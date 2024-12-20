from datetime import datetime
from task.models import Priority, Person
from task_api.serializers.priority_serializers import PrioritySerializer, PriorityAdminSerializer
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status


class GetPrioritiesTest(TestCase):
    def setUp(self):
        '''
        Create objects for tests.
        priority 1 and 2 - by self.user
        priority 3 - by self.user2
        '''
        user = User.objects.create_user(username='testuser', password='pass123word')
        user_2 = User.objects.create_user(username='testuser2', password='pass123word')
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        self.url = '/api/v1/priorities/'
        self.user = Person.objects.first()
        self.user2 = Person.objects.get(user=user_2)
        self.priority_1 = Priority.objects.create(name='priority_1', created_by=self.user,
                                                  deleted_at=None, deleted=None)
        self.priority_2 = Priority.objects.create(name='priority_2', created_by=self.user,
                                                  deleted_at=None, deleted=None)
        self.priority_3 = Priority.objects.create(name='priority_3', created_by=self.user2,
                                                  deleted_at=None, deleted=None)
        self.priority_4 = Priority.objects.create(name='priority_3', created_by=self.user,
                                                  deleted_at=datetime.now(), deleted=None)
        self.priority_5 = Priority.objects.create(name='priority_3', created_by=self.user,
                                                  deleted_at=None, deleted=datetime.now())

    def test_get_all_priorities(self):
        '''
        Get all not deleted priorities for user (created by user)
        '''
        response = self.client.get(self.url)
        priorities = Priority.objects.all().filter(created_by=self.user, deleted_at=None, deleted=None)
        serializer = PrioritySerializer(priorities, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_priority(self):
        '''
        Get single priority while created by user
        '''
        get_url = f'{self.url}{self.priority_1.pk}/'
        response = self.client.get(get_url)
        priority = Priority.objects.get(pk=self.priority_1.pk)
        serializer = PrioritySerializer(priority)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_deleted_by_user_priority(self):
        '''
        Not get single priority while created by user and deleted by user
        '''
        get_url = f'{self.url}{self.priority_4.pk}/'
        response = self.client.get(get_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_valid_single_deleted_by_admin_priority(self):
        '''
        Not get single priority while created by user and deleted by admin
        '''
        get_url = f'{self.url}{self.priority_5.pk}/'
        response = self.client.get(get_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_valid_single_not_user_priority(self):
        '''
        Not get single priority while created by not user
        '''
        get_url = f'{self.url}{self.priority_3.pk}/'
        response = self.client.get(get_url)
        # priority = Priority.objects.get(pk=self.priority_3.pk)
        priority = Priority.objects.get(pk=self.priority_3.pk)
        serializer = PrioritySerializer(priority)
        self.assertNotEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_invalid_single_priority(self):
        '''
        Not get single priority with invalid pk
        '''
        get_url = f'{self.url}100/'
        response = self.client.get(get_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetAdminPrioritiesTest(TestCase):
    def setUp(self):
        '''
        Create objects for tests.
        priority 1 and 2 - by self.user
        priority 3 - by self.user2
        '''
        user = User.objects.create_user(username='testuser', password='pass123word')
        user_2 = User.objects.create_user(username='testuser2', password='pass123word', is_staff=True)
        self.client = APIClient()
        self.client.force_authenticate(user=user_2)
        self.url = '/api/v1/priorities/'
        self.user = Person.objects.first()
        self.user2 = Person.objects.get(user=user_2)
        self.priority_1 = Priority.objects.create(name='priority_1', created_by=self.user,
                                                  deleted_at=None, deleted=None)
        self.priority_2 = Priority.objects.create(name='priority_2', created_by=self.user,
                                                  deleted_at=None, deleted=None)
        self.priority_3 = Priority.objects.create(name='priority_3', created_by=self.user,
                                                  deleted_at=None, deleted=None)
        self.priority_4 = Priority.objects.create(name='priority_4', created_by=self.user,
                                                  deleted_at=datetime.now(), deleted=None)
        self.priority_5 = Priority.objects.create(name='priority_5', created_by=self.user,
                                                  deleted_at=None, deleted=datetime.now())

    def test_admin_get_all_priorities(self):
        '''
        Get all not deleted priorities for admin (created by users)
        '''
        response = self.client.get(self.url)
        priorities = Priority.objects.all().filter(deleted_at=None, deleted=None)
        serializer = PriorityAdminSerializer(priorities, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_get_valid_single_priority(self):
        '''
        Get single not deleted priority for admin
        '''
        get_url = f'{self.url}{self.priority_3.pk}/'
        response = self.client.get(get_url)
        priority = Priority.objects.get(pk=self.priority_3.pk)
        serializer = PriorityAdminSerializer(priority)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_get_valid_single_deleted_by_user_priority(self):
        '''
        Not get single priority while deleted by user
        '''
        get_url = f'{self.url}{self.priority_4.pk}/'
        response = self.client.get(get_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_get_valid_single_deleted_by_admin_priority(self):
        '''
        Not get single priority while deleted by admin
        '''
        get_url = f'{self.url}{self.priority_5.pk}/'
        response = self.client.get(get_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_get_invalid_single_priority(self):
        '''
        Not get single priority with invalid pk
        '''
        get_url = f'{self.url}100/'
        response = self.client.get(get_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

