from django.contrib import admin
from django.apps import apps
from modeltranslation.admin import TranslationAdmin
from .models import BlogPost

class BlogAdmin(TranslationAdmin):
    pass

admin.site.register(BlogPost, BlogAdmin)