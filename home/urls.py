from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("submit/", views.submit_view, name="submit"),
    path("posts/<int:post_id>/", views.post_detail, name="post_detail"),
    path("comments/<int:comment_id>/reply/",views.reply_comment,name="reply_comment"),
    path("posts/<int:post_id>/vote/",views.vote_post,name="vote_post"),
    path("comments/<int:comment_id>/vote/",views.vote_comment,name="vote_comment"),
]