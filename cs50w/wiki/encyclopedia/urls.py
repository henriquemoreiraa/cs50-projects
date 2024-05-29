from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.wiki, name="wiki"),
    path("search-results/", views.search_results, name="search-results"),
    path("create-new-page/", views.create_new_page, name="create-new-page"),
    path("edit-page/<str:title>/", views.edit_page, name="edit-page"),
    path("random-page/", views.random_page, name="random-page")
]
