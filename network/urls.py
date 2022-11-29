
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("tweet", views.tweet, name="tweet"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("allPosts", views.allPosts, name="allPosts")
]
