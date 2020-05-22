# api/views.py
from rest_framework import generics
from .models import Todo
from .serializers import TodoSerializer, BookSerializer
from blog.models import BlogPost

class notused_BookAPIView(generics.ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BookSerializer

class notused_ListTodo(generics.ListAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


class notused_DetailTodo(generics.RetrieveAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
