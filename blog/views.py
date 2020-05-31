from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .forms import BlogPostModelForm
from .models import BlogPost
from rest_framework import generics, permissions

@login_required
def blog_post_list_myblogs(request):
    if request.user.is_authenticated:
        my_qs = BlogPost.objects.filter(name=request.name)
        for item in my_qs:
            print ('1. slug=',item.slug)
    template_name = 'blog/new-list.html'
    context = {"title": "myblog-ABC", 'object_list': my_qs}
    return render(request, template_name, context)



def blog_post_list_view(request):
    # list out objects 
    # could be search
    qs = BlogPost.objects.all().published() # queryset -> list of python object
    if request.user.is_authenticated:
        my_qs = BlogPost.objects.filter(user=request.user)
        qs = (qs | my_qs).distinct()
    template_name = 'blog/list.html'
    context = {"title": "blog_post_list_view", 'object_list': qs}
    return render(request, template_name, context) 

#@staff_member_required
@login_required
def blog_post_create_view(request):   #127.0.0.1/blog-new
    # create objects
    # ? use a form
    # request.user -> return something
    form = BlogPostModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        form = BlogPostModelForm()
    template_name = 'form.html'
    context = {'form': form}
    return render(request, template_name, context)  


def blog_post_detail_view(request, slug):
    # 1 object -> detail view
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = 'blog/detail.html'
    context = {"object": obj}
    return render(request, template_name, context)   

#@staff_member_required
@login_required
def blog_post_update_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    form = BlogPostModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    template_name = 'form.html'
    context = {"title": f"Update {obj.title}", "form": form}
    return render(request, template_name, context)  


#@staff_member_required
@login_required
def blog_post_delete_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = 'blog/delete.html'
    if request.method == "POST":
        obj.delete()
        return redirect("/blog")
    context = {"object": obj}
    return render(request, template_name, context)

from .models import Post
from .serializers import PostSerializer
from .permissions import IsAuthorOrReadOnly

class PostList(generics.ListCreateAPIView):
    #permission_classes = (permissions.IsAuthenticated,)  #permissions are already set at settings.py
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = (permissions.IsAuthenticated,)  #permissions are already set at settings.py
    permission_classes = (IsAuthorOrReadOnly,) #overide permissions set at settings.py
    queryset = Post.objects.all()
    serializer_class = PostSerializer









