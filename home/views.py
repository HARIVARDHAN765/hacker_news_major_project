from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm, LoginForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Post, Comment, Profile
from django.shortcuts import get_object_or_404
from .forms import CommentForm
from .models import PostVote, CommentVote
from django.contrib.auth.models import User
from .forms import ProfileForm


def home(request):
    posts = Post.objects.all()

    return render(
        request,
        "home/home.html",
        {
            "posts": posts,
        },
    )



def profile(request, username):

    profile_user = get_object_or_404(
        User,
        username=username,
    )

    profile, created = Profile.objects.get_or_create(
        user=profile_user
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

    post_karma = 0
    for post in submissions:
        post_karma += post.vote_count()
    comment_karma = 0
    for comment in comments:
        comment_karma += comment.vote_count()
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

    posts = Post.objects.filter(
        user=profile_user,
    ).order_by("-created_at")

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

    comments = Comment.objects.filter(
        user=profile_user,
    ).order_by("-created_at")

    return render(
        request,
        "home/user_comments.html",
        {
            "profile_user": profile_user,
            "comments": comments,
        },
    )


def login_view(request):
    if request.method == "POST":

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            next_url = request.POST.get("next")

            if next_url:
                return redirect(next_url)

            return redirect("home")

    else:

        form = LoginForm()

    register_form = RegisterForm()

    return render(
        request,
        "home/login.html",
        {
            "login_form": form,
            "register_form": register_form,
        },
    )

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            Profile.objects.create(
                user=user
            )

            login(request, user)

            return redirect("home")

        login_form = LoginForm()

        return render(
            request,
            "home/login.html",
            {
                "register_form": form,
                "login_form": login_form,
            },
        )

    return redirect("login")
def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def submit_view(request):

    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            return redirect("home")

    else:
        form = PostForm()

    return render(
        request,
        "home/submit.html",
        {
            "form": form,
        },
    )
@login_required
def edit_post(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
        user=request.user,
    )

    if request.method == "POST":

        form = PostForm(
            request.POST,
            instance=post,
        )

        if form.is_valid():
            form.save()

            return redirect(
                "post_detail",
                post_id=post.id,
            )

    else:

        form = PostForm(
            instance=post,
        )

    return render(
        request,
        "home/edit_post.html",
        {
            "form": form,
            "post": post,
        },
    )
@login_required
def delete_post(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
        user=request.user,
    )

    if request.method == "POST":

        post.delete()

        return redirect("home")

    return render(
        request,
        "home/delete_post.html",
        {
            "post": post,
        },
    )

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


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")

        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()

            return redirect("post_detail", post_id=post.id)

    else:
        form = CommentForm()

    return render(
        request,
        "home/post_detail.html",
        {
            "post": post,
            "form": form,
        },
    )


@login_required
def reply_comment(request, comment_id):
    parent_comment = get_object_or_404(Comment, id=comment_id)
    post = parent_comment.post

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.parent = parent_comment
            reply.save()

            return redirect("post_detail", post_id=post.id)

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
def vote_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    PostVote.objects.get_or_create(
        user=request.user,
        post=post,
    )

    return redirect(request.META.get("HTTP_REFERER", "home"))


@login_required
def vote_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    CommentVote.objects.get_or_create(
        user=request.user,
        comment=comment,
    )

    return redirect(
        request.META.get("HTTP_REFERER", "home")
    )


def ask_posts(request):

    posts = Post.objects.filter(
        post_type="ASK"
    )

    return render(
        request,
        "home/ask.html",
        {
            "posts": posts,
        },
    )


def show_posts(request):

    posts = Post.objects.filter(
        post_type="SHOW",
    )

    return render(
        request,
        "home/show.html",
        {
            "posts": posts,
        },
    )