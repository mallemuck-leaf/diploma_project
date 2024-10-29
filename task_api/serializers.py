from rest_framework import serializers
from django.contrib.auth.models import User
from task.models import Person, Priority, Category, Task, Status


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


class PersonDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = Person
        fields = ['user']

