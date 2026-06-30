from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta

from ..models import (
    Post,
    PostVote,
)

from ..forms import (
    PostForm,
    CommentForm,
)

from ..services.ranking import get_ranked_posts


def home(request):

    ranked_posts = get_ranked_posts(
        Post.objects.all(),
    )

    paginator = Paginator(
        ranked_posts,
        30,
    )

    page_number = request.GET.get("page")

    posts = paginator.get_page(
        page_number,
    )

    return render(
        request,
        "home/home.html",
        {
            "posts": posts,
        },
    )


def new_posts(request):

    posts = Post.objects.order_by(
        "-created_at",
    )

    return render(
        request,
        "home/new.html",
        {
            "posts": posts,
        },
    )


def ask_posts(request):

    posts = get_ranked_posts(
        Post.objects.filter(
            post_type="ASK",
        )
    )

    return render(
        request,
        "home/ask.html",
        {
            "posts": posts,
        },
    )


def show_posts(request):

    posts = get_ranked_posts(
        Post.objects.filter(
            post_type="SHOW",
        )
    )

    return render(
        request,
        "home/show.html",
        {
            "posts": posts,
        },
    )


def past_posts(request):

    period = request.GET.get(
        "period",
        "all",
    )

    posts = Post.objects.all()

    if period == "day":

        posts = posts.filter(
            created_at__gte=timezone.now() - timedelta(days=1),
        )

    elif period == "week":

        posts = posts.filter(
            created_at__gte=timezone.now() - timedelta(days=7),
        )

    elif period == "month":

        posts = posts.filter(
            created_at__gte=timezone.now() - timedelta(days=30),
        )

    posts = posts.order_by("-created_at")

    return render(
        request,
        "home/past.html",
        {
            "posts": posts,
            "period": period,
        },
    )


@login_required
def submit_view(request):

    if request.method == "POST":

        form = PostForm(
            request.POST,
        )

        if form.is_valid():

            post = form.save(
                commit=False,
            )

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

    post = get_object_or_404(
        Post,
        id=post_id,
    )

    if request.method == "POST":

        if not request.user.is_authenticated:
            return redirect("login")

        form = CommentForm(
            request.POST,
        )

        if form.is_valid():

            comment = form.save(
                commit=False,
            )

            comment.post = post
            comment.user = request.user

            comment.save()

            return redirect(
                "post_detail",
                post_id=post.id,
            )

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
def vote_post(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
    )

    if post.user != request.user:

        PostVote.objects.get_or_create(
            user=request.user,
            post=post,
        )

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "home",
        )
    )