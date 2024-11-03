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
)


class PersonViewSet(SerializerPersonMixin, PersonQuerysetClassMixin, ModelViewSet):
    # queryset = Person.objects.all()
    permission_classes = [IsAdminOrUserIDOnly]


class PriorityViewSet(SerializerPriorityMixin, AbstractQuerysetClassMixin, ModelViewSet):
    # queryset = Priority.objects.all()
    permission_classes = [IsAuthenticated]
    obj_model = Priority


class CategoryViewSet(SerializerCategoryMixin, AbstractQuerysetClassMixin, ModelViewSet):
    # queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]
    obj_model = Category


class TaskViewSet(SerializerTaskMixin, AbstractQuerysetClassMixin, ModelViewSet):
    # queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]
    obj_model = Task
