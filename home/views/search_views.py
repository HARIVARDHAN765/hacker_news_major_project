from django.shortcuts import render

from ..models import Post
from ..services.search import search_posts


def search(request):

    query = request.GET.get(
        "q",
        "",
    )

    posts = Post.objects.none()

    if query:

        posts = search_posts(
            query,
        )

    return render(
        request,
        "home/search.html",
        {
            "posts": posts,
            "query": query,
        },
    )