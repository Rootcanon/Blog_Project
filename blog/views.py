from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView
from taggit.models import Tag

from .models import Post, Category
# Create your views here.


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        now = timezone.now()
        visible_posts = Post.objects.filter(
            status=Post.Status.PUBLISHED,
            published_at__lte=now)
        return visible_posts.select_related("author", "category")


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        now = timezone.now()
        visible_posts = Post.objects.filter(
            status=Post.Status.PUBLISHED,
            published_at__lte=now
        )
        return visible_posts.select_related("author", "category")


class CategoryPostListView(PostListView):
    """Posts filtered by category"""
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        return super().get_queryset().filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context

class TagPostListView(PostListView):
    """Posts filtered by tag"""
    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs["slug"])
        return super().get_queryset().filter(tags=self.tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.tag
        return context


class AuthorPostListView(PostListView):
    """Posts filtered by author"""
    def get_queryset(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        self.author = get_object_or_404(User, username=self.kwargs["username"])
        return super().get_queryset().filter(author=self.author)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["author"] = self.author
        return context