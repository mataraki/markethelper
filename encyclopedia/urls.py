from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.createpage, name="createpage"),
    path("random", views.randompage, name="randompage"),
    path("wiki/<str:title>", views.entrypage, name="entrypage"),
    path("wiki/<str:title>/edit", views.editpage, name="editpage")
]
