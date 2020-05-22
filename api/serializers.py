# api/serializers.py
from rest_framework import serializers
from .models import Todo

from blog.models import BlogPost
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ('title', 'content', 'user')

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'body',)