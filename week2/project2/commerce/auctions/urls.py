from django.urls import path

from . import views as v

urlpatterns = [
    path("", v.index, name="index"),
    path("login", v.login_view, name="login"),
    path("register", v.register, name="register"),
    path("logout", v.logout_view, name="logout"),
    path("create", v.create_listing, name="create")
]
