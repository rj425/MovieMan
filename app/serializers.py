from rest_framework import serializers
from app.models import Task, Movie, Cast


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class CastSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cast
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'
