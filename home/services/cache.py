from django.core.cache import cache

from ..models import Post
from .ranking import get_ranked_posts


def get_cached_trending_posts():

    post_ids = cache.get("trending_posts")

    if post_ids is None:

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

    posts = list(
        Post.objects.filter(
            id__in=post_ids,
        )
    )

    posts.sort(
        key=lambda post: post_ids.index(post.id),
    )

    return posts