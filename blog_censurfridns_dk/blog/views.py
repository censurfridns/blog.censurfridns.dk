from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.utils import translation
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from .models import BlogPost
from .forms import SetLanguageForm
from taggit.models import Tag


def frontpage(request):
    latest_blogposts = BlogPost.objects.all()[:10]
    return render(request, 'frontpage.html', {
        'blogposts': latest_blogposts,
    })


def feeds(request):
    tags = Tag.objects.all()
    return render(request, 'feeds.html', {
        'tags': tags,
    })


@require_POST
def setlang(request):
    form = SetLanguageForm(request.POST or None)
    if form.is_valid():
        user_language = form.cleaned_data['language']
        translation.activate(user_language)
        request.session[translation.LANGUAGE_SESSION_KEY] = user_language
        return HttpResponseRedirect(form.cleaned_data['next'])


def tag_lookup(request, slug):
    try:
        tag = Tag.objects.get(slug=slug)
    except Tag.DoesNotExist:
        tag = None

    blogposts = BlogPost.objects.filter(tags__slug=slug)
    return render(request, 'tag_lookup.html', {
        'blogposts': blogposts,
        'tag': tag,
        'slug': slug,
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

