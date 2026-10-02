from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import View, ListView, DetailView, FormView
from taggit.models import Tag
from django.contrib import messages
from django.core.signing import Signer, BadSignature


from .forms import SubscriberForm
from .models import Post, Category, Subscriber
from .forms import CommentForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        context["comments"] = self.object.comments.filter(is_approved=True)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.save()
            return redirect(self.object.get_absolute_url())
        context = self.get_context_data()
        context["comment_form"] = form
        return self.render_to_response(context)


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


class SubscribeView(FormView):
    form_class = SubscriberForm
    success_url = "/"  # Home page

    def form_valid(self, form):
        email = form.cleaned_data["email"].lower()
        existing = Subscriber.objects.filter(email=email).first()

        if existing:
            if existing.is_active:
                messages.info(self.request, "You are already Subscribed!")
            else:
                existing.is_active = True
                existing.save()
                messages.success(
                    self.request, "Welcome back!, Your subscription has been reactivated.")
        else:
            Subscriber.objects.create(email=email)
            messages.success(self.request, "Thanks for Subscribing!")

        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "Please check the form.")
        return redirect(self.request.META.get("HTTP_REFERER", "/"))


class UnsubscribeView(View):
    def get(self, request, signed_token):
        signer = Signer()
        try:
            token = signer.unsign(signed_token)
        except BadSignature:
            messages.error(request, "invalid unsubscribe link.")
            return redirect("post_list")

        subscriber = get_object_or_404(Subscriber, unsubscribe_token=token)
        subscriber.is_active = False
        subscriber.save()
        messages.success(request, "You have been unsubscribed.")
        return redirect("post_list")
