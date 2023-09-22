from django.db import transaction

from djoser.serializers import UserCreateSerializer, UserSerializer
from .models import CustomUser, Lesson, Product, Watched
from rest_framework import serializers


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        user = super(CustomUserCreateSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class WatchedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watched
        fields = '__all__'

