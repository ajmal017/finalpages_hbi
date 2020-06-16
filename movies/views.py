from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from django.shortcuts import render
from .models import Movie
from .permissions import IsOwnerOrReadOnly, IsAuthenticated
from .serializers import MovieSerializer
from .pagination import CustomPagination

class get_delete_update_movie(RetrieveUpdateDestroyAPIView):
    serializer_class = MovieSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def get_queryset(self, pk):
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            content = {
                'status': 'Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return movie

    # Get a movie
    def get(self, request, pk):

        movie = self.get_queryset(pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update a movie
    def put(self, request, pk):
        
        movie = self.get_queryset(pk)

        if(request.user == movie.creator): # If creator is who makes request
            serializer = MovieSerializer(movie, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            content = {
                'status': 'UNAUTHORIZED'
            }
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)

    # Delete a movie
    def delete(self, request, pk):

        movie = self.get_queryset(pk)

        if(request.user == movie.creator): # If creator is who makes request
            movie.delete()
            content = {
                'status': 'NO CONTENT'
            }
            return Response(content, status=status.HTTP_204_NO_CONTENT)
        else:
            content = {
                'status': 'UNAUTHORIZED'
            }
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)
   

class get_post_movies(ListCreateAPIView):
    serializer_class = MovieSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    
    def get_queryset(self):
       movies = Movie.objects.all()
       return movies

    # Get all movies
    def get(self, request):
        movies = self.get_queryset()
        paginate_queryset = self.paginate_queryset(movies)
        serializer = self.serializer_class(paginate_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    # Create a new movie
    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from .models import Todo
from .serializers import TodoSerializer
from rest_framework import generics


class ListTodo(generics.ListAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


class DetailTodo(generics.RetrieveAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


from rest_framework import generics

from .models import Post
from .permissions import PostIsAuthorOrReadOnly
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (PostIsAuthorOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

from .models import SearchQuery

def search_view(request):
    query = request.GET.get('q', None)
    user = None
    if request.user.is_authenticated:
        user = request.user
    context =  {"query": query}
    if query is not None:
        SearchQuery.objects.create(user=user, query=query)
        blog_list = Movie.objects.search(query=query)
        context['blog_list'] = blog_list
    return render(request, 'searches/view.html',context)

