from datetime import datetime
from task.models import Priority, Person
from task_api.serializers.priority_serializers import (
    PrioritySerializer, PriorityAdminSerializer, PriorityPostSerializer,
)
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status


class PutUserPrioritiesTest(TestCase):
    def setUp(self):
        '''
        Create users and data for tests.
        '''
        user = User.objects.create_user(username='testuser', password='pass123word')
        user2 = User.objects.create_user(username='otheruser', password='pass123word')
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        self.user = Person.objects.get(user=user)
        self.other_user = Person.objects.get(user=user2)
        self.priority_for_put = Priority.objects.create(name='priority_1',
                                                        created_by=self.user,
                                                        updated_at=datetime.now())
        self.priority_by_other = Priority.objects.create(name='priority_2',
                                                         created_by=self.other_user,
                                                         updated_at=datetime.now())
        self.data = {'name': 'modified_priority'}
        self.url = f'/api/v1/priorities/{self.priority_for_put.pk}/'
        self.error_url = f'/api/v1/priorities/{self.priority_by_other.pk}/'

    def test_user_put_priority(self):
        '''
        Put priority for user (created by user)
        '''
        response = self.client.put(self.url, data=self.data)
        priority = Priority.objects.get(pk=self.priority_for_put.pk)
        serializer = PriorityPostSerializer(priority)
        self.assertEqual(serializer.data['name'], self.data['name'])
        self.assertNotEqual(serializer.data['updated_at'], self.priority_for_put.updated_at)
        self.assertEqual(serializer.data['created_by'], self.priority_for_put.created_by.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_invalid_put_priorities(self):
        '''
        Put priority for user (created by other user)
        '''
        response = self.client.put(self.error_url, data=self.data)
        priority = Priority.objects.get(pk=self.priority_by_other.pk)
        serializer = PriorityPostSerializer(priority)
        self.assertNotEqual(serializer.data['name'], self.data['name'])
        self.assertEqual(serializer.data['created_by'], self.priority_by_other.created_by.pk)
        self.assertNotEqual(serializer.data['created_by'], self.user)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PutAdminPrioritiesTest(TestCase):
    def setUp(self):
        '''
        Create users and data for tests.
        '''
        user = User.objects.create_user(username='testuser', password='pass123word', is_staff=True)
        user_regular = User.objects.create_user(username='regularuser', password='pass123word')
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        self.user_admin = Person.objects.get(user=user)
        self.user_regular = Person.objects.get(user=user_regular)
        self.obj_by_admin = Priority.objects.create(name='priority_by_admin',
                                                    created_by=self.user_admin,
                                                    updated_at=datetime.now())
        self.obj_by_regular = Priority.objects.create(name='priority_by_admin',
                                                      created_by=self.user_regular,
                                                      updated_at=datetime.now())
        self.data = {'name': 'modified_priority'}
        self.url_obj_by_admin = f'/api/v1/priorities/{self.obj_by_admin.pk}/'
        self.url_obj_by_regular = f'/api/v1/priorities/{self.obj_by_regular.pk}/'

    def test_admin_put_priorities(self):
        '''
        Put priority for admin (created by admin)
        '''
        PutSerializer = PriorityPostSerializer
        pk = self.obj_by_admin.pk

        priority = Priority.objects.get(pk=pk)
        serializer = PutSerializer(priority)
        old_object = serializer.data

        response = self.client.put(self.url_obj_by_admin, self.data)
        priority = Priority.objects.get(pk=pk)
        serializer = PutSerializer(priority)

        self.assertNotEqual(serializer.data['updated_at'], old_object['updated_at'])
        self.assertEqual(response.data['name'], serializer.data['name'])
        self.assertEqual(serializer.data['created_by'], old_object['created_by'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_put_users_priorities(self):
        '''
        Put priority for admin (created by user)
        '''

        PutSerializer = PriorityPostSerializer
        pk = self.obj_by_regular.pk

        priority = Priority.objects.get(pk=pk)
        serializer = PutSerializer(priority)
        old_object = serializer.data

        response = self.client.put(self.url_obj_by_regular, self.data)
        priority = Priority.objects.get(pk=pk)
        serializer = PutSerializer(priority)

        self.assertNotEqual(serializer.data['updated_at'], old_object['updated_at'])
        self.assertEqual(response.data['name'], serializer.data['name'])
        self.assertEqual(serializer.data['created_by'], old_object['created_by'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PutAnonimousPrioritiesTest(TestCase):
    def setUp(self):
        '''
        Create users and data for tests.
        Not authenticated!
        '''
        user = User.objects.create_user(username='testuser', password='pass123word')
        self.client = APIClient()
        self.user = Person.objects.get(user=user)
        self.object = Priority.objects.create(name='priority_1',
                                              created_by=self.user)
        self.url = f'/api/v1/priorities/{self.object.pk}/'
        self.data = {'name': 'modified_priority'}

    def test_anonimous_put_priorities(self):
        '''
        Put priority (created by users) is blocked
        access must be blocked (status 403 forbidden)
        '''
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
