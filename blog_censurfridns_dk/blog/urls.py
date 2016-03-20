from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
import blog.views
from django.utils.translation import ugettext_lazy as _

urlpatterns = [
    ### admin site
    url(r'^%s/' % settings.ADMIN_PREFIX, include(admin.site.urls)),

    ### i18n
    url(r'^i18n/', include('django.conf.urls.i18n')),

    ### blog
    url(r'^$', blog.views.BlogPostList.as_view(), name='blog'),
    url(r'^blog/(?P<slug>[\w-]+)/$', blog.views.BlogPostDetail.as_view(), name='blogpost_detail'),

    ### tags
    url(r'^tags/(?P<slug>[\w-]+)/$', blog.views.tag_lookup, name='tag_lookup'),

    ### static pages
    url(_(r'^dns-servers/$'), TemplateView.as_view(template_name="static/dns-servers.html"), name='dns_servers'),
    url(_(r'^contact/$'), TemplateView.as_view(template_name="static/contact.html"), name='contact'),
    url(_(r'^about/$'), TemplateView.as_view(template_name="static/about.html"), name='about'),
    url(_(r'^about-me/$'), TemplateView.as_view(template_name="static/about_me.html"), name='about_me'),
]
