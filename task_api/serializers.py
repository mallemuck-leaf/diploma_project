from datetime import datetime
from rest_framework import serializers
from django.contrib.auth.models import User
from task.models import Person, Priority, Category, Task, Status
from account.models import Profile


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
        fields = ['id', 'username', 'is_active']


class UserCreateSerializer(UserDetailSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = { 'password': {'write_only': True}}


class ProfileSerializer(serializers.ModelSerializer):
    user = UserPartialDetailSerializer(read_only=True)
    new_user = UserCreateSerializer(write_only=True)

    class Meta:
        model = Profile
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data.keys())
        user_data = validated_data.pop('new_user')
        user_password = user_data.pop('password')
        user = User(**user_data)
        user.set_password(user_password)
        user.save()
        Profile.objects.create(user=user, **validated_data)
        return user


class PersonSerializer(serializers.ModelSerializer):
    user = UserPartialDetailSerializer()

    class Meta:
        model = Person
        fields = '__all__'


class PersonAdminSerializer(PersonSerializer):
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

    class Meta:
        model = Task
        fields = '__all__'
