from django.test import TestCase
from task.models import Priority, Person
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from task_api.views import PriorityViewSet

# Create your tests here.


class APriorityUserTestCase(APITestCase):
    '''
    Test suite for Priority
    '''

    def setUp(self):
        user = User.objects.create_user(username='testuser', password='pass123word')
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        # person = Person.objects.get(user=user)
        # print(person)
        self.data = {
            'name': 'priority_1',
            'created_by': Person.objects.first(),
        }
        self.url = '/api/v1/priorities/'

    def test_A_create_priority(self):
        '''
        test PriorityViewSet create method
        '''
        data = self.data
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Priority.objects.count(), 1)
        self.assertEqual(Priority.objects.get().name, 'priority_1')

    def test_B_get_priority(self):
        '''
        test PriorityViewSet get method
        '''

        data = self.data
        response = self.client.post(self.url, data)
        put_url = self.url + '2/'
        response = self.client.get(put_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_C_put_priority(self):
        '''
        test PriorityViewSet put method
        '''
        self.client.post(self.url, self.data)
        data = {'name': 'priority_N'}
        put_url = self.url + '3/'
        response = self.client.put(put_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_D_delete_priority(self):
        '''
        test PriorityViewSet delete method
        deleting = adding a date to the field (for user - field "deleted_at")
        '''
        self.client.post(self.url, self.data)
        number_priority_item_in_db = 4
        delete_url = f'{self.url}{number_priority_item_in_db}/'
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(Priority.objects.get(id=number_priority_item_in_db).deleted, None)
        self.assertNotEqual(Priority.objects.get(id=number_priority_item_in_db).deleted_at, None)


class BPriorityAdminTestCase(APITestCase):
    '''
    Variation for admin
    '''

    def setUp(self):
        user = User.objects.create_user(username='testuser', password='pass123word', is_staff=True)
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        self.data = {
            'name': 'priority_1',
            'created_by': Person.objects.first(),
        }
        self.url = '/api/v1/priorities/'

    def test_D_delete_priority(self):
        '''
        test PriorityViewSet delete method
        deleting = adding a date to the field (for admin - field "deleted")
        '''
        self.client.post(self.url, self.data)
        number_priority_item_in_db = 5
        delete_url = f'{self.url}{number_priority_item_in_db}/'
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(Priority.objects.get(id=number_priority_item_in_db).deleted_at, None)
        self.assertNotEqual(Priority.objects.get(id=number_priority_item_in_db).deleted, None)