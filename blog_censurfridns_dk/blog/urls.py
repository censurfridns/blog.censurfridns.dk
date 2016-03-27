from django.core.urlresolvers import reverse_lazy
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from .feeds import AllBlogPostRssFeed, AllBlogPostAtomFeed, TagBlogPostRssFeed, TagBlogPostAtomFeed
import blog.views


urlpatterns = [
    ### admin site
    url(r'^%s/' % settings.ADMIN_PREFIX, include(admin.site.urls)),

    ### i18n
    #url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^i18n/setlang/', blog.views.setlang, name='set_language'),

    ### search
    #url(_(r'^search/'), include('haystack.urls')),

    ### frontpage
    url(r'^$', blog.views.frontpage, name='frontpage'),

    ### blog
    url(r'^blog/$', blog.views.BlogPostList.as_view(), name='blog'),
    url(r'^blog/(?P<slug>[\w-]+)/$', blog.views.blogpost_detail, name='blogpost_detail'),

    ### tags
    url(_(r'^tags/(?P<slug>[\w-]+)/$'), blog.views.tag_lookup, name='tag_lookup'),

    ### syndication
    url(_(r'^feeds/rss/all/$'), AllBlogPostRssFeed(), name='allrssfeed'),
    url(_(r'^feeds/atom/all/$'), AllBlogPostAtomFeed(), name='allatomfeed'),
    url(_(r'^feeds/rss/tag/(?P<slug>[\w-]+)/$'), TagBlogPostRssFeed(), name='tagrssfeed'),
    url(_(r'^feeds/atom/tag/(?P<slug>[\w-]+)/$'), TagBlogPostAtomFeed(), name='tagatomfeed'),

    ### old rss feed url redirects
    url(r'^en/taxonomy/term/4/0/feed', RedirectView.as_view(url=reverse_lazy('tagrssfeed', kwargs={'slug': 'system-status'}))),
    url(r'^en/rss.xml', RedirectView.as_view(url=reverse_lazy('allrssfeed'))),
    url(r'^taxonomy/term/2/0/feed', RedirectView.as_view(url=reverse_lazy('tagrssfeed', kwargs={'slug': 'driftinfo'}))),
    url(r'^rss.xml', RedirectView.as_view(url=reverse_lazy('allrssfeed'))),

    ### static pages
    url(_(r'^dns-servers/$'), TemplateView.as_view(template_name="static/dns-servers.html"), name='dns_servers'),
    url(_(r'^contact/$'), TemplateView.as_view(template_name="static/contact.html"), name='contact'),
    url(_(r'^faq/$'), TemplateView.as_view(template_name="static/faq.html"), name='faq'),
    url(_(r'^about/$'), TemplateView.as_view(template_name="static/about.html"), name='about'),
]
