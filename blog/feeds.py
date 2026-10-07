from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.utils import timezone

from .models import Post


class LatestPostsFeed(Feed):
    title = "My Blog - Latest Posts"
    link = "/"
    description = "Latest posts from My Blog"

    def items(self):
        return Post.objects.filter(
            status=Post.Status.PUBLISHED,
            published_at__lte=timezone.now()
        ).order_by("-published_at")[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content[:200] + "..." if len(item.content) > 200 else item.content

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.published_at

    def item_author_name(self, item):
        return item.author.get_full_name() or item.author.username

class AtomPostsFeed(LatestPostsFeed):
    feed_type = Atom1Feed
    subtitle = "Latest posts from My Blog"
