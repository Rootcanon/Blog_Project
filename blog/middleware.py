from django.utils.deprecation import MiddlewareMixin

from .models import VisitCount, Post


class VisitCountMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if (request.method == "GET" and response.status_code == 200 and hasattr(request, 'resolver_match') and request.resolver_match and request.resolver_match.url_name == "post_detail"):
            slug = request.resolver_match.kwargs.get("slug")
            if slug:
                try:
                    post = Post.objects.get(
                        slug=slug, status=Post.Status.PUBLISHED)

                    visit_count, created = VisitCount.objects.get_or_create(post=post)
                    visit_count.count += 1
                    visit_count.save(update_fields=["count", "last_visited"])

                except Post.DoesNotExist:
                    pass
        return response
