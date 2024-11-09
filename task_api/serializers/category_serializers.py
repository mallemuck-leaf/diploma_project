from rest_framework import serializers
from task.models import Category
from task_api.serializers.person_serializers import PersonAdminPartialDetailSerializer


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class CategoryForTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name',]


class CategoryAdminSerializer(serializers.ModelSerializer):
    created_by = PersonAdminPartialDetailSerializer(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'created_by', 'name', 'description', 'updated_at']
