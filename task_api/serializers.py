from datetime import datetime
from rest_framework import serializers
from django.contrib.auth.models import User
from task.models import Person, Priority, Category, Task, Status


# class MyDefCreateSerializer:
#     user = None
#
#     def create(self, validated_data):
#         print(validated_data)
#         validated_data.update(
#             {
#                 'created_at': datetime.now(),
#                 'created_by': Person.objects.get(user=validated_data.user)
#             }
#         )
#         return super().create(validated_data)


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'email')


class UserDetailForAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'email', 'is_staff', 'is_active')


class PersonListSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = Person
        fields = '__all__'


class PersonAdminListSerializer(serializers.ModelSerializer):
    user = UserDetailForAdminSerializer()

    class Meta:
        model = Person
        fields = '__all__'


class PersonDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = Person
        fields = ['user']


class PersonAdminDetailSerializer(serializers.ModelSerializer):

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

    def create(self, validated_data):
        validated_data['created_at'] = datetime.now()
        validated_data['updated_at'] = datetime.now()
        validated_data['created_by'] = self.request.user
        return super().create(validated_data)


class PriorityForTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Priority
        fields = ['name',]


class PriorityAdminSerializer(serializers.ModelSerializer):
    created_by = PersonAdminDetailSerializer()

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
    created_by = PersonAdminDetailSerializer()

    class Meta:
        model = Category
        fields = ['id', 'created_by', 'name', 'description']


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    priority = PriorityForTaskSerializer()
    category = CategoryForTaskSerializer()
    # status = StatusSerializer()
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'category', 'priority', 'status', 'completed',
                  'completed_at', 'created_at', 'updated_at']
