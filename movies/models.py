from django.db import models
from members.models import Member

 # Create Movie Model
class Movie(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True) # When it was create
    updated_at = models.DateTimeField(auto_now=True) # When i was update
    creator = models.ForeignKey(Member, related_name='movies', on_delete=models.CASCADE)
    #creator = models.ForeignKey('auth.User', related_name='movies', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# Create Todo Model
class Todo(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()

    def __str__(self):
        return self.title

# Create Post Model
class Post(models.Model):
    author = models.ForeignKey(Member, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class SearchQuery(models.Model):
    user = models.ForeignKey(Member, blank=True, null=True, on_delete=models.SET_NULL)
    query = models.CharField(max_length=220)
    timestamp = models.DateTimeField(auto_now_add=True)

