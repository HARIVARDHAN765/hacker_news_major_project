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
    path("user/<str:username>/",views.profile,name="profile"),
    path("user/<str:username>/submitted/",views.user_submissions,name="user_submissions"),
    path("user/<str:username>/comments/",views.user_comments,name="user_comments"),
    path("posts/<int:post_id>/edit/",views.edit_post,name="edit_post"),
    path("posts/<int:post_id>/delete/",views.delete_post,name="delete_post"),
    path("comments/<int:comment_id>/edit/",views.edit_comment,name="edit_comment"),
    path("comments/<int:comment_id>/delete/",views.delete_comment,name="delete_comment"),
    path("ask/",views.ask_posts,name="ask"),
    path("show/",views.show_posts,name="show"),
]