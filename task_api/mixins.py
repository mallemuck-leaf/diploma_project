from datetime import datetime
from django.shortcuts import redirect
from task.models import Person
from .serializers import (
    PersonDetailSerializer, PersonListSerializer, PersonAdminListSerializer, PersonAdminDetailSerializer,
    PrioritySerializer, PriorityAdminSerializer,
    CategorySerializer, CategoryAdminSerializer,
    TaskSerializer,
)

ACTIONS = ('create', 'retrieve', 'list')


class AbstractMixin:
    serializer_classes = None
    actions = None

    def get_serializer_class(self):
        if self.request.user.is_staff:
            if self.action in self.actions:
                return self.serializer_classes['admin'][self.action]
            else:
                return self.serializer_classes['admin']['else']
        else:
            if self.action in self.actions:
                return self.serializer_classes['user'][self.action]
            else:
                return self.serializer_classes['user']['else']


class AbstractQuerysetClassMixin:
    obj_model = None

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.obj_model.objects.filter(deleted_at=None,
                                                 deleted=None)
        else:
            person_user = Person.objects.get(user=self.request.user)
            return self.obj_model.objects.filter(created_by=person_user,
                                                 deleted_at=None,
                                                 deleted=None)


class AbstractDestroyMixin:
    obj_model = None
    redirect_url = None

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        deleteting_obj = self.obj_model.objects.filter(id=instance.id)
        if self.request.user.is_staff:
            deleteting_obj.update(deleted=datetime.now())
        else:
            deleteting_obj.update(deleted_at=datetime.now())
        return redirect(f'{self.redirect_url}')


class PersonQuerysetClassMixin:

    def get_queryset(self):
        if self.request.user.is_staff:
            return Person.objects.all()
        else:
            return Person.objects.filter(user=self.request.user)


class SerializerPersonMixin(AbstractMixin):
    serializer_classes = {
        'admin': {
            'create': PersonAdminDetailSerializer,
            'retrieve': PersonAdminDetailSerializer,
            'list': PersonAdminListSerializer,
            'else': PersonAdminDetailSerializer
        },
        'user': {
            'create': PersonDetailSerializer,
            'retrieve': PersonDetailSerializer,
            'list': PersonListSerializer,
            'else': PersonDetailSerializer,
        }
    }
    actions = ACTIONS


class SerializerPriorityMixin(AbstractMixin):
    serializer_classes = {
        'admin': {
            'else': PriorityAdminSerializer
        },
        'user': {
            'else': PrioritySerializer
        }
    }
    actions = ()


class SerializerCategoryMixin(AbstractMixin):
    serializer_classes = {
        'admin': {
            'else': CategoryAdminSerializer
        },
        'user': {
            'else': CategorySerializer
        }
    }
    actions = ()


class SerializerTaskMixin(AbstractMixin):
    serializer_classes = {
        'admin': {
            'create': PersonAdminDetailSerializer,
            'retrieve': PersonAdminDetailSerializer,
            'list': PersonAdminListSerializer,
            'else': PersonAdminDetailSerializer
        },
        'user': {
            'create': PersonDetailSerializer,
            'retrieve': PersonDetailSerializer,
            'list': PersonListSerializer,
            'else': TaskSerializer
        }
    }
    actions = ()
