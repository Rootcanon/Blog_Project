from django.urls import path

from .views import PostListView, PostDetailView, CategoryPostListView, TagPostListView, AuthorPostListView


urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("<slug:slug>/", PostDetailView.as_view(), name="post_detail"),
    path("category/<slug:slug>/",  CategoryPostListView.as_view(), name="category_posts"),
    path("tag/<slug:slug>/", TagPostListView.as_view(), name="tag_posts"),
    path("author/<str:username>/", AuthorPostListView.as_view(), name="author_posts"),
]
