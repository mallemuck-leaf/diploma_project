from django.http import Http404
from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.contrib.auth.models import User
from task.models import Person, Category, Priority, Task
from account.models import Profile
from django.urls import reverse


class PriorityCRUDTest(TestCase):
    count_priorities = 3

    @classmethod
    def setUpClass(cls):
        print('setUp')
        test_user1 = User.objects.create_user(username='testuser1', password='pass123word')
        test_user1.save()
        test_user2 = User.objects.create_user(username='testuser2', password='pass123word')
        test_user2.save()
        Profile.objects.create(user=User.objects.get(id=1))
        Profile.objects.create(user=User.objects.get(id=2))
        for item in range(cls.count_priorities):
            user_id = item % 2 + 1
            Priority.objects.create(name=f'priority_{item}',
                                    created_by=Person.objects.get(id=user_id))
        cls.assertEqual(Priority.objects.all().count(), cls.count_priorities, )

    def test_priority_not_found(self):
        print('test_priority_not_found is run')
        for item in range(self.count_priorities + 1):
            try:
                priority = get_object_or_404(Priority, name=f'priority_{item}')
                self.assertEqual(priority.name, f'priority_{item}')
            except Http404:
                print(f'Priority "priority_{item}" not found.')

    def test_priority_update(self):
        print('test_update_priority is run')
        old_name = 'priority_1'
        new_name = 'priority_11'
        try:
            priority = Priority.objects.get(name=old_name)
            print(priority)
            priority.name = new_name
            priority.save()
        except Http404:
            print(f'Priority "{old_name}" not found before update name.')
        try:
            priority = Priority.objects.get(name=old_name)
        except Http404:
            print(f'Priority "{old_name}" not found after update name.')

