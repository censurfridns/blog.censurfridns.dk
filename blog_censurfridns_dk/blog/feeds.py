from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.utils.feedgenerator import Atom1Feed
from .models import BlogPost

class BlogPostRssFeed(Feed):
    title = _("UncensoredDNS Blog Posts")
    link = reverse_lazy('blog')
    description = _("Blog posts and system information from UncensoredDNS")

    def items(self):
        return BlogPost.objects.order_by('-created_date')[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description


class BlogPostAtomFeed(BlogPostRssFeed):
    feed_type = Atom1Feed
    subtitle = BlogPostRssFeed.description

