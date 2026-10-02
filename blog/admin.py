from django.contrib import admin
from django.utils import timezone

from .models import Category, Post, AuthorProfile, Comment, Subscriber
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


class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "post", "created_at", "is_approved")
    list_filter = ("is_approved", "created_at")
    search_fields = ("name", "email", "content")
    actions = ["approve_comments", "reject_comments"]

    def approve_comments(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} comment(s) approved")
    approve_comments.short_description = 'Approve selected comments'

    def reject_comments(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f"{updated} comment(s) rejected")
    reject_comments.short_description = "Reject selected comments"


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "created_at", "unsubscribe_token")
    list_filter = ("is_active", "created_at")
    search_fields = ("email",)
    readonly_fields = ("unsubscribe_token", "created_at")
    list_editable = ("is_active",)
    actions = ["activate_subscribers", "deactivate_subscribers"]

    def activate_subscribers(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} subscriber(s) activated")
    activate_subscribers.short_description = "Activate selected subscribers"

    def deactivate_subscribers(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} subscriber(s) deactivated")

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(AuthorProfile, AuthorProfileAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Subscriber, SubscriberAdmin)