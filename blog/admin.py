from django.contrib import admin
from .models import Category, Post
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "published_at")
    # prepopulated_fields = {"slug": ("title",)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ("name",)}


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
