from rest_framework import serializers
from .models import Movie, Todo, Post
from django.contrib.auth.models import User


class MovieSerializer(serializers.ModelSerializer):  # create class to serializer model
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Movie
        fields = ('id', 'title', 'genre', 'year', 'creator')


class UserSerializer(serializers.ModelSerializer):  # create class to serializer usermodel
    movies = serializers.PrimaryKeyRelatedField(many=True, queryset=Movie.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'movies')

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'body',)

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'author', 'title', 'body', 'created_at',)
        model = Post
