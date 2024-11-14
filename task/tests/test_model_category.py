from django.contrib.auth.models import User
from django.test import TestCase
from task.models import Category, Person


class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='Anna',
                            password='pass123word',
                            email='pass@mail.ru')
        Category.objects.create(name='Категория 1',
                                description='Категория для теста.',
                                created_by=Person.objects.get(id=1))

    def test_name_label(self):
        category = Category.objects.get(id=1)
        field_name = category._meta.get_field('name').verbose_name
        self.assertEqual(field_name, 'name')

    def test_name_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('name'). max_length
        self.assertEqual(max_length, 30)

    def test_description_label(self):
        category = Category.objects.get(id=1)
        field_name = category._meta.get_field('description').verbose_name
        self.assertEqual(field_name, 'description')

    def test_description_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('description'). max_length
        self.assertEqual(max_length, 200)

    def test_created_by_label(self):
        category = Category.objects.get(id=1)
        field_name = category._meta.get_field('created_by').verbose_name
        self.assertEqual(field_name, 'created by')

    def test_created_at_label(self):
        category = Category.objects.get(id=1)
        field_name = category._meta.get_field('created_at').verbose_name
        self.assertEqual(field_name, 'created at')

    def test_updated_at_label(self):
        category = Category.objects.get(id=1)
        field_name = category._meta.get_field('updated_at').verbose_name
        self.assertEqual(field_name, 'updated at')

    def test_deleted_at_label(self):
        category = Category.objects.get(id=1)
        field_name = category._meta.get_field('deleted_at').verbose_name
        self.assertEqual(field_name, 'deleted at')

    def test_deleted_label(self):
        category = Category.objects.get(id=1)
        field_name = category._meta.get_field('deleted').verbose_name
        self.assertEqual(field_name, 'deleted')

    def test_object_name_str(self):
        category = Category.objects.get(id=1)
        expected_object_name = 'Категория 1'
        self.assertEqual(expected_object_name, str(category))
