from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from task.models import Person
from .serializers import (
    PersonListSerializer, PersonDetailSerializer
)
from .mixins import SerializerClassMixin


class PersonViewSet(SerializerClassMixin, ModelViewSet):
    serializer_class = PersonListSerializer
    serializer_list_class = PersonListSerializer
    serializer_detail_class = PersonDetailSerializer
    queryset = Person.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
