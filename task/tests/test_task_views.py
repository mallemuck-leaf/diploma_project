from datetime import datetime
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.test import TestCase, Client
from django.contrib.auth.models import User
from task.models import Person, Category, Priority, Task
from account.models import Profile
from django.urls import reverse


class TaskListViewTest(TestCase):
    '''
    Tests for task_list view (get action)
    '''

    def setUp(self):
        self.client = Client()
        self.test_user_info = {'username': 'testuser1',
                               'password': 'pass123word'}
        self.test_user1 = User.objects.create_user(username=self.test_user_info['username'],
                                                   password=self.test_user_info['password'])
        self.test_user1.save()
        Profile.objects.create(user=self.test_user1)

    def test_task_list_authorize_user(self):
        '''
        for authorized user
        '''
        self.client.login(username=self.test_user_info['username'],
                          password=self.test_user_info['password'])
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='task/task_list.html')

    def test_task_list_anonimous_user(self):
        '''
        for anonimous user (redirect to login page)
        '''
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 302)


class TaskDetailViewTest(TestCase):
    '''
    Tests for task_list view (get action)
    '''

    def setUp(self):
        self.client = Client()
        self.test_user_info = {'username': 'testuser1',
                               'password': 'pass123word'}
        self.test_user = User.objects.create_user(username=self.test_user_info['username'],
                                                  password=self.test_user_info['password'])
        self.test_user.save()
        self.test_person = Person.objects.get(user=self.test_user)
        priority = Priority.objects.create(name='testpriority', created_by=self.test_person)
        category = Category.objects.create(name='testcategory', created_by=self.test_person, description='categoryinfo')
        self.test_task = Task.objects.create(created_by=self.test_person,
                                             title='test_task',
                                             description='test_content',
                                             completed='2024-12-09 00:00:00+03:00',
                                             priority=priority,
                                             category=category,
                                             status='p')
        self.test_task.save()

    def test_task_detail_authorize_user(self):
        '''
        for authorized user
        '''
        self.client.login(username=self.test_user_info['username'],
                          password=self.test_user_info['password'])
        response = self.client.get(f'/tasks/{self.test_task.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='task/task_detail.html')

    def test_task_detail_anonimous_user(self):
        '''
        for anonimous user (redirect to login page)
        '''
        response = self.client.get(f'/tasks/{self.test_task.pk}/')
        self.assertEqual(response.status_code, 302)


class TaskUpdateViewTest(TestCase):
    '''
    Tests for task_list view (get action)
    '''

    def setUp(self):
        self.client = Client()
        self.test_user_info = {'username': 'testuser1',
                               'password': 'pass123word'}
        self.test_user = User.objects.create_user(username=self.test_user_info['username'],
                                                  password=self.test_user_info['password'])
        self.test_user.save()
        self.test_person = Person.objects.get(user=self.test_user)
        priority = Priority.objects.create(name='testpriority', created_by=self.test_person)
        category = Category.objects.create(name='testcategory', created_by=self.test_person, description='categoryinfo')
        self.test_task = Task.objects.create(created_by=self.test_person,
                                             title='test_task',
                                             description='test_content',
                                             completed='2024-12-09 00:00:00+03:00',
                                             priority=priority,
                                             category=category,
                                             status='p')
        self.test_task.save()
        self.url = f'/tasks/update/{self.test_task.pk}'

    def test_task_update_authorize_user(self):
        '''
        for authorized user
        '''
        self.client.login(username=self.test_user_info['username'],
                          password=self.test_user_info['password'])
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='task/task_detail.html')

    def test_task_update_anonimous_user(self):
        '''
        for anonimous user (redirect to login page)
        '''
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


class TaskDeleteViewTest(TestCase):
    '''
    Tests for task_list view (get action)
    '''

    def setUp(self):
        self.client = Client()
        self.test_user_info = {'username': 'testuser1',
                               'password': 'pass123word'}
        self.test_user = User.objects.create_user(username=self.test_user_info['username'],
                                                  password=self.test_user_info['password'])
        self.test_user.save()
        self.test_person = Person.objects.get(user=self.test_user)
        priority = Priority.objects.create(name='testpriority', created_by=self.test_person)
        category = Category.objects.create(name='testcategory', created_by=self.test_person, description='categoryinfo')
        self.test_task = Task.objects.create(created_by=self.test_person,
                                             title='test_task',
                                             description='test_content',
                                             completed='2024-12-09 00:00:00+03:00',
                                             priority=priority,
                                             category=category,
                                             status='p')
        self.test_task.save()
        self.url = f'/tasks/delete/{self.test_task.pk}'

    def test_task_delete_authorize_user(self):
        '''
        for authorized user
        '''
        self.client.login(username=self.test_user_info['username'],
                          password=self.test_user_info['password'])
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='task/task_delete.html')

    def test_task_delete_anonimous_user(self):
        '''
        for anonimous user (redirect to login page)
        '''
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
