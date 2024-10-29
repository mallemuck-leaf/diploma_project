from .serializers import PersonDetailSerializer, PersonListSerializer


class SerializerClassMixin:

    serializer_create_class = None
    serializer_detail_class = None
    serializer_list_class = None

    def get_serializer_class(self):
        if self.action == 'create':
            return PersonDetailSerializer
        elif self.action == 'retrieve':
            return PersonDetailSerializer
        elif self.action == 'list':
            return PersonListSerializer
        return super().get_serializer_class()
