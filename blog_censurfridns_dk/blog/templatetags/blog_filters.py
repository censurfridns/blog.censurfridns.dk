from django import template
from django.core.urlresolvers import resolve, reverse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import translation
from blog.models import BlogPost
import CommonMark

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

    ### handle blogpost_detail view differently
    if match.view_name == 'blogpost_detail':
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
        with translation.override(to_lang):
            path = reverse(match.func, args=match.args, kwargs=match.kwargs)
    
    if settings.DEBUG:
        return path
    else:
        return 'https://' + settings.PRIMARY_LANGUAGE_DOMAINS[to_lang] + path

