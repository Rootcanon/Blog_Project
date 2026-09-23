from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView, DetailView

from .models import Post
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
