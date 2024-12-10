from datetime import datetime
from rest_framework import serializers
from task.models import Task, Status, Priority, Category, Person
from task_api.serializers.category_serializers import CategoryForTaskSerializer
from task_api.serializers.priority_serializers import PriorityForTaskSerializer
from task_api.serializers.person_serializers import PersonAdminPartialDetailSerializer


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class SlugRelatedFieldForTask(serializers.SlugRelatedField):
    '''
    Queryset for view only user's priorities and categories. For admin - all objects.
    '''
    def get_queryset(self):
        request = self.context.get('request')
        if request.user.is_staff:
            queryset = self.queryset.filter(deleted=None, deleted_at=None)
        else:
            person = Person.objects.get(user=request.user)
            queryset = self.queryset.filter(created_by=person, deleted=None, deleted_at=None)
        return queryset


class TaskSerializer(serializers.ModelSerializer):
    priorities = None
    categories = None
    priority = PriorityForTaskSerializer(read_only=True)
    priority_id = SlugRelatedFieldForTask(write_only=True,
                                          slug_field='id',
                                          queryset=Priority.objects,
                                          required=False)
    category = CategoryForTaskSerializer(read_only=True)
    category_id = SlugRelatedFieldForTask(write_only=True,
                                          slug_field='id',
                                          queryset=Category.objects,
                                          required=False)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'category', 'priority', 'status', 'completed',
                  'completed_at', 'created_at', 'updated_at', 'priority_id', 'category_id']

    def create(self, validated_data):
        priority_id = validated_data.pop('priority_id')
        category_id = validated_data.pop('category_id')
        task_object = Task.objects.create(**validated_data,
                                          priority=priority_id,
                                          category=category_id)
        return task_object

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.completed = validated_data.get('completed', instance.completed)
        instance.completed_at = validated_data.get('completed_at', instance.completed_at)
        instance.updated = datetime.now()
        instance.priority = validated_data.get('priority_id', instance.priority)
        instance.category = validated_data.get('category_id', instance.category)
        instance.save()
        return instance


class DeletedTaskSerializer(TaskSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'category', 'priority', 'status', 'completed',
                  'completed_at', 'created_at', 'updated_at', 'priority_id', 'category_id']

    def update(self, instance, validated_data):
        instance.deleted_at = None
        instance.save()
        super().update(instance, validated_data)
        return instance


class TaskAdminSerializer(TaskSerializer):
    created_by = PersonAdminPartialDetailSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'


class DeletedTaskAdminSerializer(DeletedTaskSerializer):
    created_by = PersonAdminPartialDetailSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.deleted = None
        instance.save()
        super().update(instance, validated_data)
        return instance
