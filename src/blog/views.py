from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.utils import translation
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from .models import BlogPost
from taggit.models import Tag
from .forms import SetLanguageForm
from django.conf import settings


class FrontpageView(ListView):
    model = BlogPost
    pagenate_by = 10
    template_name = 'frontpage.html'


def feeds(request):
    tags = Tag.objects.all()
    return render(request, 'feeds.html', {
        'tags': tags,
    })


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
        language = "da"
        translation.activate(language)
    except BlogPost.DoesNotExist:
        pass

    ### last chance, is it an english slug?
    if not blogpost:
        blogpost = get_object_or_404(BlogPost, slug_en=slug)
        language = "en"
        translation.activate(language)

    response = render(request, 'blog/blogpost_detail.html', {
        'blogpost': blogpost,
    })
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    return response

@require_POST
def setlang(request):
    """A custom set_language view which permits redirect to other domains."""
    form = SetLanguageForm(request.POST or None)
    if form.is_valid():
        user_language = form.cleaned_data['language']
        translation.activate(user_language)
        response = HttpResponseRedirect(form.cleaned_data['next'])
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_language)
        return response
