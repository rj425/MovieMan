from rest_framework import serializers
from django.contrib.auth.models import User, Group
from app.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):

    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password',
                  'first_name', 'last_name', 'email')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class TaskSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('author','movieCount')


class CastSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Cast
        fields = '__all__'


class MovieSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'


class ActivitySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Activity
        fields = '__all__'
        read_only_fields = ('username',)
