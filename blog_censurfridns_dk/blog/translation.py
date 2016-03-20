from modeltranslation.translator import register, TranslationOptions
from .models import BlogPost
from taggit.models import Tag


@register(BlogPost)
class BlogPostTranslationOptions(TranslationOptions):
    fields = ('title', 'body', 'slug')
    required_languages = ('en', 'da')


@register(Tag)
class TaggitTranslations(TranslationOptions):
    fields = ('name',)
    required_languages = ('en', 'da')

