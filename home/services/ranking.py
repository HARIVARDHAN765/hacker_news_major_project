from django.db.models import Count


def get_ranked_posts(queryset):

    posts = queryset.annotate(
        vote_total=Count("votes"),
    )

    return sorted(
        posts,
        key=lambda post: post.ranking_score(),
        reverse=True,
    )