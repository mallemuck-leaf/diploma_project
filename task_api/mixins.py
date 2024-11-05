from datetime import datetime
from django.shortcuts import redirect
from task.models import Person


class AbstractSerializerClassMixin:
    admin_create_serializer = None
    admin_retrieve_serializer = None
    admin_list_serializer = None
    admin_other_serializer = None
    user_create_serializer = None
    user_retrieve_serializer = None
    user_list_serializer = None
    user_other_serializer = None
    serializer_classes = {
        'admin': {
            'create': admin_create_serializer,
            'retrieve': admin_retrieve_serializer,
            'list': admin_list_serializer,
            'else': admin_other_serializer
        },
        'user': {
            'create': user_create_serializer,
            'retrieve': user_retrieve_serializer,
            'list': user_list_serializer,
            'else': user_other_serializer,
        }
    }
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


# class AbstractCreateMixin:
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer['created_at'] = datetime.now()
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PersonQuerysetClassMixin:

    def get_queryset(self):
        if self.request.user.is_staff:
            return Person.objects.all()
        else:
            return Person.objects.filter(user=self.request.user)

