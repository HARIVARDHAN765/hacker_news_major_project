from ..documents import PostDocument
from ..models import Post


def search_posts(query):

    if not query:
        return Post.objects.none()

    search = (
        PostDocument.search()
        .query(
            "multi_match",
            query=query,
            type="bool_prefix",
            fields=[
                "title.suggest",
                "title.suggest._2gram",
                "title.suggest._3gram",
                "user",
                "text",
            ],
        )
    )

    results = search.execute()

    post_ids = [
        int(hit.id)
        for hit in results
    ]

    posts = list(
        Post.objects.filter(
            id__in=post_ids,
        )
    )

    posts.sort(
        key=lambda post: post_ids.index(post.id)
    )

    return posts