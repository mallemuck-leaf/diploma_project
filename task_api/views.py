from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from . import serializers
from .permissions import IsAuthenticatedOrCreateOnly
from task.models import Person, Task, Priority, Category
from .mixins import (
    AbstractQuerysetClassMixin, PersonQuerysetClassMixin, UserDestroyMixin,
    AbstractDestroyMixin, AbstractSerializerClassMixin, AbstractCreateMixin, AbstractUpdateMixin
)


class PersonViewSet(AbstractSerializerClassMixin,
                    PersonQuerysetClassMixin,
                    UserDestroyMixin,
                    ModelViewSet):
    admin_create_serializer = serializers.ProfileSerializer
    admin_list_serializer = serializers.PersonSerializer
    admin_retrieve_serializer = serializers.ProfileSerializer
    admin_other_serializer = serializers.PersonAdminDetailSerializer
    user_create_serializer = serializers.ProfileSerializer
    user_list_serializer = serializers.PersonSerializer
    user_retrieve_serializer = serializers.PersonDetailSerializer
    user_other_serializer = serializers.PersonDetailSerializer
    permission_classes = [IsAuthenticatedOrCreateOnly]


class PriorityViewSet(AbstractSerializerClassMixin,
                      AbstractQuerysetClassMixin,
                      AbstractDestroyMixin,
                      AbstractCreateMixin,
                      AbstractUpdateMixin,
                      ModelViewSet):
    admin_create_serializer = serializers.PriorityAdminSerializer
    admin_list_serializer = serializers.PriorityAdminSerializer
    admin_retrieve_serializer = serializers.PriorityAdminSerializer
    admin_other_serializer = serializers.PriorityAdminSerializer
    user_create_serializer = serializers.PrioritySerializer
    user_list_serializer = serializers.PrioritySerializer
    user_retrieve_serializer = serializers.PrioritySerializer
    user_other_serializer = serializers.PrioritySerializer
    permission_classes = [IsAuthenticated]
    obj_model = Priority
    redirect_url = '/api/v1/priorities/'


class CategoryViewSet(AbstractSerializerClassMixin,
                      AbstractQuerysetClassMixin,
                      AbstractCreateMixin,
                      AbstractUpdateMixin,
                      AbstractDestroyMixin,
                      ModelViewSet):
    admin_create_serializer = serializers.CategoryAdminSerializer
    admin_list_serializer = serializers.CategoryAdminSerializer
    admin_retrieve_serializer = serializers.CategoryAdminSerializer
    admin_other_serializer = serializers.CategoryAdminSerializer
    user_create_serializer = serializers.CategorySerializer
    user_list_serializer = serializers.CategorySerializer
    user_retrieve_serializer = serializers.CategorySerializer
    user_other_serializer = serializers.CategorySerializer
    permission_classes = [IsAuthenticated]
    obj_model = Category
    redirect_url = '/api/v1/categories/'


class TaskViewSet(AbstractSerializerClassMixin,
                  AbstractQuerysetClassMixin,
                  AbstractCreateMixin,
                  AbstractDestroyMixin,
                  ModelViewSet):
    admin_create_serializer = serializers.TaskAdminSerializer
    admin_list_serializer = serializers.TaskAdminSerializer
    admin_retrieve_serializer = serializers.TaskAdminSerializer
    admin_other_serializer = serializers.TaskAdminSerializer
    user_create_serializer = serializers.TaskSerializer
    user_list_serializer = serializers.TaskSerializer
    user_retrieve_serializer = serializers.TaskSerializer
    user_other_serializer = serializers.TaskSerializer
    permission_classes = [IsAuthenticated]
    obj_model = Task
    redirect_url = '/api/v1/tasks/'
