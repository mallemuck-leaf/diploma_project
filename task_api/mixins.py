from .serializers import (
    PersonDetailSerializer, PersonListSerializer, PersonAdminListSerializer, PersonAdminDetailSerializer,
)


class SerializerPersonMixin:
    def get_serializer_class(self):
        if self.request.user.is_staff:
            if self.action == 'create':
                return PersonAdminDetailSerializer
            elif self.action == 'retrieve':
                return PersonAdminDetailSerializer
            elif self.action == 'list':
                return PersonAdminListSerializer
            return PersonAdminDetailSerializer
        else:
            if self.action == 'create':
                return PersonDetailSerializer
            elif self.action == 'retrieve':
                return PersonDetailSerializer
            elif self.action == 'list':
                return PersonListSerializer
        # return super().get_serializer_class()
            return PersonDetailSerializer

class SerializerTaskMixin:
    def get_serializer_class(self):
        pass
