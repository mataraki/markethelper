
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("edit/<str:postid>", views.edit, name="edit"),
    path("following", views.following, name="following"),
    path("following/posts/<str:pagenumber>", views.followingposts, name="followingposts"),
    path("like/<str:postid>", views.like, name="like"),
    path("newpost", views.newpost, name="newpost"),
    path("posts/<str:pagenumber>", views.posts, name="posts"),
    path("profile", views.profile, name="profile"),
    path("user/<str:name>", views.user, name="user"),
    path("user/<str:name>/follow", views.follow, name="follow"),
    path("user/<str:name>/posts/<str:pagenumber>", views.userposts, name="userposts")
]
