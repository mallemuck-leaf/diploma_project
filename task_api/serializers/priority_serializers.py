from rest_framework import serializers
from task.models import Priority
from task_api.serializers.person_serializers import PersonAdminPartialDetailSerializer


class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ['id', 'name']


class DeletedPrioritySerializer(PrioritySerializer):
    class Meta:
        model = Priority
        fields = ['id', 'name', 'deleted_at']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.deleted_at = None
        instance.save()
        return instance


class AdminDeletedPrioritySerializer(DeletedPrioritySerializer):
    class Meta:
        model = Priority
        fields = ['id', 'created_by', 'name', 'deleted_at', 'deleted']

    def update(self, instance, validated_data):
        instance.deleted = None
        super().update(instance, validated_data)
        return instance


class PriorityPostSerializer(serializers.ModelSerializer):
    '''
    Serializer for tests
    '''
    created_at = serializers.DateTimeField(write_only=True)
    # updated_at = serializers.DateTimeField(write_only=True)
    # created_by = serializers.IntegerField(write_only=True)

    class Meta:
        model = Priority
        fields = ['id', 'name', 'updated_at', 'created_by', 'created_at']


class PriorityForTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ['name',]


class PriorityAdminSerializer(serializers.ModelSerializer):
    created_by = PersonAdminPartialDetailSerializer(read_only=True)

    class Meta:
        model = Priority
        fields = ['id', 'created_by', 'name']
