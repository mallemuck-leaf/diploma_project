from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAdminOrUserIDOnly
from task.models import Person, Task
from .serializers import (
    PersonListSerializer, PersonDetailSerializer
)
from .mixins import SerializerPersonMixin


class PersonViewSet(SerializerPersonMixin, ModelViewSet):
    queryset = Person.objects.all()
    permission_classes = [IsAdminOrUserIDOnly]


# class TaskViewSet(SerializerPersonMixin, ModelViewSet):
#     queryset = Task.objects.all()
#     permission_classes = [IsAdminOrUserIDOnly]
