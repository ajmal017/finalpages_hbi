from django.urls import include, path, re_path
from . import views


urlpatterns = [
    # Url to get update or delete a movie
    #re_path(r'^api/v1/movies/(?P<pk>[0-9]+)$', views.get_delete_update_movie.as_view(), name='get_delete_update_movie'),
    # urls list all and create new one
    #path('api/v1/movies/', views.get_post_movies.as_view(), name='get_post_movies')
]