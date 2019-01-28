from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from taggit.managers import TaggableManager


class BlogPost(models.Model):
    created_date = models.DateTimeField(null=True, blank=True)
    modified_date = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=100)
    body = models.TextField()
    slug = models.SlugField(blank=True, max_length=100)
    tags = TaggableManager()

    class Meta:
        ordering = ['-created_date']

    def __unicode__(self):
        return unicode(self.title_en)

    def get_absolute_url(self):
        return reverse('blogpost_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.pk is None:
            ### save to make sure we have an id (needed for the slug)
            super(BlogPost, self).save(*args, **kwargs)
            if not self.created_date:
                ### no created_date was specified in the form, set it to now()
                self.created_date = timezone.now()

        ### set/update slugs for all enabled languages
        for code, language in settings.LANGUAGES:
            setattr(self, 'slug_%s' % code, '%s-%s' % (self.id, slugify(getattr(self, 'title_%s' % code))))

        ### update modified_date
        self.modified_date = timezone.now()

        ### save
        super(BlogPost, self).save(*args, **kwargs)

