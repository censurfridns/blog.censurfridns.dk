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
    ### parse languages from arg
    from_lang, to_lang = lang.split(",")

    ### resolve url to ResolverMatch object
    match = resolve(url)

    if match.func.func_name == 'blogpost_detail':
        ### create a filter to find the blogpost from the current url
        filter = {
            'slug_%s' % from_lang: match.kwargs['slug'],
        }
        blogpost = BlogPost.objects.get(**filter)
        ### get slug for this blogpost in the new language
        slug = getattr(blogpost, 'slug_%s' % to_lang)
        ### get url for this blogpost with the slug in the new language
        path = reverse(match.func, kwargs={'slug': slug})
    else:
        path = reverse(match.func, args=match.args, kwargs=match.kwargs)
    if settings.DEBUG:
        return path
    else:
        return 'https://' + settings.LANGUAGE_DOMAINS[to_lang] + path

