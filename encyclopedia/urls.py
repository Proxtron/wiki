from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("newpage", views.newpage, name="newpage"),
    path("createnewpage", views.createnewpage, name="createnewpage"),
    path("editpage/<str:title>", views.editpage, name="editpage"),
    path("editpagecontents/<str:title>", views.editpagecontents, name="editpagecontents"),
    path("randompage", views.randompage, name="randompage")
]
