from django.db import models
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.conf import settings
from taggit.managers import TaggableManager


class BlogPost(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    body = models.TextField()
    slug = models.SlugField(blank=True, max_length=100)
    tags = TaggableManager()

    class Meta:
        ordering = ['-created_date']

    def __unicode__(self):
        return unicode(self.title)

    def get_absolute_url(self):
        return reverse('blogpost_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        ### set/update slugs for all enabled languages
        for code, language in settings.LANGUAGES:
            setattr(self, 'slug_%s' % code, slugify(getattr(self, 'title_%s' % code)))
        ### save forreal
        super(BlogPost, self).save(*args, **kwargs)

