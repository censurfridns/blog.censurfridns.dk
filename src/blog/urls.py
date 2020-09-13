from django.urls import reverse_lazy
from django.urls import include, path
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from .feeds import AllBlogPostRssFeed, AllBlogPostAtomFeed, TagBlogPostRssFeed, TagBlogPostAtomFeed
import blog.views


urlpatterns = [
    ### admin site
    path('%s/' % settings.ADMIN_PREFIX, admin.site.urls),

    ### i18n
    path('i18n/', include('django.conf.urls.i18n')),

    ### frontpage
    path('', blog.views.FrontpageView.as_view(), name='frontpage'),

    ### blog
    path('blog/', blog.views.BlogPostList.as_view(), name='blog'),
    path('blog/<slug:slug>/', blog.views.blogpost_detail, name='blogpost_detail'),

    ### tags
    path(_('tags/<slug:slug>/'), blog.views.tag_lookup, name='tag_lookup'),

    ### syndication
    path(_('feeds/rss/all/'), AllBlogPostRssFeed(), name='allrssfeed'),
    path(_('feeds/atom/all/'), AllBlogPostAtomFeed(), name='allatomfeed'),
    path(_('feeds/rss/tag/<slug:slug>'), TagBlogPostRssFeed(), name='tagrssfeed'),
    path(_('feeds/atom/tag/<slug:slug>'), TagBlogPostAtomFeed(), name='tagatomfeed'),
    path(_('feeds/'), blog.views.feeds, name='feeds'),

    ### old rss feed url redirects
    path('en/taxonomy/term/4/0/feed', RedirectView.as_view(url=reverse_lazy('tagrssfeed', kwargs={'slug': 'system-status'}))),
    path('en/rss.xml', RedirectView.as_view(url=reverse_lazy('allrssfeed'))),
    path('taxonomy/term/2/0/feed', RedirectView.as_view(url=reverse_lazy('tagrssfeed', kwargs={'slug': 'driftinfo'}))),
    path('rss.xml', RedirectView.as_view(url=reverse_lazy('allrssfeed'))),

    ### static pages
    path(_('dns-servers/'), TemplateView.as_view(template_name="dns-servers.html"), name='dns_servers'),
    path(_('contact/'), TemplateView.as_view(template_name="contact.html"), name='contact'),
    path(_('faq/'), TemplateView.as_view(template_name="faq.html"), name='faq'),
    path(_('about/'), TemplateView.as_view(template_name="about.html"), name='about'),
]
