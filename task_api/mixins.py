from datetime import datetime
from django.shortcuts import redirect
from rest_framework.response import Response
from django.contrib.auth.models import User
from task.models import Person


class AbstractSerializerClassMixin:
    '''
    Class for selecting serializers for actions
    '''
    admin_create_serializer = None
    admin_retrieve_serializer = None
    admin_list_serializer = None
    admin_other_serializer = None
    user_create_serializer = None
    user_retrieve_serializer = None
    user_list_serializer = None
    user_other_serializer = None
    actions = ('create', 'retrieve', 'list')

    def get_serializer_class(self):
        if self.request.user.is_staff:
            serializer_classes = {
                    'create': self.admin_create_serializer,
                    'retrieve': self.admin_retrieve_serializer,
                    'list': self.admin_list_serializer,
                    'else': self.admin_other_serializer
            }
            if self.action in self.actions:
                return serializer_classes[self.action]
            else:
                return serializer_classes['else']
        else:
            serializer_classes = {
                'create': self.user_create_serializer,
                'retrieve': self.user_retrieve_serializer,
                'list': self.user_list_serializer,
                'else': self.user_other_serializer,
            }
            if self.action in self.actions:
                return serializer_classes[self.action]
            else:
                return serializer_classes['else']


class AbstractQuerysetClassMixin:
    '''
    Class for selecting model objects for viewset.
    '''
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


class DeletedObjectsQuerysetClassMixin:
    '''
    Class for selecting deleting model objects for viewset.
    '''
    obj_model = None

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.obj_model.objects.all().exclude(deleted_at=None, deleted=None)
        else:
            person_user = Person.objects.get(user=self.request.user)
            return self.obj_model.objects.filter(created_by=person_user, deleted=None).exclude(deleted_at=None)


class AbstractDestroyMixin:
    '''
    Marking deleting objects as deleted.
    '''
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


class UserDestroyMixin:
    '''
    Marking deleting user as not active.
    '''
    def destroy(self, request, pk=None, *args, **kwargs):
        if request.user.is_staff:
            user = User.objects.get(id=pk)
            user.is_active = False
            user.save()
            return Response(status=204)
        else:
            request.user.is_active = False
            request.user.save()
            return Response(status=204)


class AbstractCreateMixin:
    '''
    Creating new object
    '''

    def perform_create(self, serializer):
        serializer.save(created_by=Person.objects.get(user=self.request.user),
                        created_at=datetime.now(),
                        updated_at=datetime.now())


class AbstractUpdateMixin:
    '''
    adding a change datetime when updating object
    '''

    def perform_update(self, serializer):
        # instance = self.get_object()
        if self.request.user.is_authenticated:
            serializer.save(updated_at=datetime.now())


class PersonQuerysetClassMixin:
    '''
    selecting person objects for user list
    for user - only user object
    for admin - all users
    '''

    def get_queryset(self):
        # print(self.request.user)
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return Person.objects.all()
            else:
                return Person.objects.filter(user=self.request.user)
        else:
            return Person.objects.filter(id=0)


class DeletedUserObjectsMixin:
    '''
    Marking deleting objects ad deleted for user
    '''

    def perform_destroy(self, instance):
        instance.deleted = datetime.now()
        instance.save()
