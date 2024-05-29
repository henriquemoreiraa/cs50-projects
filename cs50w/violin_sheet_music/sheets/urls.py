from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("upload-sheet", views.upload_sheet, name="upload-sheet"),
    path("sheets", views.sheets, name="sheets"),
    path("sheet/<int:id>", views.sheet, name="sheet"),
    path("attempt/<int:id>", views.attempt, name="attempt"),
    path("rate/<int:attempt_id>", views.rate, name="rate"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]
