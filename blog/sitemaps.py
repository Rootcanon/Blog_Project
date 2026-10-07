from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone

from .models import Post, Category


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Post.objects.filter(
            status=Post.Status.PUBLISHED,
            published_at__lte=timezone.now()
        )

    def lastmod(self, obj):
        return obj.published_at or obj.created_at

    def location(self, obj):
        return obj.get_absolute_url()


class CategorySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.6

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        latest = obj.posts.filter(
            status=Post.Status.PUBLISHED,
            published_at__lte=timezone.now()
        ).order_by('-published_at').first()
        return latest.published_at if latest else None

    def location(self, obj):
        return reverse("blog:category_posts", kwargs={"slug": obj.slug})


class StaticSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return ["post_list"]

    def location(self, item):
        from django.urls import reverse
        return reverse("blog:" + item)
