from django.contrib import admin
from .models import Post, Comment, PostVote, CommentVote


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "post_type", "user", "created_at")
    list_filter = ("post_type", "created_at")
    search_fields = ("title", "text")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created_at")
    list_filter = ("created_at",)
    search_fields = ("content",)


@admin.register(PostVote)
class PostVoteAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created_at")


@admin.register(CommentVote)
class CommentVoteAdmin(admin.ModelAdmin):
    list_display = ("user", "comment", "created_at")