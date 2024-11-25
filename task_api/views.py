# from datetime import datetime
# from django.core.exceptions import ObjectDoesNotExist
# from django.http import Http404
# from django.shortcuts import render
# from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
# from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from .serializers import (
    person_serializers, priority_serializers, category_serializers, task_serializers
)
from .permissions import IsAuthenticatedOrCreateOnly
from task.models import Task, Priority, Category
from .mixins import (
    AbstractQuerysetClassMixin, PersonQuerysetClassMixin, UserDestroyMixin,
    AbstractDestroyMixin, AbstractSerializerClassMixin, AbstractCreateMixin, AbstractUpdateMixin,
    DeletedObjectsQuerysetClassMixin, DeletedUserObjectsMixin,
)


class PersonViewSet(AbstractSerializerClassMixin,
                    PersonQuerysetClassMixin,
                    UserDestroyMixin,
                    ModelViewSet):
    admin_create_serializer = person_serializers.ProfileSerializer
    admin_list_serializer = person_serializers.PersonSerializer
    admin_retrieve_serializer = person_serializers.ProfileSerializer
    admin_other_serializer = person_serializers.PersonAdminDetailSerializer
    user_create_serializer = person_serializers.ProfileSerializer
    user_list_serializer = person_serializers.PersonSerializer
    user_retrieve_serializer = person_serializers.PersonDetailSerializer
    user_other_serializer = person_serializers.PersonDetailSerializer
    permission_classes = [IsAuthenticatedOrCreateOnly]


class PriorityViewSet(AbstractSerializerClassMixin,
                      AbstractQuerysetClassMixin,
                      AbstractDestroyMixin,
                      AbstractCreateMixin,
                      AbstractUpdateMixin,
                      ModelViewSet):
    admin_create_serializer = priority_serializers.PriorityAdminSerializer
    admin_list_serializer = priority_serializers.PriorityAdminSerializer
    admin_retrieve_serializer = priority_serializers.PriorityAdminSerializer
    admin_other_serializer = priority_serializers.PriorityAdminSerializer
    user_create_serializer = priority_serializers.PrioritySerializer
    user_list_serializer = priority_serializers.PrioritySerializer
    user_retrieve_serializer = priority_serializers.PrioritySerializer
    user_other_serializer = priority_serializers.PrioritySerializer
    permission_classes = [IsAuthenticated]
    obj_model = Priority
    redirect_url = '/api/v1/priorities/'


class CategoryViewSet(AbstractSerializerClassMixin,
                      AbstractQuerysetClassMixin,
                      AbstractCreateMixin,
                      AbstractUpdateMixin,
                      AbstractDestroyMixin,
                      ModelViewSet):
    admin_create_serializer = category_serializers.CategoryAdminSerializer
    admin_list_serializer = category_serializers.CategoryAdminSerializer
    admin_retrieve_serializer = category_serializers.CategoryAdminSerializer
    admin_other_serializer = category_serializers.CategoryAdminSerializer
    user_create_serializer = category_serializers.CategorySerializer
    user_list_serializer = category_serializers.CategorySerializer
    user_retrieve_serializer = category_serializers.CategorySerializer
    user_other_serializer = category_serializers.CategorySerializer
    permission_classes = [IsAuthenticated]
    obj_model = Category
    redirect_url = '/api/v1/categories/'


class TaskViewSet(AbstractSerializerClassMixin,
                  AbstractQuerysetClassMixin,
                  AbstractCreateMixin,
                  AbstractDestroyMixin,
                  ModelViewSet):
    admin_create_serializer = task_serializers.TaskAdminSerializer
    admin_list_serializer = task_serializers.TaskAdminSerializer
    admin_retrieve_serializer = task_serializers.TaskAdminSerializer
    admin_other_serializer = task_serializers.TaskAdminSerializer
    user_create_serializer = task_serializers.TaskSerializer
    user_list_serializer = task_serializers.TaskSerializer
    user_retrieve_serializer = task_serializers.TaskSerializer
    user_other_serializer = task_serializers.TaskSerializer
    permission_classes = [IsAuthenticated]
    obj_model = Task
    redirect_url = '/api/v1/tasks/'


class RecoveryPriorityViewSet(AbstractSerializerClassMixin,
                              DeletedObjectsQuerysetClassMixin,
                              DeletedUserObjectsMixin,
                              ModelViewSet):
    admin_create_serializer = priority_serializers.AdminDeletedPrioritySerializer
    admin_list_serializer = priority_serializers.AdminDeletedPrioritySerializer
    admin_retrieve_serializer = priority_serializers.AdminDeletedPrioritySerializer
    admin_other_serializer = priority_serializers.AdminDeletedPrioritySerializer
    user_create_serializer = priority_serializers.DeletedPrioritySerializer
    user_list_serializer = priority_serializers.DeletedPrioritySerializer
    user_retrieve_serializer = priority_serializers.DeletedPrioritySerializer
    user_other_serializer = priority_serializers.DeletedPrioritySerializer
    obj_model = Priority
    permission_classes = [IsAuthenticated]


class RecoveryCategoryViewSet(AbstractSerializerClassMixin,
                              DeletedObjectsQuerysetClassMixin,
                              DeletedUserObjectsMixin,
                              ModelViewSet):
    admin_create_serializer = category_serializers.DeletedCategoryAdminSerializer
    admin_list_serializer = category_serializers.DeletedCategoryAdminSerializer
    admin_retrieve_serializer = category_serializers.DeletedCategoryAdminSerializer
    admin_other_serializer = category_serializers.DeletedCategoryAdminSerializer
    user_create_serializer = category_serializers.DeletedCategorySerializer
    user_list_serializer = category_serializers.DeletedCategorySerializer
    user_retrieve_serializer = category_serializers.DeletedCategorySerializer
    user_other_serializer = category_serializers.DeletedCategorySerializer
    obj_model = Category
    permission_classes = [IsAuthenticated]


class RecoveryTaskViewSet(AbstractSerializerClassMixin,
                          DeletedObjectsQuerysetClassMixin,
                          DeletedUserObjectsMixin,
                          ModelViewSet):
    admin_create_serializer = task_serializers.DeletedTaskAdminSerializer
    admin_list_serializer = task_serializers.DeletedTaskAdminSerializer
    admin_retrieve_serializer = task_serializers.DeletedTaskAdminSerializer
    admin_other_serializer = task_serializers.DeletedTaskSerializer
    user_create_serializer = task_serializers.DeletedTaskAdminSerializer
    user_list_serializer = task_serializers.DeletedTaskAdminSerializer
    user_retrieve_serializer = task_serializers.DeletedTaskAdminSerializer
    user_other_serializer = task_serializers.DeletedTaskAdminSerializer
    permission_classes = [IsAuthenticated]
    obj_model = Task
