from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        SCHEDULED = "scheduled", "Scheduled"

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts")

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")

    content = RichTextUploadingField()

    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.DRAFT)

    published_at = models.DateTimeField(null=True, blank=True)
    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ["-published_at"]

    def save(self, *args, **kwargs):
        if self.pk:
            original = Post.objects.get(pk=self.pk)
            if (original.status != self.Status.PUBLISHED
                    and self.status == self.Status.PUBLISHED
                    and not self.published_at):
                self.published_at = timezone.now()

        if not self.pk:
            base = slugify(self.title)
            slug = base
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                counter += 1
                slug = f"{base}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.title} {self.author} {self.status} {self.published_at}"


class AuthorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="author_profile"
    )
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def post_count(self):
        return self.user.posts.filter(status=Post.Status.PUBLISHED).count()

    def __str__(self):
        return f"{self.user.username}'s Profile"
