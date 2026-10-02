from django.urls import path

from .views import PostListView, PostDetailView, CategoryPostListView, TagPostListView, AuthorPostListView, SubscribeView, UnsubscribeView


urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("subscribe/", SubscribeView.as_view(), name="subscribe"),
    path("unsubscribe/<str:signed_token>/", UnsubscribeView.as_view(), name="unsubscribe"),
    path("<slug:slug>/", PostDetailView.as_view(), name="post_detail"),
    path("category/<slug:slug>/",  CategoryPostListView.as_view(), name="category_posts"),
    path("tag/<slug:slug>/", TagPostListView.as_view(), name="tag_posts"),
    path("author/<str:username>/", AuthorPostListView.as_view(), name="author_posts"),
]
