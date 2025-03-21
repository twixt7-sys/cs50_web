from django.urls import path

from . import views as v

urlpatterns = [
    path("", v.index, name="index"),
    path("login", v.login_view, name="login"),
    path("register", v.register, name="register"),
    path("logout", v.logout_view, name="logout"),
    path("create", v.create_listing, name="create"),
    path("listing/<int:listing_id>/", v.listing, name="listing"),
    path("watchlist", v.watchlist, name="watchlist"),
    path("categories", v.categories, name="categories")
]