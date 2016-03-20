from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.utils import translation
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


def blogpost_detail(request, slug):
    ### initialize empty var
    blogpost = None

    ### is this a danish slug?
    try:
        blogpost = BlogPost.objects.get(slug_da=slug)
        translation.activate('da')
        request.session[translation.LANGUAGE_SESSION_KEY] = 'da'
    except BlogPost.DoesNotExist:
        pass

    ### last chance, is it an english slug?
    if not blogpost:
        blogpost = get_object_or_404(BlogPost, slug_en=slug)
        translation.activate('en')
        request.session[translation.LANGUAGE_SESSION_KEY] = 'en'

    return render(request, 'blog/blogpost_detail.html', {
        'blogpost': blogpost,
    })

