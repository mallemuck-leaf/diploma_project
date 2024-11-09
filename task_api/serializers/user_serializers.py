from django.contrib.auth.models import User
from rest_framework import serializers


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
        extra_kwargs = {'password': {'write_only': True}}