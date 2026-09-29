from django.contrib import admin
from django.utils import timezone

from .models import Category, Post, AuthorProfile
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "published_at", "tag_list")
    list_filter = ("status", "category", "tags")
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

    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.tags.all())
    tag_list.short_description = "Tags"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', "post_count")
    prepopulated_fields = {'slug': ("name",)}
    search_fields = ("name",)

    def post_count(self, obj):
        return obj.posts.count()

    post_count.short_description = "Posts"


class AuthorProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "post_count")
    search_fields = ("user__username", "user__email", "bio")

    def post_count(self, obj):
        return obj.post_count()


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(AuthorProfile, AuthorProfileAdmin)
