from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("categories", views.categoriespage, name="categoriespage"),
    path("categories/<str:category>", views.categorypage, name="categorypage"),
    path("create", views.create, name="create"),
    path("listings/<str:id>", views.listings, name="listings"),
    path("listings/<str:id>/bid", views.bid, name="bid"),
    path("listings/<str:id>/close", views.close, name="close"),
    path("listings/<str:id>/comment", views.comment, name="comment"),
    path("listings/<str:id>/unwatch", views.unwatch, name="unwatch"),
    path("listings/<str:id>/watch", views.watch, name="watch"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user/<str:name>", views.userpage, name="userpage"),
    path("watchlist", views.watchlist, name="watchlist")
]
