from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from django.contrib.auth.models import User

from ..models import (
    Profile,
)

from ..forms import (
    ProfileForm,
)


def profile(request, username):

    profile_user = get_object_or_404(
        User,
        username=username,
    )

    profile, created = Profile.objects.get_or_create(
        user=profile_user,
    )

    if request.user == profile_user:

        if request.method == "POST":

            form = ProfileForm(
                request.POST,
                instance=profile,
            )

            if form.is_valid():

                form.save()

                return redirect(
                    "profile",
                    username=profile_user.username,
                )

        else:

            form = ProfileForm(
                instance=profile,
            )

    else:

        form = None

    submissions = profile_user.posts.all()

    comments = profile_user.comments.all()

    post_karma = sum(
        post.vote_count()
        for post in submissions
    )

    comment_karma = sum(
        comment.vote_count()
        for comment in comments
    )

    karma = post_karma + comment_karma

    return render(
        request,
        "home/profile.html",
        {
            "profile_user": profile_user,
            "profile": profile,
            "submissions": submissions,
            "comments": comments,
            "karma": karma,
            "form": form,
        },
    )


def user_submissions(request, username):

    profile_user = get_object_or_404(
        User,
        username=username,
    )

    posts = profile_user.posts.order_by(
        "-created_at",
    )

    return render(
        request,
        "home/user_submissions.html",
        {
            "profile_user": profile_user,
            "posts": posts,
        },
    )


def user_comments(request, username):

    profile_user = get_object_or_404(
        User,
        username=username,
    )

    comments = profile_user.comments.order_by(
        "-created_at",
    )

    return render(
        request,
        "home/user_comments.html",
        {
            "profile_user": profile_user,
            "comments": comments,
        },
    )