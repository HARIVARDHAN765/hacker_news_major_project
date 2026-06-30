from celery import shared_task
from django.core.cache import cache

from .models import Post
from .services.ranking import get_ranked_posts


@shared_task
def recalculate_trending_posts():

    ranked_posts = get_ranked_posts(
        Post.objects.all(),
    )

    post_ids = [
        post.id
        for post in ranked_posts
    ]

    cache.set(
        "trending_posts",
        post_ids,
        timeout=None,
    )

    return len(post_ids)