from datetime import datetime
from task.models import Priority, Person
from task_api.serializers.priority_serializers import PriorityPostSerializer
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status


class DeleteUserPrioritiesTest(TestCase):
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

        self.priority_by_user = Priority.objects.create(name='priority_1',
                                                        created_by=self.user,
                                                        updated_at=datetime.now())
        self.priority_by_other = Priority.objects.create(name='priority_2',
                                                         created_by=self.other_user,
                                                         updated_at=datetime.now())

        self.url_user_obj = f'/api/v1/priorities/{self.priority_by_user.pk}/'
        self.url_other_user_obj = f'/api/v1/priorities/{self.priority_by_other.pk}/'

    def test_user_delete_priority(self):
        '''
        Delete priority for user (created by user)
        '''
        response = self.client.delete(self.url_user_obj)
        priority = Priority.objects.get(pk=self.priority_by_user.pk)
        self.assertNotEqual(priority.deleted_at, None)
        self.assertEqual(priority.deleted, None)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_user_invalid_delete_priorities(self):
        '''
        Delete priority for user (created by other user)
        '''
        response = self.client.delete(self.url_other_user_obj)
        priority = Priority.objects.get(pk=self.priority_by_other.pk)
        self.assertEqual(priority.deleted_at, None)
        self.assertEqual(priority.deleted, None)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeleteAdminPrioritiesTest(TestCase):
    def setUp(self):
        '''
        Create users and data for tests.
        '''
        admin = User.objects.create_user(username='testuser', password='pass123word', is_staff=True)
        user = User.objects.create_user(username='regularuser', password='pass123word')
        self.client = APIClient()
        self.client.force_authenticate(user=admin)

        self.user_admin = Person.objects.get(user=admin)
        self.user_regular = Person.objects.get(user=user)

        self.obj_by_admin = Priority.objects.create(name='priority_by_admin',
                                                    created_by=self.user_admin,
                                                    updated_at=datetime.now())
        self.obj_by_regular = Priority.objects.create(name='priority_by_user',
                                                      created_by=self.user_regular,
                                                      updated_at=datetime.now())

        self.url_obj_by_admin = f'/api/v1/priorities/{self.obj_by_admin.pk}/'
        self.url_obj_by_user = f'/api/v1/priorities/{self.obj_by_regular.pk}/'

    def test_admin_delete_priorities(self):
        '''
        Delete priority for admin (created by admin)
        '''
        response = self.client.delete(self.url_obj_by_admin)
        priority = Priority.objects.get(pk=self.obj_by_admin.pk)
        self.assertEqual(priority.deleted_at, None)
        self.assertNotEqual(priority.deleted, None)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_admin_put_users_priorities(self):
        '''
        Delete priority for admin (created by user)
        '''
        response = self.client.delete(self.url_obj_by_user)
        priority = Priority.objects.get(pk=self.obj_by_regular.pk)
        self.assertEqual(priority.deleted_at, None)
        self.assertNotEqual(priority.deleted, None)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)


class DeleteAnonimousPrioritiesTest(TestCase):
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

    def test_anonimous_delete_priorities(self):
        '''
        Put priority (created by users) is blocked
        access must be blocked (status 403 forbidden)
        '''
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
