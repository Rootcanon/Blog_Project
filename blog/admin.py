from django.contrib import admin
from django.utils import timezone

from .models import Category, Post
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "published_at")
    list_filter = ("status", "category")
    search_fields = ("title", "content")
    actions = ["make_published"]

    def make_published(self, request, queryset):
        updated = queryset.filter(
            status__in=[Post.Status.DRAFT, Post.Status.SCHEDULED]
        ).update(
            status=Post.Status.PUBLISHED,
            published_at=timezone.now()
        )
        self.message_user(request, f"{updated} post(s) published")
    make_published.short_description = "Publish selected posts now"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', "post_count")
    prepopulated_fields = {'slug': ("name",)}
    search_fields = ("name",)

    def post_count(self, obj):
        return obj.posts.count()

    post_count.short_description = "Posts"


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
