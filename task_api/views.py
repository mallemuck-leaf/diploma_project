from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsAdminOrUserIDOnly
from task.models import Person, Task, Priority, Category
from .serializers import (
    PersonListSerializer, PersonDetailSerializer
)
from .mixins import (
    SerializerPersonMixin, SerializerPriorityMixin, SerializerCategoryMixin, SerializerTaskMixin,
    AbstractQuerysetClassMixin, PersonQuerysetClassMixin,
    AbstractDestroyMixin,
)


class PersonViewSet(SerializerPersonMixin, PersonQuerysetClassMixin, ModelViewSet):
    # queryset = Person.objects.all()
    permission_classes = [IsAdminOrUserIDOnly]


class PriorityViewSet(SerializerPriorityMixin, AbstractQuerysetClassMixin, AbstractDestroyMixin, ModelViewSet):
    # queryset = Priority.objects.all()
    permission_classes = [IsAuthenticated]
    obj_model = Priority
    redirect_url = '/api/v1/priorities/'


class CategoryViewSet(SerializerCategoryMixin, AbstractQuerysetClassMixin, AbstractDestroyMixin, ModelViewSet):
    # queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]
    obj_model = Category
    redirect_url = '/api/v1/categories/'


class TaskViewSet(SerializerTaskMixin, AbstractQuerysetClassMixin, AbstractDestroyMixin, ModelViewSet):
    # queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]
    obj_model = Task
    redirect_url = '/api/v1/tasks/'
