from django.core.cache import cache

from ..models import Post
from .ranking import get_ranked_posts


CACHE_KEY = "trending_posts"


def refresh_trending_posts():
    """
    Recalculate the trending posts and update Redis.
    """

    ranked_posts = get_ranked_posts(
        Post.objects.all(),
    )

    post_ids = [
        post.id
        for post in ranked_posts
    ]

    cache.set(
        CACHE_KEY,
        post_ids,
        timeout=None,
    )

    return post_ids


def get_cached_trending_posts():
    """
    Get trending posts from Redis.
    If the cache is empty, build it first.
    """

    post_ids = cache.get(CACHE_KEY)

    if post_ids is None:
        post_ids = refresh_trending_posts()

    posts = list(
        Post.objects.filter(
            id__in=post_ids,
        )
    )

    posts.sort(
        key=lambda post: post_ids.index(post.id),
    )

    return posts