from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Movie, Todo, Post, SearchQuery

class CustomMovieAdmin(admin.ModelAdmin):
    model = Movie
    list_display = ('id', 'title', 'creator', 'genre', 'year', )

admin.site.register(Movie, CustomMovieAdmin)
admin.site.register(Todo)
admin.site.register(Post)
admin.site.register(SearchQuery)
