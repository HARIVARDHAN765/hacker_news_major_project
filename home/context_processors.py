from .models import Post, Comment


def user_karma(request):

    if not request.user.is_authenticated:
        return {}

    submissions = request.user.posts.all()
    comments = request.user.comments.all()

    post_karma = sum(post.vote_count() for post in submissions)
    comment_karma = sum(comment.vote_count() for comment in comments)

    return {
        "user_karma": post_karma + comment_karma,
    }