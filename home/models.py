from django.db import models
from django.conf import settings
from django.utils import timezone
import math


class Post(models.Model):

    POST_TYPES = [
        ("NEWS", "News"),
        ("ASK", "Ask HN"),
        ("SHOW", "Show HN"),
    ]

    title = models.CharField(max_length=255)
    url = models.URLField(blank=True)
    text = models.TextField(blank=True)

    post_type = models.CharField(
        max_length=10,
        choices=POST_TYPES,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def vote_count(self):
        return self.votes.count()

    def __str__(self):
        return self.title
    
    def ranking_score(self):
        votes = getattr(self, "vote_total", None)
        if votes is None:
            votes = self.vote_count()
        age_hours = (timezone.now() - self.created_at).total_seconds() / 3600
        return (votes + 1) / math.pow(age_hours + 2,1.8,)


class Comment(models.Model):

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies"
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def vote_count(self):
        return self.votes.count()

    def __str__(self):
        return f"{self.user.username} commented on {self.post.title}"
    


class PostVote(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="post_votes"
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="votes"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"],
                name="unique_post_vote"
            )
        ]

    def __str__(self):
        return f"{self.user.username} voted for {self.post.title}"
    


class CommentVote(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comment_votes"
    )

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="votes"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "comment"],
                name="unique_comment_vote"
            )
        ]

    def __str__(self):
        return f"{self.user.username} voted for a comment"
    

class Profile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    about = models.TextField(
        blank=True,
    )

    def __str__(self):
        return self.user.username