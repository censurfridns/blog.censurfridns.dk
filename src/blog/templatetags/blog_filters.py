from django import template
from django.urls import resolve, reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import translation
from blog.models import BlogPost
import commonmark
from taggit.models import Tag

register = template.Library()

@register.filter(is_safe=True)
def markdown(input):
    parser = commonmark.Parser()
    renderer = commonmark.HtmlRenderer()
    ast = parser.parse(input)
    return renderer.render(ast)


@register.filter
def get_i18n_url(url, lang):
    ### parse languages from arg
    from_lang, to_lang = lang.split(",")

    ### resolve url to ResolverMatch object
    match = resolve(url)

    ### handle blogpost_detail and tag_lookup views differently
    if match.view_name == 'blogpost_detail' or match.view_name == 'tag_lookup':
        ### create a filter to find the blogpost from the current url
        filter = {
            'slug_%s' % from_lang: match.kwargs['slug'],
        }
        if match.view_name == 'blogpost_detail':
            blogpost = BlogPost.objects.get(**filter)

            ### get slug for this blogpost in the new language
            slug = getattr(blogpost, 'slug_%s' % to_lang)
        elif match.view_name == 'tag_lookup':
            tag = Tag.objects.get(**filter)
            
            ### get slug for this tag in the new language
            slug = getattr(tag, 'slug_%s' % to_lang)

        ### get url for this object with the slug in the new language
        with translation.override(to_lang):
            path = reverse(match.func, kwargs={'slug': slug})
    else:
        with translation.override(to_lang):
            path = reverse(match.func, args=match.args, kwargs=match.kwargs)

    ### return absolute url unless we are in DEBUG mode,
    ### then only return relative url
    if settings.DEBUG:
        return path
    else:
        return 'https://' + settings.PRIMARY_LANGUAGE_DOMAINS[to_lang] + path

