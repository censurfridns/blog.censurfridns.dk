from django.views.generic import ListView, DetailView
from django.shortcuts import render
from .models import BlogPost
from taggit.models import Tag

def tag_lookup(request, slug):
    try:
        tag = Tag.objects.get(slug=slug)
    except Tag.DoesNotExist:
        tag = None

    blogposts = BlogPost.objects.filter(tags__slug=slug)
    return render(request, 'tag_lookup.html', {
        'blogposts': blogposts,
        'tag': tag,
    })


class BlogPostList(ListView):
    queryset = BlogPost.objects.all()
    paginate_by = 25


class BlogPostDetail(DetailView):
    model = BlogPost


