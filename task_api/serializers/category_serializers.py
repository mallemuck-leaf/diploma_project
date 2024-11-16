from rest_framework import serializers
from task_api.serializers import person_serializers
from task.models import Category
from task_api.serializers.person_serializers import PersonAdminPartialDetailSerializer


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class DeletedCategorySerializer(CategorySerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'deleted_at']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.deleted_at = None
        instance.save()
        return instance


class DeletedCategoryAdminSerializer(DeletedCategorySerializer):
    created_by = person_serializers.PersonAdminPartialDetailSerializer(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'created_by', 'name', 'description', 'deleted_at', 'deleted']

    def update(self, instance, validated_data):
        instance.deleted = None
        super().update(instance, validated_data)
        return instance


class CategoryForTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name',]


class CategoryAdminSerializer(serializers.ModelSerializer):
    created_by = PersonAdminPartialDetailSerializer(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'created_by', 'name', 'description', 'updated_at']
