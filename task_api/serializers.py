from datetime import datetime
from rest_framework import serializers
from django.contrib.auth.models import User
from task.models import Person, Priority, Category, Task, Status


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'email')


class UserDetailForAdminSerializer(UserDetailSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserPartialDetailSerializer(UserDetailSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class PersonListSerializer(serializers.ModelSerializer):
    user = UserPartialDetailSerializer()

    class Meta:
        model = Person
        fields = '__all__'


class PersonAdminListSerializer(PersonListSerializer):
    user = UserPartialDetailSerializer()

    class Meta:
        model = Person
        fields = '__all__'


class PersonDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = Person
        fields = ['user']


class PersonAdminDetailSerializer(PersonDetailSerializer):
    user = UserDetailForAdminSerializer()

    class Meta:
        model = Person
        fields = ['user']


class PersonAdminPartialDetailSerializer(PersonDetailSerializer):
    user = UserPartialDetailSerializer()

    class Meta:
        model = Person
        fields = ['user']


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


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    priority = PriorityForTaskSerializer(read_only=True)
    priority_id = serializers.SlugRelatedField(write_only=True,
                                               slug_field='id',
                                               queryset=Priority.objects,
                                               required=False)
    category = CategoryForTaskSerializer(read_only=True)
    category_id = serializers.SlugRelatedField(write_only=True,
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


class TaskAdminSerializer(TaskSerializer):
    user = PersonAdminPartialDetailSerializer()

    class Meta:
        model = Task
        fields = '__all__'
