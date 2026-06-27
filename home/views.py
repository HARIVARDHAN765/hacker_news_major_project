from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm, LoginForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Post, Comment
from django.shortcuts import get_object_or_404
from .forms import CommentForm
from .models import PostVote, CommentVote


def home(request):
    posts = Post.objects.all()

    return render(
        request,
        "home/home.html",
        {
            "posts": posts,
        },
    )


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(
                request,
                username=username,
                password=password,
            )

            if user is not None:
                login(request, user)
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
        "post_detail",
        post_id=comment.post.id,
    )