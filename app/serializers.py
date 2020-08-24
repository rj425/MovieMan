from rest_framework import serializers
from django.contrib.auth.models import User, Group
from app.models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('movieCount',)


class CastSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cast
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'


class ActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = '__all__'