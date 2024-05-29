from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listings/<int:id>", views.listings, name="listings"),
    path("create-listing", views.create_listing, name="create_listing"),
    path("close_listing/<int:id>", views.close_listing, name="close_listing"),
    path("bid/<int:listing_pk>", views.bid, name="bid"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
    # path("listings/<int:id>", views.listings, name="listings"),
]
