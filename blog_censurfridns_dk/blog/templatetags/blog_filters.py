from django import template
from django.core.urlresolvers import resolve, reverse
from django.conf import settings
import CommonMark
from blog.models import BlogPost

register = template.Library()

@register.filter(is_safe=True)
def markdown(input):
    parser = CommonMark.Parser()
    renderer = CommonMark.HtmlRenderer()
    ast = parser.parse(input)
    return renderer.render(ast)


@register.filter
def get_i18n_url(url, lang):
    from_lang, to_lang = lang.split(",")
    match = resolve(url)
    if match.func.func_name == 'blogpost_detail':
        ### handle url translation for blogpost_detail views
        filter = {
            'slug_%s' % from_lang: match.kwargs['slug'],
        }
        blogpost = BlogPost.objects.get(**filter)
        slug = getattr(blogpost, 'slug_%s' % to_lang)
        path = reverse(match.func, kwargs={'slug': slug})
    else:
        path = reverse(match.func, args=match.args, kwargs=match.kwargs)
    return '//' + settings.LANGUAGE_DOMAINS[to_lang] + url

