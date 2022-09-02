from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.utils.feedgenerator import Atom1Feed
from .models import BlogPost


class AllBlogPostRssFeed(Feed):
    title = _("UncensoredDNS Blog Posts")
    link = reverse_lazy('blog')
    description = _("Blog posts and system information from UncensoredDNS")

    def items(self):
        return BlogPost.objects.order_by('-created_date')[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body[:250]


class AllBlogPostAtomFeed(AllBlogPostRssFeed):
    feed_type = Atom1Feed
    subtitle = AllBlogPostRssFeed.description
