from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from django.contrib.auth.decorators import login_required

from ..models import (
    Comment,
    CommentVote,
)

from ..forms import CommentForm


@login_required
def edit_comment(request, comment_id):

    comment = get_object_or_404(
        Comment,
        id=comment_id,
        user=request.user,
    )

    if request.method == "POST":

        form = CommentForm(
            request.POST,
            instance=comment,
        )

        if form.is_valid():

            form.save()

            return redirect(
                "post_detail",
                post_id=comment.post.id,
            )

    else:

        form = CommentForm(
            instance=comment,
        )

    return render(
        request,
        "home/edit_comment.html",
        {
            "form": form,
            "comment": comment,
        },
    )


@login_required
def delete_comment(request, comment_id):

    comment = get_object_or_404(
        Comment,
        id=comment_id,
        user=request.user,
    )

    if request.method == "POST":

        post_id = comment.post.id

        comment.delete()

        return redirect(
            "post_detail",
            post_id=post_id,
        )

    return render(
        request,
        "home/delete_comment.html",
        {
            "comment": comment,
        },
    )


@login_required
def reply_comment(request, comment_id):

    parent_comment = get_object_or_404(
        Comment,
        id=comment_id,
    )

    post = parent_comment.post

    if request.method == "POST":

        form = CommentForm(
            request.POST,
        )

        if form.is_valid():

            reply = form.save(
                commit=False,
            )

            reply.user = request.user
            reply.post = post
            reply.parent = parent_comment

            reply.save()

            return redirect(
                "post_detail",
                post_id=post.id,
            )

    else:

        form = CommentForm()

    return render(
        request,
        "home/reply.html",
        {
            "form": form,
            "comment": parent_comment,
            "post": post,
        },
    )


@login_required
def vote_comment(request, comment_id):

    comment = get_object_or_404(
        Comment,
        id=comment_id,
    )

    if comment.user != request.user:

        CommentVote.objects.get_or_create(
            user=request.user,
            comment=comment,
        )

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "home",
        )
    )


def comments_page(request):

    comments = (
        Comment.objects
        .select_related(
            "user",
            "post",
        )
        .order_by("-created_at")
    )

    return render(
        request,
        "home/comments.html",
        {
            "comments": comments,
        },
    )


@login_required
def threads(request):

    comments = Comment.objects.filter(
        user=request.user,
    ).order_by("-created_at")

    return render(
        request,
        "home/threads.html",
        {
            "comments": comments,
        },
    )