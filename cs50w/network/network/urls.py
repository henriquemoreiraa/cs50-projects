from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("following", views.following, name="following"),
    path("profile/<str:user_name>", views.profile, name="profile"),
    path("user/<str:user_name>", views.user, name="user"),
    path("posts", views.posts, name="posts"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]