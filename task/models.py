from django.db import models
from django.conf import settings
from django.utils import timezone


class Person(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='is_user')

    def __str__(self):
        if self.user.first_name is not None and self.user.last_name is not None:
            return f'{self.user.first_name} {self.user.last_name}'
        if self.user.first_name is not None:
            return f'{self.user.first_name} -'
        if self.user.last_name is not None:
            return f'- {self.user.last_name}'
        return f'{self.user.username}'


class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=200)
    created_by = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='category_created_by')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    deleted_at = models.DateTimeField(default=None, blank=True, null=True, editable=False)
    deleted = models.DateTimeField(blank=True, default=None, null=True, editable=False)

    def __str__(self):
        return self.name


class Priority(models.Model):
    name = models.CharField(max_length=30)
    created_by = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='priority_created_by')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    deleted_at = models.DateTimeField(default=None, blank=True, null=True, editable=False)
    deleted = models.DateTimeField(blank=True, default=None, null=True, editable=False)

    def __str__(self):
        return self.name


class Status(models.TextChoices):
    WAITING = 'w', 'в ожидании'
    INPROCESS = 'p', 'выполняется'
    COMPLETE = 'c', 'выполнено'


class Task(models.Model):
    created_by = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='task_created_by')
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.WAITING)
    completed = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    completed_at = models.DateTimeField(default=None, blank=True, null=True, editable=False)
    deleted_at = models.DateTimeField(default=None, blank=True, null=True, editable=False)
    deleted = models.DateTimeField(blank=True, default=None, null=True, editable=False)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name='task_category')
    priority = models.ForeignKey('Priority', on_delete=models.SET_NULL, null=True, related_name='task_priority')

    def __str__(self):
        return self.title
