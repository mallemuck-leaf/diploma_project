from rest_framework import serializers
from task.models import Priority
from task_api.serializers.person_serializers import PersonAdminPartialDetailSerializer


class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ['id', 'name']


class PriorityPostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(write_only=True)
    updated_at = serializers.DateTimeField(write_only=True)
    created_by = serializers.IntegerField(write_only=True)

    class Meta:
        model = Priority
        fields = ['id', 'name']


class PriorityForTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ['name',]


class PriorityAdminSerializer(serializers.ModelSerializer):
    created_by = PersonAdminPartialDetailSerializer(read_only=True)

    class Meta:
        model = Priority
        fields = ['id', 'created_by', 'name']
