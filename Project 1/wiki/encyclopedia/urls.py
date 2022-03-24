from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("create", views.create, name="create"),
    path("wiki/", views.random, name="random"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
]

