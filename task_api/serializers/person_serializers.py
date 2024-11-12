from django.contrib.auth.models import User
from rest_framework import serializers
from account.models import Profile
from task.models import Person
from task_api.serializers.user_serializers import (
    UserPartialDetailSerializer, UserDetailSerializer, UserDetailForAdminSerializer, UserCreateSerializer
)


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

    def update(self, instance, validated_data):
        user_data = validated_data.get('user', None)
        # instance = self.get_object()
        # print(instance, validated_data)
        instance.user.first_name = user_data['first_name']
        instance.user.last_name = user_data['last_name']
        instance.user.email = user_data['email']
        instance.user.is_active = True if user_data['is_active'] else False
        instance.user.is_staff = True if user_data['is_staff'] else False
        instance.user.save()
        instance.save()
        return instance


class PersonAdminPartialDetailSerializer(PersonDetailSerializer):
    user = UserPartialDetailSerializer()

    class Meta:
        model = Person
        fields = ['user']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserPartialDetailSerializer(read_only=True)
    new_user = UserCreateSerializer(write_only=True)

    class Meta:
        model = Profile
        fields = '__all__'

    def create(self, validated_data):
        # print(validated_data.keys())
        user_data = validated_data.pop('new_user')
        user_password = user_data.pop('password')
        user = User(**user_data)
        user.set_password(user_password)
        user.save()
        Profile.objects.create(user=user, **validated_data)
        return user


